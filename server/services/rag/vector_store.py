"""
Vector store module for RAG system
Manages document embeddings and vector storage using ChromaDB
"""
import os
import chromadb
from chromadb.config import Settings
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from typing import List, Dict, Optional, Union

class VectorStore:
    def __init__(self, persist_directory: str = "server/services/rag/chroma_db"):
        """
        Initialize the vector store with a persistent directory
        
        Args:
            persist_directory: Directory where ChromaDB will persist data
        """
        self.persist_directory = persist_directory
        
        # Create directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)
        
        # Use Sentence Transformers for embeddings
        self.embedding_model = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.db = None
        
    def initialize_collection(self, collection_name: str = "knowtopia_materials"):
        """
        Initialize or load a collection in the vector store
        
        Args:
            collection_name: Name of the collection to create or load
        """
        self.db = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embedding_model,
            collection_name=collection_name
        )
        print(f"Vector DB initialized at {self.persist_directory}")
        return self.db
    
    def add_documents(self, documents: List[Dict[str, Union[str, Dict]]]):
        """
        Add documents to the vector store
        
        Args:
            documents: List of document dictionaries with content and metadata
        """
        if not self.db:
            self.initialize_collection()
        
        # Extract contents and metadata for Chroma
        texts = [doc["content"] for doc in documents]
        metadatas = [doc["metadata"] for doc in documents]
        
        # Generate ids from metadata
        ids = [f"{meta['material_id']}_{meta['chunk_id']}" for meta in metadatas]
        
        # Add to the collection
        self.db.add_texts(texts=texts, metadatas=metadatas, ids=ids)
        print(f"Added {len(documents)} document chunks to the vector store")
        
    def add_material(self, material_docs: List[Dict[str, Union[str, Dict]]]):
        """
        Add or update material documents in the vector store
        
        Args:
            material_docs: List of document chunks from a material
        """
        if not material_docs:
            return
        
        # Remove any existing documents for this material to avoid duplicates
        material_id = material_docs[0]["metadata"]["material_id"]
        self.delete_material(material_id)
        
        # Add the new document chunks
        self.add_documents(material_docs)
        
    def delete_material(self, material_id):
        """
        Delete all document chunks for a specific material
        
        Args:
            material_id: ID of the material to remove
        """
        if not self.db:
            self.initialize_collection()
            
        # Get all documents in the collection
        all_docs = self.db.get()
        if not all_docs or not all_docs.get('ids'):
            return
            
        # Find documents for this material
        to_delete = []
        for i, meta in enumerate(all_docs.get('metadatas', [])):
            if meta.get('material_id') == material_id:
                to_delete.append(all_docs['ids'][i])
                
        # Delete matching documents
        if to_delete:
            self.db._collection.delete(to_delete)
            print(f"Deleted {len(to_delete)} document chunks for material {material_id}")
    
    def similarity_search(self, query: str, k: int = 5, filter_criteria: Optional[Dict] = None):
        """
        Perform a similarity search for a query
        
        Args:
            query: Query text to search for
            k: Number of results to return
            filter_criteria: Optional filters for the search
            
        Returns:
            List of document chunks with relevance scores
        """
        if not self.db:
            self.initialize_collection()
            
        # Perform search with optional filtering
        results = self.db.similarity_search_with_relevance_scores(
            query, k=k, filter=filter_criteria
        )
        
        return results