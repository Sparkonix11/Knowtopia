"""
Retrieval module for RAG system
Handles query processing and context retrieval
"""
import os
from google import genai
from typing import List, Dict, Optional, Union
from .vector_store import VectorStore

class RAGRetrieval:
    def __init__(self, api_key: str = None):
        """
        Initialize the RAG retrieval system
        
        Args:
            api_key: Google Gemini API key (defaults to GOOGLE_API_KEY env var)
        """
        # Initialize Gemini client
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=self.api_key)
        
        # Initialize vector store
        self.vector_store = VectorStore()
        self.vector_store.initialize_collection()
        
    def retrieve_context(self, query: str, k: int = 5, filter_criteria: Optional[Dict] = None) -> List[Dict]:
        """
        Retrieve relevant context for a query using vector similarity search
        
        Args:
            query: Query text to search for
            k: Number of results to return
            filter_criteria: Optional filters for the search
            
        Returns:
            List of relevant document chunks with scores
        """
        # Get similar documents from vector store
        results = self.vector_store.similarity_search(query, k=k, filter_criteria=filter_criteria)
        
        # Format results for easier handling
        formatted_results = []
        if results:
            for doc, score in results:
                formatted_results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": score
                })
        
        return formatted_results
    
    def retrieve_material_context(self, query: str, material_id: int, k: int = 5) -> str:
        """
        Retrieve context specifically from a single material
        
        Args:
            query: Query text to search for
            material_id: ID of the material to search within
            k: Number of results to return
            
        Returns:
            Concatenated context text from relevant chunks
        """
        # Set filter to only include this material
        filter_criteria = {"material_id": material_id}
        
        # Get relevant chunks
        results = self.retrieve_context(query, k=k, filter_criteria=filter_criteria)
        
        # If no results, return empty string
        if not results:
            return ""
        
        # Concatenate the retrieved context
        context_text = "\n\n".join([result["content"] for result in results])
        
        return context_text
    
    def answer_with_rag(self, query: str, material_id: Optional[int] = None, 
                        model: str = "gemini-2.0-flash", system_instruction: str = None) -> Dict:
        """
        Answer a query using RAG-enhanced LLM
        
        Args:
            query: User's question
            material_id: Optional material ID to restrict context to
            model: Gemini model to use
            system_instruction: Optional system instruction for Gemini
            
        Returns:
            Response dictionary with answer
        """
        # Initialize Gemini model
        model = genai.models.get_model(model)
        
        # Extract topic heading
        try:
            topic_model = genai.models.get_model("gemini-2.0-flash")
            topic_response = topic_model.generate_content(
                f"Extract a short topic heading from this question: {query}"
            )
            topic_heading = topic_response.text.strip()
        except Exception as e:
            print(f"Error extracting topic: {e}")
            topic_heading = "Unknown Topic"
            
        # Get relevant material name
        material_name = "General Knowledge"
        
        # Set up prompt based on whether material_id is provided
        try:
            if (material_id):
                # Retrieve context specific to this material
                context = self.retrieve_material_context(query, material_id)
                
                # Try to get material name from the first result's metadata
                filter_criteria = {"material_id": material_id}
                results = self.retrieve_context(query, k=1, filter_criteria=filter_criteria)
                if results:
                    material_name = results[0]["metadata"].get("material_name", "Material")
                
                # Material-specific prompt with RAG context
                prompt = f"""Question: {query} 
                
Background material from '{material_name}': 

{context}

Provide hints and guidance instead of direct answers. Don't do the work for the student."""
                
            else:
                # No material specified, use general RAG across all materials
                results = self.retrieve_context(query, k=5)
                
                if results:
                    # Use all retrieved contexts
                    contexts = []
                    material_names = set()
                    
                    for result in results:
                        contexts.append(result["content"])
                        material_names.add(result["metadata"].get("material_name", ""))
                    
                    context = "\n\n".join(contexts)
                    material_name = ", ".join(filter(None, material_names)) or "Knowledge Base"
                    
                    prompt = f"""Question: {query}
                    
Background information from materials ({material_name}):

{context}

Provide hints and guidance instead of direct answers. Don't do the work for the student."""
                else:
                    # No context found
                    prompt = f"""Question: {query}
                    
I don't have specific information about this in my knowledge base.
Provide hints and guidance instead of direct answers if possible."""
            
            # Configure and call Gemini
            generation_config = {
                "temperature": 0.7,
                "top_p": 0.9,
                "top_k": 40,
                "max_output_tokens": 1024,
            }
            
            safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            ]
            
            # Add system instruction if provided
            if not system_instruction:
                system_instruction = "You are an experienced teacher with strict instructions to stay within the defined scope."
            
            response = model.generate_content(
                contents=prompt,
                generation_config=generation_config,
                safety_settings=safety_settings,
                system_instruction=system_instruction,
            )
            
            answer = response.text.strip()
            
        except Exception as e:
            return {
                "error": f"Error generating response: {str(e)}",
                "topic": "Error",
                "answer": f"I encountered an error while processing your question: {str(e)}",
                "material_name": material_name
            }
        
        # Return formatted response
        return {
            "topic": topic_heading,
            "answer": answer,
            "material_name": material_name
        }
        
    def summarize_with_rag(self, material_id: int, model: str = "gemini-2.0-flash") -> Dict:
        """
        Create a summary of a material using RAG
        
        Args:
            material_id: ID of the material to summarize
            model: Gemini model to use
            
        Returns:
            Response dictionary with summary
        """
        try:
            # Retrieve all context for this material
            filter_criteria = {"material_id": material_id}
            results = self.retrieve_context("summarize this material", k=10, filter_criteria=filter_criteria)
            
            if not results:
                return {
                    "error": f"No content found for material ID {material_id}",
                    "topic": "No Content",
                    "summary": "No content available to summarize.",
                    "material_name": "Unknown Material"
                }
            
            # Get material name from metadata
            material_name = results[0]["metadata"].get("material_name", "Material")
            
            # Concatenate the content from all chunks
            content = "\n\n".join([result["content"] for result in results])
            
            # Initialize Gemini model
            model = genai.models.get_model(model)
            
            # Create prompt for summarization
            prompt = f"Create a summary of the following material titled '{material_name}' in bullet points.\n\n{content}"
            
            system_instruction = "You are a helpful AI assistant that creates concise, informative summaries."
            
            # Generate summary
            response = model.generate_content(
                contents=prompt,
                system_instruction=system_instruction,
            )
            
            summary = response.text.strip()
            
            # Extract topic heading
            topic_model = genai.models.get_model("gemini-2.0-flash")
            topic_response = topic_model.generate_content(
                f"Extract a short topic heading from this text: {summary}"
            )
            topic_heading = topic_response.text.strip()
            
            return {
                "topic": topic_heading,
                "summary": summary,
                "material_name": material_name
            }
            
        except Exception as e:
            return {
                "error": f"Error generating summary: {str(e)}",
                "topic": "Error",
                "summary": f"I encountered an error while summarizing: {str(e)}",
                "material_name": "Unknown Material"
            }