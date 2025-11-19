"""
Tech Vocab AI Coach - FastAPI Application
Cloud-native microservice for learning technical concepts
"""
from fastapi import FastAPI
from app.routers import terms, quiz, vocabulary, auth

# Create FastAPI application instance
app = FastAPI(
    title="Tech Vocab AI Coach",
    description="Learn DevOps, Cloud, Backend, Networking, System Design, and Security",
    version="1.0.0"
)

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



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
