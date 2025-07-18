# ---- Base Image ----
FROM python:3.11-slim

# ---- Metadata ----
LABEL maintainer="Shardul <your.email@example.com>"
LABEL version="1.0"
LABEL description="Reconnaissance API built with FastAPI"

# ---- System Prep ----
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---- System dependencies ----
RUN apt-get update && \
    apt-get install -y gcc libffi-dev libssl-dev curl dnsutils && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# ---- Working Directory ----
WORKDIR /app

# ---- Copy App ----
COPY . .

# ---- Install Python dependencies ----
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ---- Add a non-root user (Optional but recommended) ----
RUN useradd -m reconuser
USER reconuser

# ---- Run App ----
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
