"""
API endpoints for the Mangrove Chatbot.

This module provides the following endpoints:
1. POST /upload - Upload and process PDF documents
2. POST /chat - Generate chat responses using RAG
3. GET /documents - List all processed documents
4. DELETE /documents/{filename} - Remove a document

The API uses FastAPI for high performance and automatic OpenAPI documentation.
All endpoints are async for better scalability and performance.
"""
import os
import shutil
from typing import List
from pathlib import Path
from fastapi import APIRouter, HTTPException, UploadFile, File # type: ignore
from .models import ChatRequest, ChatResponse, Document
from .data_processing import DocumentProcessor
from .rag import RAGPipeline
from .data_loader import load_documents, get_document_list, DATA_DIR

# Create router
router = APIRouter()

# Initialize document processor
doc_processor = DocumentProcessor()

# Initialize RAG pipeline with documents from data directory
rag_pipeline = load_documents()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)) -> dict:
    """
    Upload and process a PDF document.

    Args:
        file: PDF file to upload

    Returns:
        Dictionary with processing status
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    try:
        # Save the file to the data directory
        file_path = DATA_DIR / file.filename
        
        # Save the uploaded file
        with open(file_path, "wb") as dest_file:
            content = await file.read()
            dest_file.write(content)

        # Process the PDF
        documents = doc_processor.process_pdf(str(file_path))

        # Update RAG pipeline
        global rag_pipeline
        if rag_pipeline is None:
            rag_pipeline = RAGPipeline(documents)
        else:
            rag_pipeline.documents.extend(documents)

        return {
            "status": "success",
            "message": f"Successfully processed {file.filename}",
            "num_chunks": len(documents)
        }

    except Exception as e:
        # Clean up file in case of error
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat")
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Generate a response to a chat message.

    Args:
        request: Chat request containing messages and parameters

    Returns:
        ChatResponse with assistant's response
    """
    if not request.messages:
        raise HTTPException(
            status_code=422,
            detail="No messages provided in the request"
        )

    if rag_pipeline is None or not rag_pipeline.documents:
        raise HTTPException(
            status_code=400,
            detail="I'm not ready to chat yet. Please try again in a moment."
        )

    try:
        # Get the user's latest message
        user_message = request.messages[-1].content

        # Generate response using RAG pipeline
        response_text, _ = rag_pipeline.generate_response(
            query=user_message,
            chat_history=request.messages[:-1]  # Exclude the latest message
        )

        return ChatResponse(response=response_text)

    except Exception as e:
        raise HTTPException(status_code=500, detail="I'm having trouble processing your request. Please try again.")


@router.get("/documents")
async def list_documents() -> List[str]:
    """
    List all processed documents.

    Returns:
        List of document filenames
    """
    return get_document_list()


@router.delete("/documents/{filename}")
async def delete_document(filename: str) -> dict:
    """
    Delete a document from the data directory and update the RAG pipeline.

    Args:
        filename: Name of the file to delete

    Returns:
        Dictionary with deletion status
    """
    file_path = DATA_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"Document {filename} not found")
    
    try:
        # Delete the file
        file_path.unlink()
        
        # Reload all documents to update the RAG pipeline
        global rag_pipeline
        rag_pipeline = load_documents()
        
        return {
            "status": "success",
            "message": f"Successfully deleted {filename}"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.on_event("startup")
async def startup_event():
    """Initialize the data directory and load documents on startup."""
    global rag_pipeline
    rag_pipeline = load_documents()
