# 🔍 Reconnaissance API

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-⚡-green)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Containerized-Docker-blue)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [API Documentation](#-api-documentation)
- [Setup (Local)](#-setup-local)
- [Docker Deployment](#-docker-deployment)
- [Sample Request](#-sample-request)
- [Testing](#-testing)
- [License](#-license)

---

## 📖 Overview

This project is a **passive reconnaissance microservice** built using FastAPI. Given a domain name, it gathers:

- ✅ All subdomains
- ✅ IP addresses (hostnames)
- ✅ TLS certificates
- ✅ Email DNS records (SPF, DKIM, DMARC, MX)

The API can be used for cybersecurity reconnaissance, penetration testing setups, or automated domain analysis workflows.

---

## 🚀 Features

- ⚡ Built with **FastAPI**
- 🧠 DNS & TLS inspection using `dnspython`, `ssl`, and `crt.sh`
- 🔐 Secure and containerized with Docker
- ✅ Includes unit tests for API contract
- 📦 Fully documented Swagger UI (`/docs`)
- 🧪 Production-ready code with logging and error handling

---

## ⚙️ Tech Stack

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

## 📑 API Documentation

Once running, visit:
