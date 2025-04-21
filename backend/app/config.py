"""
Configuration module for the application.
Handles environment variables and client initialization.
"""
import os
from dotenv import load_dotenv # type: ignore
import cohere # type: ignore

# Load environment variables from .env file
load_dotenv()

# Initialize Cohere client
cohere_api_key = os.getenv("COHERE_API_KEY")
if not cohere_api_key:
    raise ValueError("COHERE_API_KEY environment variable is not set")

cohere_client = cohere.Client(cohere_api_key)

# Constants
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "500"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7")) 