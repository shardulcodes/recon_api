import socket
import ssl
import requests
import dns.resolver
import logging

logger = logging.getLogger(__name__)

def get_subdomains(domain: str) -> list[str]:
    """
    Fetch subdomains using crt.sh certificate transparency logs.

    Args:
        domain (str): The base domain to search.

    Returns:
        list[str]: A list of unique subdomains.
    """
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


def get_hosts(domains: list[str]) -> dict:
    """
    Resolve domain or subdomain names to IP addresses.

    Args:
        domains (list[str]): List of domain or subdomain names.

    Returns:
        dict: Mapping of each domain to its resolved IP address list.
    """
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


def get_cert(domain: str) -> list:
    """
    Retrieve TLS certificate subject and issuer information.

    Args:
        domain (str): Domain to connect to via SSL.

    Returns:
        list: [subject info, issuer info]
    """
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.settimeout(5.0)
            s.connect((domain, 443))
            cert = s.getpeercert()
            return [
                cert.get("subject", []),
                cert.get("issuer", [])
            ]
    except Exception as e:
        logger.warning(f"TLS certificate retrieval failed for {domain}: {e}")
        return []


def get_email_records(domain: str) -> dict:
    """
    Query DNS records related to email configuration (MX, SPF, DKIM, DMARC).

    Args:
        domain (str): The domain to query.

    Returns:
        dict: Dictionary with keys: mx, spf, dkim, dmarc
    """
    records = {}

    # MX Records
    try:
        mx_records = dns.resolver.resolve(domain, "MX", lifetime=5)
        records["mx"] = [r.exchange.to_text() for r in mx_records]
    except Exception as e:
        logger.warning(f"MX record lookup failed for {domain}: {e}")
        records["mx"] = []

    # TXT Records (to find SPF, DKIM, DMARC)
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

    # Default to empty strings if any are missing
    records.setdefault("spf", "")
    records.setdefault("dmarc", "")
    records.setdefault("dkim", "")

    return records


async def perform_recon(domain: str) -> dict:
    """
    Perform full passive recon on a domain.

    Args:
        domain (str): The domain to analyze.

    Returns:
        dict: Recon results (subdomains, hosts, certs, email records)
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
