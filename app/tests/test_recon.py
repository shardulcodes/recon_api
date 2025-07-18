from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_recon_api_response_structure():
    """
    Test the /api/v1/recon endpoint to ensure correct structure of response.
    """
    test_domain = "example.com"
    response = client.post("/api/v1/recon", json={"domain": test_domain})

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    
    data = response.json()
    
    # Top-level keys
    for key in ["subdomains", "hosts", "certs", "email_records"]:
        assert key in data, f"Missing key in response: {key}"

    # Validate types
    assert isinstance(data["subdomains"], list), "Subdomains should be a list"
    assert isinstance(data["hosts"], dict), "Hosts should be a dictionary"
    assert isinstance(data["certs"], dict), "Certs should be a dictionary"
    assert isinstance(data["email_records"], dict), "Email records should be a dictionary"

    # Optional deeper checks
    if data["subdomains"]:
        assert all(isinstance(sub, str) for sub in data["subdomains"]), "Subdomain entries should be strings"

    if data["hosts"]:
        for host, ips in data["hosts"].items():
            assert isinstance(ips, list), f"IPs for {host} should be a list"

    if data["certs"]:
        for domain, cert_list in data["certs"].items():
            assert isinstance(cert_list, list), f"Expected list of certs for {domain}"
            for cert in cert_list:
                assert isinstance(cert, dict), f"Cert for {domain} must be a dict"
                assert "subject" in cert, f"Missing 'subject' in cert for {domain}"
                assert "issuer" in cert, f"Missing 'issuer' in cert for {domain}"

