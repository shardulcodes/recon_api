from pydantic import BaseModel, Field
from typing import List, Dict, Union, Optional


class ReconRequest(BaseModel):
    """
    Request model for recon API.

    Attributes:
        domain (str): Target domain to perform reconnaissance on.
    """
    domain: str = Field(..., example="example.com")


class CertificateInfo(BaseModel):
    """
    TLS certificate subject or issuer information.
    Each is a list of key-value pairs.
    """
    subject: List[List[List[str]]] = Field(..., description="TLS subject fields")
    issuer: List[List[List[str]]] = Field(..., description="TLS issuer fields")


class ReconResponse(BaseModel):
    """
    Response model containing recon results.

    Attributes:
        subdomains (List[str]): Discovered subdomains.
        hosts (Dict[str, List[str]]): Mapping of domain/subdomain to resolved IPs.
        certs (Dict[str, CertificateInfo]): TLS cert subject/issuer for each domain.
        email_records (Dict[str, Union[str, List[str]]]): MX, SPF, DKIM, DMARC records.
    """
    subdomains: List[str]
    hosts: Dict[str, List[str]]
    certs: Dict[str, CertificateInfo]
    email_records: Dict[str, Union[str, List[str]]]
