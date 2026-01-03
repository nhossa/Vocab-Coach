"""
StackTutor - FastAPI Application
Cloud-native microservice for learning technical concepts
"""
import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.database import Base, engine
from app.routers import terms, quiz, vocabulary, auth
from seed import seed_terms

# Setup logging first (must be before other imports)
from app import logging_config

# Get logger for this module
logger = logging.getLogger(__name__)

# Get environment setting
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Create rate limiter (limits requests per IP address)
limiter = Limiter(key_func=get_remote_address)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: db
    logger.info("Application starting", extra={"environment": ENVIRONMENT})
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created/verified")
    
    # Startup: seed initial terms (safe skip if exists)
    try:
        seed_terms()
        logger.info("Database seeded with initial terms")
    except Exception as e:
        logger.warning(f"Seed skipped: {str(e)}")
    
    logger.info("Application startup complete")
    yield
    logger.info("Application shutting down") 



# Create FastAPI application instance
app = FastAPI(
    title="StackTutor",
    description="Learn DevOps, Cloud, Backend, Networking, System Design, and Security",
    version="1.0.0",
    lifespan=lifespan,
)

# Attach rate limiter to app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS based on environment
if ENVIRONMENT == "production":
    # Production: Only allow specific domain
    frontend_url = os.getenv("FRONTEND_URL", "")
    allowed_origins = [frontend_url] if frontend_url else []
else:
    # Development: Allow localhost and file://
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security: Trusted Host middleware (prevents Host header attacks)
if ENVIRONMENT == "production":
    frontend_domain = os.getenv("FRONTEND_URL", "").replace("https://", "").replace("http://", "")
    allowed_hosts = [frontend_domain] if frontend_domain else ["*"]
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)

# Security: Add security headers middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains" if ENVIRONMENT == "production" else ""
        return response

app.add_middleware(SecurityHeadersMiddleware)

# Register routers with common prefix
app.include_router(auth.router, prefix="/api/v1")
app.include_router(terms.router, prefix="/api/v1")
app.include_router(quiz.router, prefix="/api/v1")
app.include_router(vocabulary.router, prefix="/api/v1")


@app.get("/")
async def root():
    """
    Root endpoint - Welcome message
    """
    return {
        "message": "Welcome to Vocab AI Coach API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return {"status": "healthy"}


@app.get("/alive")
async def liveness_probe():
    """
    Kubernetes liveness probe - indicates container is alive
    Returns 200 if app process is running
    """
    return {"status": "alive", "message": "Container is running"}


@app.get("/ready")
async def readiness_probe():
    """
    Kubernetes readiness probe - indicates app is ready to handle traffic
    Checks database connectivity
    """
    try:
        # Check database connection
        from sqlalchemy import text
        from app.database import SessionLocal
        
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        
        return {
            "status": "ready",
            "message": "Application is ready to handle requests",
            "database": "connected"
        }
    except Exception as e:
        logger.error(f"Readiness check failed: {str(e)}")
        return {
            "status": "not_ready",
            "message": "Application is not ready",
            "database": "disconnected",
            "error": str(e)
        }, 503


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
