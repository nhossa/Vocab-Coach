"""
Vocab AI Coach - FastAPI Application
A microservice for vocabulary learning with AI-powered simplification
"""

from app.schemas import WordSuggestionRequest, WordSuggestion

from fastapi import FastAPI

# Create FastAPI application instance
app = FastAPI(
    title="Vocab AI Coach",
    description="AI-powered vocabulary learning microservice",
    version="1.0.0"
)


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

@app.post("/api/v1/suggest")
async def suggest_word(request: WordSuggestionRequest):
    # For now, return a dummy word based on part_of_speech
    # We'll add real logic later
    return WordSuggestion(
        word="serendipitous",
        part_of_speech=request.part_of_speech,
        difficulty=request.difficulty,
        simple_definition="Happening by lucky accident",
        example="Finding money in your pocket is serendipitous"
    )



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
