from flask import Flask, request, jsonify, session
from pymongo import MongoClient
from hashlib import sha256
import openai
from dotenv import load_dotenv
import os
import fitz  # PyMuPDF for PDFs
import docx

# Load environment variables
load_dotenv()

# OpenAI API setup
openai.api_key = os.getenv("API_KEY")  # Load the OpenAI API key from .env file

# Establish MongoDB connection using the connection string in the .env file
mongo_connection_string = os.getenv("MONGO_CONNECTION_STRING")
client = MongoClient(mongo_connection_string)
db = client['job_data']
user_collection = db['users']
job_collection = db['job_listings']

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")  # Secret key for session management

# ---------------------- User Management Functions ----------------------

def add_user(username, name, password):
    hashed_password = sha256(password.encode()).hexdigest()
    user_data = {
        'name': name,
        'username': username,
        'password': hashed_password
    }
    user_collection.insert_one(user_data)

def reset_password(username, new_password):
    hashed_new_password = sha256(new_password.encode()).hexdigest()
    result = user_collection.update_one(
        {'username': username},
        {'$set': {'password': hashed_new_password}}
    )
    return "Password reset successfully" if result.matched_count > 0 else "User not found"

def verify_user(username, password):
    hashed_password = sha256(password.encode()).hexdigest()
    user = user_collection.find_one({'username': username})
    return "Login successful" if user and user['password'] == hashed_password else "Invalid credentials"

# ---------------------- MongoDB Query Functions ----------------------

# Fetch jobs from MongoDB based on job title and required skills
def fetch_jobs(job_title, skills_list):
    query = {'job_title': {'$regex': job_title, '$options': 'i'}}
    if skills_list:
        query['required_skills'] = {'$in': skills_list}
    return list(job_collection.find(query))

# Extract text from PDF using PyMuPDF
def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Extract text from DOCX file using python-docx
def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

# ---------------------- OpenAI Resume Feedback Function ----------------------

def get_resume_feedback(resume_text, user_question):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use the correct model: gpt-4 or gpt-3.5-turbo (or mini variant if needed)
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides detailed resume feedback focusing on structure, clarity, and job market appeal."},
            {"role": "user", "content": f"Please analyze this resume and suggest improvements based on the following request: {user_question}\n\n{resume_text}"}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

# ---------------------- Flask Routes ----------------------

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    login_message = verify_user(username, password)
    if login_message == "Login successful":
        session['username'] = username
        return jsonify({"message": login_message})
    else:
        return jsonify({"message": login_message}), 400

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    name = request.json.get('name')
    password = request.json.get('password')
    if user_collection.find_one({'username': username}):
        return jsonify({"message": "Username already exists"}), 400
    add_user(username, name, password)
    return jsonify({"message": "User registered successfully"})

@app.route('/reset_password', methods=['POST'])
def reset():
    username = request.json.get('username')
    new_password = request.json.get('new_password')
    return jsonify({"message": reset_password(username, new_password)})

@app.route('/job_recommendations', methods=['GET'])
def job_recommendations():
    if 'username' not in session:
        return jsonify({"message": "Not logged in"}), 400
    
    job_title = request.args.get('job_title')
    skills_input = request.args.get('skills')
    skills_list = [skill.strip() for skill in skills_input.split(',')] if skills_input else []
    
    if job_title:
        matching_jobs = fetch_jobs(job_title, skills_list)
        return jsonify({"jobs": matching_jobs})
    else:
        return jsonify({"message": "Please provide a job title."})

@app.route('/resume_review', methods=['POST'])
def resume_review():
    if 'username' not in session:
        return jsonify({"message": "Not logged in"}), 400
    
    uploaded_resume = request.files['resume']
    if uploaded_resume:
        resume_text = ""
        if uploaded_resume.filename.endswith('.pdf'):
            resume_text = extract_text_from_pdf(uploaded_resume)
        elif uploaded_resume.filename.endswith('.docx'):
            resume_text = extract_text_from_docx(uploaded_resume)
        
        if resume_text.strip():
            user_question = request.json.get('user_question')
            feedback = get_resume_feedback(resume_text, user_question)
            return jsonify({"message": feedback})
        else:
            return jsonify({"message": "Could not extract text from the resume."}), 400
    else:
        return jsonify({"message": "Please upload a resume."})

# ---------------------- Main Flask App ----------------------

if __name__ == '__main__':
    app.run(debug=True)
