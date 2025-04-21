"""
RAG (Retrieval Augmented Generation) pipeline for the Mangrove Chatbot.
Handles document embedding, retrieval, and response generation.

This module implements a complete RAG pipeline with the following components:
1. Document Embedding: Using Cohere's embed-multilingual-v3.0 model
2. Similarity Search: Using cosine similarity to find relevant documents
3. Reranking: Using Cohere's rerank-multilingual-v2.0 model
4. Response Generation: Using Cohere's command model

The pipeline follows these steps:
1. Documents are embedded when loaded
2. When a query is received, it's embedded and similar documents are found
3. Top documents are reranked for better relevance
4. Context from relevant documents is used to generate a response
"""
import os
from typing import List, Tuple, Union, Optional
import numpy as np
from tenacity import retry, stop_after_attempt, wait_exponential
from app.models import Document, Message
from app.config import cohere_client

# Constants for API configuration
EMBED_BATCH_SIZE = 96  # Cohere's recommended batch size for optimal performance
EMBED_MODEL = 'embed-multilingual-v3.0'  # Multilingual embedding model for better language support
RERANK_MODEL = 'rerank-multilingual-v2.0'  # Advanced reranking model for improved relevance
CHAT_MODEL = 'command'  # Cohere's chat model for response generation

class RAGPipeline:
    """
    Implements the RAG pipeline for the chatbot.
    """
    def __init__(self, documents: List[Document] = None):
        """
        Initialize the RAG pipeline.

        Args:
            documents: List of Document objects to use in the pipeline
        """
        self.documents = documents or []
        self._ensure_embeddings()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def _get_embedding(self, text: Union[str, List[str]]) -> Union[np.ndarray, List[np.ndarray]]:
        """
        Get embeddings for text using Cohere's embed model.

        Args:
            text: Text or list of texts to embed

        Returns:
            Vector embedding(s) of the text(s)
        """
        # Convert single text to list for consistent handling
        texts = [text] if isinstance(text, str) else text
        
        try:
            # Get embeddings from Cohere
            response = cohere_client.embed(
                texts=texts,
                model=EMBED_MODEL,
                input_type='search_query'
            )
            
            # Convert to numpy arrays for easier manipulation
            embeddings = [np.array(emb) for emb in response.embeddings]
            
            # Return single embedding for single text, list of embeddings for multiple texts
            return embeddings[0] if isinstance(text, str) else embeddings
        except Exception as e:
            print(f"Embedding error: {str(e)}")
            raise

    def _ensure_embeddings(self):
        """
        Ensure all documents have embeddings, using batched requests for efficiency.
        """
        docs_without_embeddings = [doc for doc in self.documents if doc.embedding is None]
        
        # Process in batches
        for i in range(0, len(docs_without_embeddings), EMBED_BATCH_SIZE):
            batch = docs_without_embeddings[i:i + EMBED_BATCH_SIZE]
            texts = [doc.content for doc in batch]
            embeddings = self._get_embedding(texts)
            
            # Assign embeddings back to documents
            for doc, embedding in zip(batch, embeddings):
                doc.embedding = embedding

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """
        Calculate cosine similarity between two vectors.
        
        Args:
            a (np.ndarray): First vector
            b (np.ndarray): Second vector
            
        Returns:
            float: Cosine similarity score
        """
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def _rerank(self, query: str, documents: List[Document], top_k: int = 3) -> List[Document]:
        """
        Rerank documents using Cohere's rerank endpoint.
        
        Args:
            query (str): The search query
            documents (List[Document]): List of documents to rerank
            top_k (int): Number of documents to return
            
        Returns:
            List[Document]: Reranked documents
        """
        if not documents:
            return []
        
        try:
            rerank_docs = [doc.content for doc in documents]
            results = cohere_client.rerank(
                query=query,
                documents=rerank_docs,
                top_n=top_k,
                model=RERANK_MODEL
            )
            
            # Create a mapping of content to original Document objects
            doc_map = {doc.content: doc for doc in documents}
            
            # Return reranked documents in order
            reranked = []
            for result in results:
                doc = doc_map[result.document['text']]
                reranked.append(doc)
            
            return reranked
        except Exception as e:
            print(f"Rerank error: {str(e)}")
            # If reranking fails, return documents in original order
            return documents[:top_k]

    def retrieve(self, query: str, top_k: int = 5) -> List[Document]:
        """
        Retrieve relevant documents for a query.

        Args:
            query: User query
            top_k: Number of documents to retrieve

        Returns:
            List of relevant documents
        """
        # Get query embedding
        query_embedding = self._get_embedding(query)

        # Calculate similarities
        similarities = [
            (doc, self._cosine_similarity(query_embedding, doc.embedding))
            for doc in self.documents
        ]

        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        top_docs = [doc for doc, _ in similarities[:top_k]]

        # Rerank the top documents
        return self._rerank(query, top_docs)

    def _create_prompt(self, query: str, context_docs: List[Document], chat_history: List[Message]) -> str:
        """
        Create a prompt for the language model.

        Args:
            query: User query
            context_docs: Retrieved relevant documents
            chat_history: Previous chat messages

        Returns:
            Formatted prompt string
        """
        # Format context with source information
        context_sections = []
        for i, doc in enumerate(context_docs, 1):
            source = doc.metadata.get("source", "Unknown Source")
            context_sections.append(f"[Document {i} from {source}]:\n{doc.content}")
        context = "\n\n".join(context_sections)

        # Format chat history
        history = "\n".join([f"{msg.role}: {msg.content}" for msg in chat_history[-5:]])  # Last 5 messages

        # Create the prompt with more explicit instructions
        prompt = f"""You are a helpful AI assistant. Answer the user's question based on the provided context documents. Follow these rules:

1. Use ONLY the information from the provided context documents to answer the question
2. If the context doesn't contain enough information to fully answer the question, say so clearly
3. Do not make up or infer information that isn't in the context
4. If you quote or paraphrase from the context, mention which document it came from
5. If the question cannot be answered from the context, say "I cannot find information about this in the provided documents"

Context Documents:
{context}

Previous Conversation:
{history}

Current Question: {query}

Answer: """

        return prompt

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate_response(self, query: str, chat_history: List[Message] = None) -> Tuple[str, List[str]]:
        """
        Generate a response using the RAG pipeline.

        Args:
            query: User query
            chat_history: List of previous messages

        Returns:
            Tuple of (generated response, list of source documents)
        """
        try:
            # Initialize chat history if None
            chat_history = chat_history or []

            # Find relevant documents
            sources = []
            relevant_docs = []
            if self.documents:
                # Get relevant documents using the retrieve method which handles embedding and reranking
                relevant_docs = self.retrieve(query, top_k=3)
                sources = [doc.metadata.get("source", "Unknown") for doc in relevant_docs]

            # Format chat history for Cohere
            formatted_history = []
            for msg in chat_history:
                # Convert roles to match Cohere's expected values
                cohere_role = "User" if msg.role == "user" else "Chatbot"
                formatted_history.append({
                    "role": cohere_role,
                    "message": msg.content
                })

            # Create the prompt with context if we have relevant documents
            if relevant_docs:
                # Use the _create_prompt method to format the prompt with context
                prompt = self._create_prompt(query, relevant_docs, chat_history)
                
                # Generate response using Cohere with context
                response = cohere_client.chat(
                    message=prompt,
                    model=CHAT_MODEL,
                    chat_history=formatted_history,
                    temperature=0.7,
                    # Don't use web search when we have relevant documents
                    connectors=None
                )
            else:
                # If no relevant documents found, use web search as fallback
                response = cohere_client.chat(
                    message=query,
                    model=CHAT_MODEL,
                    chat_history=formatted_history,
                    temperature=0.7,
                    connectors=[{"id": "web-search"}]
                )

            return response.text, sources

        except Exception as e:
            print(f"Pipeline error: {str(e)}")
            raise
