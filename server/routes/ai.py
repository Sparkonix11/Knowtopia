"""
AI features for Knowtopia using RAG with LangChain and Gemini API
"""
import os
from flask import Flask, request, jsonify
from flask_restful import Resource
from google import genai
from google.genai import types
from dotenv import load_dotenv
from services.rag import get_rag_system, init_rag_system
from services.rag.indexer import MaterialIndexer

load_dotenv()

# Initialize RAG system
rag_system = init_rag_system()

class AskResource(Resource):
    def post(self):
        data = request.get_json(force=True)
        question = data.get("question", "").strip()
        material_id = data.get("material_id")

        if not question:
            return {"error": "Question is required."}, 400
            
        # If the user is logged in and asking about a specific material, record it as a doubt
        from flask_login import current_user
        if current_user.is_authenticated and material_id:  
            try:
                # Import MaterialDoubt model
                from models.material_doubt import MaterialDoubt
                
                # Create a new doubt record
                new_doubt = MaterialDoubt(
                    material_id=material_id,
                    student_id=current_user.id,
                    doubt_text=question
                )
                
                # Add to database
                from models import db
                db.session.add(new_doubt)
                db.session.commit()
                print(f"Doubt recorded for material {material_id} by user {current_user.id}")
            except Exception as e:
                print(f"Error recording doubt: {str(e)}")
                # Continue processing even if doubt recording fails

        # CASE 1: If material_id is provided, only provide answers from that material
        if material_id:
            # Import Material model
            from models.material import Material
            
            # Fetch material from database
            material = Material.query.get(material_id)
            if not material:
                return {"error": f"Material with ID {material_id} not found."}, 404
                
            # Use RAG to answer with context from this material
            response = rag_system.answer_with_rag(
                query=question, 
                material_id=material_id,
                system_instruction="You are an experienced teacher with strict instructions to stay within the defined scope."
            )
            
            # Check for error in response
            if "error" in response:
                return {"error": response["error"]}, 500
                
            return jsonify(response)

        # CASE 2: No material_id provided - ONLY answer questions related to enrolled courses
        elif current_user.is_authenticated and not current_user.is_instructor:
            # Import enrollment model to get enrolled courses
            from models.enrollment import Enrollment
            from models.course import Course
            
            # Get all courses the student is enrolled in
            enrolled_courses = Course.query.join(Enrollment).filter(Enrollment.student_id == current_user.id).all()
            
            if not enrolled_courses:
                return jsonify({
                    "topic": "Not Enrolled", 
                    "answer": "You are not enrolled in any courses. Please enroll in courses to get help with course-related questions.",
                    "material_name": "No Courses"
                })
            
            # Create a context with the student's courses
            course_names = [course.name for course in enrolled_courses]
            course_descriptions = [f"{course.name}: {course.description}" for course in enrolled_courses]
            courses_context = "\n".join(course_descriptions)
            
            # Generate a response using the RAG system with enrolled courses
            # Since this doesn't use RAG directly, we'll use Gemini API
            try:
                # Use the same client as in the RAG system
                model = genai.models.get_model("gemini-2.0-flash")
                
                prompt = f"""Question: {question}

The student is enrolled in these courses:
{courses_context}

You are a teacher helping a student learn about their enrolled courses.
STRICTLY ENFORCE: ONLY answer if the question is directly related to these specific courses.
If the question is not about these courses, respond with EXACTLY:
"I can only answer questions related to your enrolled courses. Please ask something about {', '.join(course_names)}."

Provide hints and guidance instead of direct answers. Don't do the work for the student."""
                
                response = model.generate_content(
                    contents=prompt,
                    system_instruction="You are an experienced teacher with strict instructions to stay within the defined scope.",
                )
                answer = response.text.strip()
                
                # Extract topic heading
                topic_model = genai.models.get_model("gemini-2.0-flash")
                topic_response = topic_model.generate_content(
                    f"Extract a short topic heading from this question: {question}"
                )
                topic_heading = topic_response.text.strip()
                
                return jsonify({
                    "topic": topic_heading, 
                    "answer": answer,
                    "material_name": "Enrolled Courses"
                })
                
            except Exception as e:
                return {"error": f"Gemini API error: {str(e)}"}, 500
        
        # CASE 3: User is not a student or not authenticated - instructors handle differently
        else:
            # For instructors or unauthenticated users, return a generic response
            if current_user.is_authenticated and current_user.is_instructor:
                return jsonify({
                    "topic": "Instructor Mode", 
                    "answer": "As an instructor, you can view course materials directly or check student doubts to answer their questions.",
                    "material_name": "Instructor Guide"
                })
            else:
                return jsonify({
                    "topic": "Authentication Required", 
                    "answer": "Please log in as a student and enroll in courses to ask questions.",
                    "material_name": "Login Required"
                })

