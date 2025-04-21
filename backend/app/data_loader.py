"""
Data loader module for automatically loading documents from the data directory.
"""
import os
from pathlib import Path
from typing import List
from .data_processing import DocumentProcessor
from .rag import RAGPipeline

# Constants
DATA_DIR = Path(__file__).parent.parent / "data" / "documents"

def load_documents() -> RAGPipeline:
    """
    Load all PDF documents from the data directory and initialize the RAG pipeline.
    
    Returns:
        RAGPipeline: Initialized pipeline with loaded documents
    """
    # Create data directory if it doesn't exist
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Initialize document processor
    doc_processor = DocumentProcessor()
    all_documents = []
    
    # Process all PDF files in the data directory
    for file_path in DATA_DIR.glob("*.pdf"):
        try:
            # Process each PDF file
            documents = doc_processor.process_pdf(str(file_path))
            all_documents.extend(documents)
            print(f"✓ Loaded {len(documents)} chunks from {file_path.name}")
        except Exception as e:
            print(f"Error processing {file_path.name}: {str(e)}")
    
    # Initialize RAG pipeline with all documents
    pipeline = RAGPipeline(documents=all_documents)
    
    return pipeline

def get_document_list() -> List[str]:
    """
    Get a list of all PDF documents in the data directory.
    
    Returns:
        List[str]: List of document filenames
    """
    # Create data directory if it doesn't exist
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Get all PDF files
    pdf_files = [f.name for f in DATA_DIR.glob("*.pdf")]
    return sorted(pdf_files) 