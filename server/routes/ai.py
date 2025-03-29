import os
from flask import Flask, request, jsonify
from flask_restful import Resource
import openai

import docx                
import PyPDF2              
from PIL import Image      
import pytesseract
from dotenv import load_dotenv

load_dotenv()


client = openai.OpenAI(api_key= os.getenv("OPENAI_API_KEY"))

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
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI trained to summarize questions into concise topic headings."},
                {"role": "user", "content": f"Extract a short topic heading from this question: {question}"}
            ],
            max_tokens=10,
            temperature=0.5
        )
        topic_heading = response.choices[0].message.content.strip()
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

        # If material_id is provided, fetch context from the material
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
            # Don't print the text directly to avoid encoding issues
            print(f"Extracted text length: {len(all_text) if all_text else 0} characters")

            if not all_text.strip():
                return {"error": "No text could be extracted from the material."}, 400

        # If no material_id was provided or if we're here after successfully extracting text
        topic_heading = extract_topic_heading(question)

        try:
            # Prepare system message based on whether we have material context or not
            system_message = "You are an experienced teacher helping a student understand a topic."
            
            # Prepare user message based on whether we have material context
            if all_text.strip():
                user_message = f"Question: {question}\n\nBackground material from '{material_name}':\n{all_text}"
            else:
                # No context available, answer generally
                user_message = f"Question: {question}"
                
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message},
                    {"role": "system", "content": "Instead of giving a direct answer, provide hints and guidance to help the student think through the problem. Don't do the work for the student, but help her/him learn how to solve the problem on their own."}
                ],
                max_tokens=150,
                temperature=0.7,
                n=1
            )
            answer = response.choices[0].message.content.strip()

        except Exception as e:
            return {"error": f"OpenAI API error: {str(e)}"}, 500

        # Return material name along with the answer, similar to SummarizeResource
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
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an experienced teacher who gives hints about the correct answer without revealing it."},
                    {"role": "user", "content": f"Question: {question}\nOptions: {', '.join(options)}\nProvide hints without revealing the answer."},
                    {"role": "system", "content": "Do not state the correct answer explicitly. Instead, provide logical reasoning and indirect clues to help the student figure it out."}
                ],
                max_tokens=100,
                temperature=0.7
            )
            hint = response.choices[0].message.content.strip()

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
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant that creates concise, informative summaries."},
                    {"role": "user", "content": f"Create a summary of the following material titled '{material_name}' in bullet points.\n\n{all_text}"},
                ],
                max_tokens=300,
                temperature=0.7,
                n=1
            )
            answer = response.choices[0].message.content.strip()
        except Exception as e:
            return {"error": f"OpenAI API error: {str(e)}"}, 500

        topic_heading = extract_topic_heading(answer)
        
        # Return material name along with the summary
        return jsonify({
            "topic": topic_heading, 
            "summary": answer,
            "material_name": material_name
        })

