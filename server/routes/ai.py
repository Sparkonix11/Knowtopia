import os
from flask import Flask, request, jsonify
from flask_restful import Resource
from google import genai
from google.genai import types
import docx                
import PyPDF2              
from PIL import Image      
import pytesseract
from dotenv import load_dotenv

load_dotenv()

# Initialize Google Gemini API client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def extract_text_from_pdf(file_path):
  
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

def extract_text_from_docx(file_path):
    try:
        doc = docx.Document(file_path)
        fullText = [para.text for para in doc.paragraphs]
        return "\n".join(fullText)
    except Exception as e:
        print(f"Error processing DOCX {file_path}: {e}")
        return ""

def extract_text_from_image(file_path):
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Error processing image {file_path}: {e}")
        return ""

def extract_text_from_file(file_path):
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext in [".docx", ".doc"]:
        return extract_text_from_docx(file_path)
    elif ext in [".png", ".jpg", ".jpeg"]:
        return extract_text_from_image(file_path)
    else:
        return ""

def extract_topic_heading(question):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"Extract a short topic heading from this question: {question}",
        )
        topic_heading = response.text.strip()
        return topic_heading
    except Exception as e:
        print(f"Error extracting topic: {e}")
        return "Unknown Topic"

class AskResource(Resource):
    def post(self):
        data = request.get_json(force=True)
        question = data.get("question", "").strip()
        material_id = data.get("material_id")

        if not question:
            return {"error": "Question is required."}, 400

        all_text = ""
        material_name = "General Knowledge"
        courses_context = None
        
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
                
            # Get file path based on material type
            file_path = None
            file_name = material.filename
            material_name = material.name
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
                return {"error": f"File for material ID {material_id} not found at {file_path}."}, 404

            all_text = extract_text_from_file(file_path)
            print(f"Extracted text length: {len(all_text) if all_text else 0} characters")

            if not all_text.strip():
                return {"error": "No text could be extracted from the material."}, 400

            # Skip to prompt generation for material

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
            material_name = "Enrolled Courses"
        
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

        topic_heading = extract_topic_heading(question)

        try:
            # Only two possible prompts: material-specific or enrolled-courses
            if material_id and all_text.strip():
                # CASE 1: Use material context if available - STRICT material only
                prompt = f"""Question: {question} Background material from '{material_name}': {all_text} Provide hints and guidance instead of direct answers. Don't do the work for the student."""
            else:
                # CASE 2: For students with enrolled courses - STRICT courses only
                prompt = f"""Question: {question}

The student is enrolled in these courses:
{courses_context}

You are a teacher helping a student learn about their enrolled courses.
STRICTLY ENFORCE: ONLY answer if the question is directly related to these specific courses.
If the question is not about these courses, respond with EXACTLY:
"I can only answer questions related to your enrolled courses. Please ask something about {', '.join(course_names)}."

Provide hints and guidance instead of direct answers. Don't do the work for the student."""
            
            print(f"Using prompt type: {'Material-specific' if material_id else 'Enrolled-courses-only'}")
            
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                config=types.GenerateContentConfig(
                    system_instruction="You are an experienced teacher with strict instructions to stay within the defined scope.",
                ),
                contents=prompt,
            )
            answer = response.text.strip()

        except Exception as e:
            return {"error": f"Gemini API error: {str(e)}"}, 500

        # Return material name along with the answer
        return jsonify({
            "topic": topic_heading, 
            "answer": answer,
            "material_name": material_name
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
            
            # Initialize Gemini model            
            prompt = f"Question: {question}\nOptions: {', '.join(options)}\nProvide hints without revealing the answer.\n\nDo not state the correct answer explicitly. Instead, provide logical reasoning and indirect clues to help the student figure it out."
            
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                config=types.GenerateContentConfig(
                    system_instruction="You are an experienced teacher who gives hints about the correct answer without revealing it.",
                ),
                contents=prompt,
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

        # Import Material model
        from models.material import Material
        
        # Fetch material from database
        material = Material.query.get(material_id)
        if not material:
            return {"error": f"Material with ID {material_id} not found."}, 404
            
        # Get file path based on material type
        file_path = None
        file_name = material.filename
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
            return {"error": f"File for material ID {material_id} not found at {file_path}."}, 404

        all_text = extract_text_from_file(file_path)
        # Don't print the text directly to avoid encoding issues
        print(f"Extracted text length: {len(all_text) if all_text else 0} characters")

        if not all_text.strip():
            return {"error": "No text could be extracted from the material."}, 400

        try:
            # Get material name for better context
            material_name = material.name
            
            # Initialize Gemini model            
            prompt = f"Create a summary of the following material titled '{material_name}' in bullet points.\n\n{all_text}"
            
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                config=types.GenerateContentConfig(
                    system_instruction="You are a helpful AI assistant that creates concise, informative summaries.",
                ),
                contents=prompt,
            )
            answer = response.text.strip()
        except Exception as e:
            return {"error": f"Gemini API error: {str(e)}"}, 500

        topic_heading = extract_topic_heading(answer)
        
        # Return material name along with the summary
        return jsonify({
            "topic": topic_heading, 
            "summary": answer,
            "material_name": material_name
        })

