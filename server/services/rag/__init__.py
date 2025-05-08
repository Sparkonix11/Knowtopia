"""
RAG (Retrieval Augmented Generation) system for Knowtopia
Provides improved handling of PDFs and video transcripts through vector storage
"""

from .document_processor import DocumentProcessor
from .vector_store import VectorStore
from .retrieval import RAGRetrieval

__all__ = ['DocumentProcessor', 'VectorStore', 'RAGRetrieval', 'init_rag_system', 'get_rag_system']

# Singleton instance
_rag_system = None

def init_rag_system():
    """
    Initialize the RAG system
    
    Returns:
        An instance of RAGRetrieval
    """
    global _rag_system
    if _rag_system is None:
        _rag_system = RAGRetrieval()
    return _rag_system
    
def get_rag_system():
    """
    Get the RAG system instance, initializing if necessary
    
    Returns:
        An instance of RAGRetrieval
    """
    global _rag_system
    if _rag_system is None:
        _rag_system = init_rag_system()
    return _rag_system