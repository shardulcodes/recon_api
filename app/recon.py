import socket
import ssl
import requests
import dns.resolver
import logging
from typing import List, Dict
from app.models import CertificateInfo  # Make sure this is imported properly

logger = logging.getLogger(__name__)


def get_subdomains(domain: str) -> List[str]:
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        subdomains = set()

        for item in data:
            name = item.get("name_value", "")
            for entry in name.split("\n"):
                if domain in entry:
                    subdomains.add(entry.strip())

        return sorted(list(subdomains))
    except Exception as e:
        logger.warning(f"Subdomain enumeration failed for {domain}: {e}")
        return []


def get_hosts(domains: List[str]) -> Dict[str, List[str]]:
    hosts = {}
    for subdomain in domains:
        try:
            ip = socket.gethostbyname(subdomain)
            hosts[subdomain] = [ip]
        except socket.gaierror:
            hosts[subdomain] = []
        except Exception as e:
            logger.warning(f"Host resolution error for {subdomain}: {e}")
            hosts[subdomain] = []
    return hosts


def parse_name_to_3d_list(name_list) -> List[List[List[str]]]:
    """
    Converts certificate name fields to required 3D list format.
    Example: [[("CN", "xyz"), ("O", "abc")]] → [[["CN", "xyz"], ["O", "abc"]]]
    """
    return [[[k, v] for k, v in group] for group in name_list]



def get_cert(domain: str) -> List[CertificateInfo]:
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.settimeout(5.0)
            s.connect((domain, 443))
            cert = s.getpeercert()

            def to_nested_list(name_list):
                result = []
                for attr in name_list:
                    inner = []
                    for k, v in attr:
                        inner.append([k, v])
                    result.append(inner)
                return result

            subject = to_nested_list(cert.get("subject", []))
            issuer = to_nested_list(cert.get("issuer", []))

            return [CertificateInfo(subject=subject, issuer=issuer)]
    except Exception as e:
        logger.warning(f"TLS certificate retrieval failed for {domain}: {e}")
        return [CertificateInfo(subject=[], issuer=[])]  # ✅ Always return a valid structure




def get_email_records(domain: str) -> Dict[str, List[str] or str]:
    records = {}

    try:
        mx_records = dns.resolver.resolve(domain, "MX", lifetime=5)
        records["mx"] = [r.exchange.to_text() for r in mx_records]
    except Exception as e:
        logger.warning(f"MX record lookup failed for {domain}: {e}")
        records["mx"] = []

    try:
        txt_records = dns.resolver.resolve(domain, "TXT", lifetime=5)
        for r in txt_records:
            txt = r.to_text().strip('"').lower()
            if "spf" in txt and "spf" not in records:
                records["spf"] = txt
            if "dmarc" in txt and "dmarc" not in records:
                records["dmarc"] = txt
            if "dkim" in txt and "dkim" not in records:
                records["dkim"] = txt
    except Exception as e:
        logger.warning(f"TXT record lookup failed for {domain}: {e}")

    # Default empty fields
    records.setdefault("spf", "")
    records.setdefault("dmarc", "")
    records.setdefault("dkim", "")

    return records


async def perform_recon(domain: str) -> Dict:
    """
    Perform passive recon and return data formatted to match ReconResponse schema.
    """
    logger.info(f"Starting recon for domain: {domain}")

    subdomains = get_subdomains(domain)
    all_domains = subdomains + [domain]

    hosts = get_hosts(all_domains)
    certs = {d: get_cert(d) for d in all_domains}
    email_records = get_email_records(domain)

    result = {
        "subdomains": subdomains,
        "hosts": hosts,
        "certs": certs,
        "email_records": email_records
    }

    logger.info(f"Recon completed for domain: {domain}")
    return result
