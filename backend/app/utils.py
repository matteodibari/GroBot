"""
Utility functions for the Mangrove Chatbot.
"""
import os
from typing import List
from dotenv import load_dotenv


def load_environment_variables() -> None:
    """
    Load environment variables from .env file.
    Raises an error if required variables are missing.
    """
    load_dotenv()

    required_vars = ["OPENAI_API_KEY", "COHERE_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars and not os.getenv("TESTING"):
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )


def validate_api_keys() -> None:
    """
    Validate that API keys are properly formatted.
    This doesn't check if they're valid, just that they're formatted correctly.
    """
    # Skip validation in test environment
    if os.getenv("TESTING"):
        return

    openai_key = os.getenv("OPENAI_API_KEY", "")
    cohere_key = os.getenv("COHERE_API_KEY", "")

    if not openai_key.startswith("sk-"):
        raise ValueError("Invalid OpenAI API key format")

    if len(cohere_key) < 32:
        raise ValueError("Invalid Cohere API key format")


def format_sources(sources: List[str]) -> str:
    """
    Format a list of source documents into a readable string.

    Args:
        sources: List of source document names

    Returns:
        Formatted string of sources
    """
    if not sources:
        return "No sources available"

    unique_sources = sorted(set(sources))
    return "\n".join([f"- {source}" for source in unique_sources])


def create_error_response(error: Exception) -> dict:
    """
    Create a standardized error response.

    Args:
        error: The exception that occurred

    Returns:
        Dictionary with error details
    """
    return {
        "status": "error",
        "message": str(error),
        "type": error.__class__.__name__
    }
