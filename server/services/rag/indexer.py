"""
Material indexer for the RAG system
Processes PDFs and video transcripts and adds them to the vector store
"""

from typing import List, Optional, Union
from .document_processor import DocumentProcessor
from .vector_store import VectorStore
from models.material import Material

class MaterialIndexer:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the material indexer
        
        Args:
            chunk_size: The size of each text chunk for embedding
            chunk_overlap: The overlap between chunks to maintain context
        """
        self.document_processor = DocumentProcessor(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        self.vector_store = VectorStore()
        self.vector_store.initialize_collection()
        
    def index_material(self, material: Material) -> bool:
        """
        Process and index a single material
        
        Args:
            material: Material object to process
            
        Returns:
            True if indexing was successful, False otherwise
        """
        try:
            # Process material to get document chunks
            doc_chunks = self.document_processor.process_material(material)
            
            if not doc_chunks:
                print(f"No content extracted from material: {material.name} (ID: {material.id})")
                return False
                
            # Add to vector store
            self.vector_store.add_material(doc_chunks)
            print(f"Successfully indexed material: {material.name} (ID: {material.id})")
            return True
            
        except Exception as e:
            print(f"Error indexing material ID {material.id}: {str(e)}")
            return False
            
    def index_materials(self, materials: List[Material]) -> dict:
        """
        Process and index multiple materials
        
        Args:
            materials: List of Material objects to process
            
        Returns:
            Dictionary with success and failure counts
        """
        results = {"success": 0, "failed": 0, "total": len(materials)}
        
        for material in materials:
            success = self.index_material(material)
            if success:
                results["success"] += 1
            else:
                results["failed"] += 1
                
        print(f"Indexing complete. {results['success']}/{results['total']} materials indexed successfully.")
        return results
        
    def index_all_materials(self) -> dict:
        """
        Index all materials in the database
        
        Returns:
            Dictionary with success and failure counts
        """
        try:
            # Get all materials from the database
            materials = Material.query.all()
            return self.index_materials(materials)
        except Exception as e:
            print(f"Error accessing database: {str(e)}")
            return {"success": 0, "failed": 0, "total": 0, "error": str(e)}
            
    def reindex_material(self, material_id: int) -> bool:
        """
        Reindex a specific material
        
        Args:
            material_id: ID of the material to reindex
            
        Returns:
            True if reindexing was successful, False otherwise
        """
        try:
            # Get the material from the database
            material = Material.query.get(material_id)
            if not material:
                print(f"Material ID {material_id} not found.")
                return False
                
            # Remove from vector store first
            self.vector_store.delete_material(material_id)
            
            # Then reindex
            return self.index_material(material)
            
        except Exception as e:
            print(f"Error reindexing material ID {material_id}: {str(e)}")
            return False