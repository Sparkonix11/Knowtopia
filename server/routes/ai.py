import os
from flask import Blueprint, request, jsonify
from flask_login import login_required
import openai
import docx
import PyPDF2
from PIL import Image
import pytesseract
from dotenv import load_dotenv

load_dotenv()

ai_api_bp = Blueprint('openai_api', __name__)

client = openai.OpenAI(api_key=os.getenv("FLASK_SECRET_KEY"))

def extract_text_from_pdf(file_path):
    text = ""
    try:
        with open(file_path, "rb") as f:
            pdf = PyPDF2.PdfReader(f)
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
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
            model="gpt-4",
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

@ai_api_bp.route('/ask', methods=['POST'])
@login_required
def ask_question():
    data = request.get_json(force=True)
    question = data.get("question", "").strip()
    folder_name = data.get("folder_name", "").strip()

    if not question or not folder_name:
        return jsonify({"error": "Both 'question' and 'folder_name' are required."}), 400

    base_dir = "documents"  # Adjust this path as needed.
    folder_path = os.path.join(base_dir, folder_name)

    if not os.path.exists(folder_path):
        return jsonify({"error": f"Folder '{folder_name}' not found."}), 404

    all_text = ""
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            file_text = extract_text_from_file(file_path)
            if file_text:
                all_text += f"\n--- Content from {filename} ---\n{file_text}\n"

    if not all_text.strip():
        return jsonify({"error": "No text could be extracted from the specified folder."}), 400

    topic_heading = extract_topic_heading(question)

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an experienced teacher helping a student understand a topic."},
                {"role": "user", "content": f"Question: {question}\n\nBackground material:\n{all_text}"},
                {"role": "system", "content": "Instead of giving a direct answer, provide hints and guidance to help the student think through the problem. Don't do the work for the student, but help her/him learn how to solve the problem on their own. "}
            ],
            max_tokens=150,
            temperature=0.7,
            n=1
        )
        answer = response.choices[0].message.content.strip()

    except Exception as e:
        return jsonify({"error": f"OpenAI API error: {str(e)}"}), 500

    return jsonify({"topic": topic_heading, "answer": answer})

@ai_api_bp.route('/question_hint', methods=['POST'])
@login_required
def question_hint():
    data = request.get_json(force=True)
    question = data.get("question", "").strip()
    options = data.get("options", [])

    if not question or not options or not isinstance(options, list):
        return jsonify({"error": "Both 'question' and a list of 'options' are required."}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4",
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
        return jsonify({"error": f"OpenAI API error: {str(e)}"}), 500

    return jsonify({"question": question, "hint": hint})