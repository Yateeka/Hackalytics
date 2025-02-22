from flask import Flask, request, jsonify, session
from pymongo import MongoClient
import bcrypt
import openai
from dotenv import load_dotenv
import os
import fitz  # PyMuPDF for PDFs
import docx

# Load environment variables
load_dotenv()

# OpenAI API setup
openai.api_key = os.getenv("API_KEY")

# Establish MongoDB connection
mongo_connection_string = os.getenv("MONGO_CONNECTION_STRING")
client = MongoClient(mongo_connection_string)
db = client['job_data']
user_collection = db['users']
job_collection = db['job_listings']

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")  # Secret key for session management

# ---------------------- User Management Functions ----------------------

def hash_password(password):
    # Hash the password with bcrypt
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)

def add_user(username, name, password):
    hashed_password = hash_password(password)
    user_data = {
        'name': name,
        'username': username,
        'password': hashed_password
    }
    user_collection.insert_one(user_data)

def reset_password(username, new_password):
    hashed_new_password = hash_password(new_password)
    result = user_collection.update_one(
        {'username': username},
        {'$set': {'password': hashed_new_password}}
    )
    return "Password reset successfully" if result.matched_count > 0 else "User not found"

def verify_user(username, password):
    user = user_collection.find_one({'username': username})
    if user and verify_password(user['password'], password):
        return "Login successful"
    return "Invalid credentials"

# ---------------------- MongoDB Query Functions ----------------------

# Fetch jobs from MongoDB based on job title and employment type
def fetch_jobs(job_title, employment_type, page=1, per_page=10):
    query = {'job_title': {'$regex': job_title, '$options': 'i'}}  # Case-insensitive match
    if employment_type:
        query['employment_type'] = {'$regex': employment_type, '$options': 'i'}  # Filter by employment type
    
    # Add pagination by limiting the number of results
    jobs = job_collection.find(query).skip((page - 1) * per_page).limit(per_page)
    return list(jobs)

def fetch_unique_job_titles():
    try:
        # Fetch distinct job titles from MongoDB
        job_titles = job_collection.distinct("job_title")
        return sorted(job_titles)  # Sort alphabetically
    except Exception as e:
        print(f"Error fetching job titles: {e}")
        return []

def fetch_unique_employment_type():
    try:
        # Fetch distinct employment type from MongoDB
        employment_type = job_collection.distinct("employment_type")
        return sorted(employment_type)  # Sort alphabetically
    except Exception as e:
        print(f"Error fetching employment types: {e}")
        return []

# ---------------------- Resume Text Extraction Functions ----------------------

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
        model="gpt-4",
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
    employment_type = request.args.get('employment_type')

    if not job_title:
        return jsonify({"message": "Please provide a job title."}), 400

    page = int(request.args.get('page', 1))  # Default page is 1
    matching_jobs = fetch_jobs(job_title, employment_type, page)
    return jsonify({"jobs": matching_jobs})

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