class QuestionHintResource(Resource):
    def post(self):
        data = request.get_json(force=True)
        question_id = data.get("question_id")

        if not question_id:
            return {"error": "Question ID is required."}, 400

        try:
            # Fetch question from database
            from models.question import Question
            question_data = Question.query.get(question_id)
            
            if not question_data:
                return {"error": "Question not found."}, 404
                
            question = question_data.description
            options = [question_data.option1, question_data.option2, question_data.option3, question_data.option4]
            
            # Initialize Gemini model using the same client as RAG system           
            model = genai.models.get_model("gemini-2.0-flash")
            prompt = f"Question: {question}\nOptions: {', '.join(options)}\nProvide hints without revealing the answer.\n\nDo not state the correct answer explicitly. Instead, provide logical reasoning and indirect clues to help the student figure it out."
            
            response = model.generate_content(
                contents=prompt,
                system_instruction="You are an experienced teacher who gives hints about the correct answer without revealing it.",
            )
            hint = response.text.strip()

        except Exception as e:
            return {"error": f"Error: {str(e)}"}, 500

        return jsonify({"question": question, "hint": hint})

class SummarizeResource(Resource):
    def post(self):
        data = request.get_json(force=True)
        material_id = data.get("material_id")

        if not material_id:
            return {"error": "Material ID is required."}, 400

        try:
            # Import Material model to verify material exists
            from models.material import Material
            
            # Fetch material from database
            material = Material.query.get(material_id)
            if not material:
                return {"error": f"Material with ID {material_id} not found."}, 404
            
            # Use RAG system to summarize material
            response = rag_system.summarize_with_rag(material_id=material_id)
            
            # Check for error in response
            if "error" in response:
                return {"error": response["error"]}, 500
                
            return jsonify(response)
            
        except Exception as e:
            return {"error": f"Error generating summary: {str(e)}"}, 500

class IndexMaterialResource(Resource):
    def post(self):
        """
        Index or re-index a material in the RAG system
        """
        data = request.get_json(force=True)
        material_id = data.get("material_id")
        
        if not material_id:
            return {"error": "Material ID is required."}, 400
            
        # Check if user is instructor (only instructors can trigger indexing)
        from flask_login import current_user
        if not current_user.is_authenticated or not current_user.is_instructor:
            return {"error": "Only instructors can index materials."}, 403
            
        try:
            # Import Material model
            from models.material import Material
            
            # Fetch material from database
            material = Material.query.get(material_id)
            if not material:
                return {"error": f"Material with ID {material_id} not found."}, 404
                
            # Create indexer and index the material
            indexer = MaterialIndexer()
            success = indexer.reindex_material(material_id)
            
            if success:
                return jsonify({
                    "message": f"Material '{material.name}' was successfully indexed.",
                    "material_id": material_id,
                    "material_name": material.name
                })
            else:
                return {"error": f"Failed to index material ID {material_id}."}, 500
                
        except Exception as e:
            return {"error": f"Error indexing material: {str(e)}"}, 500
            
class IndexAllMaterialsResource(Resource):
    def post(self):
        """
        Index all materials in the RAG system
        """
        # Check if user is instructor (only instructors can trigger indexing)
        from flask_login import current_user
        if not current_user.is_authenticated or not current_user.is_instructor:
            return {"error": "Only instructors can index materials."}, 403
            
        try:
            # Create indexer and index all materials
            indexer = MaterialIndexer()
            results = indexer.index_all_materials()
            
            return jsonify({
                "message": f"Indexing complete. {results['success']}/{results['total']} materials indexed successfully.",
                "results": results
            })
                
        except Exception as e:
            return {"error": f"Error indexing materials: {str(e)}"}, 500

