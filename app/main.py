from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import ReconRequest, ReconResponse
from app.recon import perform_recon
import logging

# -----------------------
# App Configuration
# -----------------------
app = FastAPI(
    title="Reconnaissance API",
    description="An API that performs passive reconnaissance on a given domain.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# -----------------------
# Optional: Enable CORS
# -----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, change this to restrict origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# Setup logging
# -----------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -----------------------
# API Endpoint
# -----------------------
@app.post("/api/v1/recon", response_model=ReconResponse, tags=["Reconnaissance"])
async def recon_endpoint(request: ReconRequest):
    """
    Perform passive reconnaissance on a given domain.

    - **domain**: Domain to analyze (e.g., "example.com")
    - Returns: Subdomains, Hosts, Certificates, Email DNS Records
    """
    logger.info(f"Received recon request for domain: {request.domain}")

    try:
        result = await perform_recon(request.domain)
        return result
    except Exception as e:
        logger.error(f"Recon failed for domain {request.domain}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
