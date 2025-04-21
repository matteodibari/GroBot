"""
Main FastAPI application file for the Mangrove Chatbot backend.
"""
from fastapi import FastAPI, HTTPException # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from .api import router
from .utils import load_environment_variables, validate_api_keys

# Load and validate environment variables
try:
    load_environment_variables()
    validate_api_keys()
except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

# Create FastAPI app instance
app = FastAPI(
    title="Mangrove Chatbot API",
    description="A RAG-based chatbot system for mangrove ecosystem information",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include router
app.include_router(router, prefix="/api")

# Health check endpoint
@app.get("/")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "healthy", "message": "Mangrove Chatbot API is running"}
