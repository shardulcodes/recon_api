Thanks for sharing that! Since I can't view your page content directly, I’ll help you fix the Markdown rendering issues based on what you've pasted. Here's a cleaned-up version of your `README.md` that should render properly when copied and pasted:

```markdown
# Reconnaissance API

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-%E2%9A%A1-green)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Containerized-Docker-blue)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [API Documentation](#api-documentation)
- [Setup](#setup)
  - [Run Locally](#run-locally)
  - [Run with Docker](#run-with-docker)
- [Sample Request](#sample-request)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [License](#license)
- [Author](#author)

---

## Overview

This project is a **passive reconnaissance microservice** built using **FastAPI**. Given a domain name, it gathers:

- All subdomains
- IP addresses (hostnames)
- TLS certificates
- Email DNS records (SPF, DKIM, DMARC, MX)

The API is useful for cybersecurity reconnaissance, penetration testing setups, or automated domain analysis.

---

## Features

- Built with FastAPI
- DNS and TLS inspection using `dnspython`, `ssl`, and `crt.sh`
- Dockerized for easy deployment
- Unit tests for API validation
- Swagger and ReDoc documentation auto-generated
- Minimal dependencies and clean code structure

---

## Tech Stack

| Component   | Description                 |
| ----------- | --------------------------- |
| Python 3.11 | Programming Language        |
| FastAPI     | Web framework (async-based) |
| Uvicorn     | ASGI server                 |
| Docker      | Containerization            |
| dnspython   | DNS queries                 |
| Requests    | HTTP client for `crt.sh`    |
| pytest      | Unit testing framework      |

---

## API Documentation

After running the project, access the API documentation at:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc UI: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Setup

### Run Locally

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/recon-api.git
cd recon-api

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs) to access the API interface.

---

### Run with Docker

```bash
# Build Docker image
docker build -t recon-api .

# Run the container
docker run -p 8000:8000 recon-api
```

Then visit [http://localhost:8000/docs](http://localhost:8000/docs) to explore the API.

---

## Sample Request

**Endpoint:** `POST /api/v1/recon`  
**Payload:**

```json
{
  "domain": "example.com"
}
```

**Response:**

```json
{
  "subdomains": ["sub1.example.com", "sub2.example.com"],
  "hosts": {
    "example.com": ["93.184.216.34"],
    "sub1.example.com": ["93.184.216.35"]
  },
  "certs": {
    "example.com": [
      {
        "subject": { "commonName": "example.com" },
        "issuer": { "commonName": "DigiCert Inc" }
      }
    ]
  },
  "email_records": {
    "mx": ["mail.example.com."],
    "spf": "v=spf1 include:spf.example.com ~all",
    "dkim": "v=DKIM1; k=rsa; p=....",
    "dmarc": "v=DMARC1; p=none; rua=mailto:dmarc@example.com"
  }
}
```

---

## Testing

To run unit tests and verify the API's response structure:

```bash
python -m pytest
```

Tests are located in `app/tests/test_recon.py` and validate:

- HTTP status code
- Response structure
- Field types (`list`, `dict`)
- Presence of keys like `subject` and `issuer` in certificate data

---

## Project Structure

```
recon_api/
├── app/
│   ├── main.py         # FastAPI app entrypoint
│   ├── recon.py        # Core recon logic (subdomains, certs, DNS)
│   ├── models.py       # Pydantic models (request/response)
│   └── tests/
│       └── test_recon.py  # Unit tests
├── Dockerfile            # Containerization config
├── requirements.txt      # Dependencies
└── README.md             # Documentation
```

---

## Author

**Shardul**
```

