"""
Tech Vocab AI Coach - FastAPI Application
Cloud-native microservice for learning technical concepts
"""
from fastapi import FastAPI
from app.routers import terms

# Create FastAPI application instance
app = FastAPI(
    title="Tech Vocab AI Coach",
    description="Learn DevOps, Cloud, Backend, Networking, System Design, and Security",
    version="1.0.0"
)

# Register routers
app.include_router(terms.router)


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



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
