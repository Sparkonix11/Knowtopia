"""
Document processing module for RAG system
Handles extraction and processing of text from PDFs and video transcripts
"""
import os
import PyPDF2
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Dict, Optional, Union

class DocumentProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the document processor with configurable chunking parameters
        
        Args:
            chunk_size: The size of each text chunk for embedding
            chunk_overlap: The overlap between chunks to maintain context
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """
        Extract text from a PDF file
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Extracted text as a string
        """
        text = ""
        try:
            with open(file_path, "rb") as f:
                pdf = PyPDF2.PdfReader(f)
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        # Clean the text of problematic Unicode characters
                        page_text = ''.join(char if ord(char) < 0xF000 else ' ' for char in page_text)
                        text += page_text + "\n"
        except Exception as e:
            print(f"Error processing PDF {file_path}: {e}")
        return text
    
    def extract_text_from_transcript(self, transcript_path: str) -> str:
        """
        Extract text from a video transcript file
        
        Args:
            transcript_path: Path to the transcript file
            
        Returns:
            Extracted text as a string
        """
        try:
            with open(transcript_path, 'r', encoding='utf-8') as file:
                text = file.read()
            return text
        except Exception as e:
            print(f"Error reading transcript file {transcript_path}: {e}")
            return ""
    
    def process_document(self, file_path: str) -> List[Dict[str, str]]:
        """
        Process a document, extracting text and splitting into chunks with metadata
        
        Args:
            file_path: Path to the document file
            
        Returns:
            List of document chunks with metadata
        """
        # Get file extension
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        # Extract text based on file type
        if ext == ".pdf":
            text = self.extract_text_from_pdf(file_path)
        elif ext == ".txt":  # Assuming transcripts are stored as .txt
            text = self.extract_text_from_transcript(file_path)
        else:
            return []
        
        if not text.strip():
            return []
        
        # Split text into chunks
        chunks = self.text_splitter.create_documents([text])
        
        # Prepare document chunks with metadata
        doc_chunks = []
        for i, chunk in enumerate(chunks):
            doc_chunks.append({
                "content": chunk.page_content,
                "metadata": {
                    "source": file_path,
                    "chunk_id": i,
                    "file_type": ext,
                }
            })
        
        return doc_chunks
    
    def process_material(self, material) -> List[Dict[str, str]]:
        """
        Process a material from the database, extracting text from its associated file
        
        Args:
            material: Material object from the database
            
        Returns:
            List of document chunks with metadata
        """
        file_path = None
        file_name = material.filename
        material_name = material.name
        material_id = material.id
        _, ext = os.path.splitext(file_name)
        ext = ext.lower()
        
        # For videos, use transcript if available
        if ext == ".mp4" and material.transcript_path:
            # Convert relative path to absolute path
            transcript_path = material.transcript_path.lstrip('/')
            file_path = os.path.join(os.getcwd(), transcript_path)
        else:
            # For PDFs and other files, use the material file path
            material_path = material.file_path.lstrip('/')
            file_path = os.path.join(os.getcwd(), material_path)
        
        if not os.path.exists(file_path):
            print(f"File for material ID {material_id} not found at {file_path}.")
            return []
            
        # Process the document and add additional metadata
        doc_chunks = self.process_document(file_path)
        
        # Add material-specific metadata to all chunks
        for chunk in doc_chunks:
            chunk["metadata"].update({
                "material_id": material_id,
                "material_name": material_name,
            })
            
        return doc_chunks