"""
Document processing module for the Mangrove Chatbot.
Handles PDF loading, text extraction, and chunking.
"""
import os
from typing import List
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from .models import Document


class DocumentProcessor:
    """
    Handles document processing operations including loading PDFs and chunking text.
    """
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the document processor.

        Args:
            chunk_size: The size of text chunks to create
            chunk_overlap: The overlap between consecutive chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )

    def load_pdf(self, file_path: str) -> str:
        """
        Load and extract text from a PDF file.

        Args:
            file_path: Path to the PDF file

        Returns:
            Extracted text from the PDF
        
        Raises:
            FileNotFoundError: If the PDF file doesn't exist
            Exception: For other PDF processing errors
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found: {file_path}")

        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            raise Exception(f"Error processing PDF file: {str(e)}")

    def create_chunks(self, text: str, metadata: dict = None) -> List[Document]:
        """
        Split text into chunks and create Document objects.

        Args:
            text: The text to split into chunks
            metadata: Optional metadata to attach to each chunk

        Returns:
            List of Document objects containing the chunks
        """
        if metadata is None:
            metadata = {}

        # Split text into chunks
        chunks = self.text_splitter.split_text(text)

        # Create Document objects for each chunk
        documents = []
        for i, chunk in enumerate(chunks):
            chunk_metadata = {
                "chunk_index": i,
                **metadata
            }
            documents.append(Document(
                content=chunk,
                metadata=chunk_metadata
            ))

        return documents

    def process_pdf(self, file_path: str) -> List[Document]:
        """
        Process a PDF file: load it and split into chunks.

        Args:
            file_path: Path to the PDF file

        Returns:
            List of Document objects containing the chunks
        """
        # Extract metadata from file path
        metadata = {
            "source": os.path.basename(file_path),
            "file_path": file_path
        }

        # Load and process the PDF
        text = self.load_pdf(file_path)
        return self.create_chunks(text, metadata)
