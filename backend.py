from flask import Flask, request, jsonify, session, redirect, url_for
from pymongo import MongoClient
from hashlib import sha256

# Establish a connection to MongoDB (cloud-based)
client = MongoClient("mongodb+srv://Yateeka:hacklytics@hackalytics.warwu.mongodb.net/")
db = client['job_data']  # Database name
user_collection = db['users']  # Collection for user data

# Initialize Flask app
app = Flask(__name__)

# Secret key for session management
app.secret_key = "your_secret_key_here"

# Function to add a new user
def add_user(username, name, password):
    hashed_password = sha256(password.encode()).hexdigest()
    user_data = {
        'name': name,
        'username': username,
        'password': hashed_password
    }
    user_collection.insert_one(user_data)  # Insert user into MongoDB

# Function to reset a user's password
def reset_password(username, new_password):
    hashed_new_password = sha256(new_password.encode()).hexdigest()
    result = user_collection.update_one(
        {'username': username},
        {'$set': {'password': hashed_new_password}}
    )
    if result.matched_count > 0:
        return "Password reset successfully"
    else:
        return "User not found"

# Function to verify a user's login
def verify_user(username, password):
    hashed_password = sha256(password.encode()).hexdigest()
    user = user_collection.find_one({'username': username})
    if user and user['password'] == hashed_password:
        return "Login successful"
    else:
        return "Invalid credentials"

# Endpoint for login
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    login_message = verify_user(username, password)
    
    if login_message == "Login successful":
        session['username'] = username  # Save username in session
        return jsonify({"message": login_message})
    else:
        return jsonify({"message": login_message}), 400

# Endpoint for registration (signup)
@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    name = request.json.get('name')
    password = request.json.get('password')
    
    # Check if the username already exists
    if user_collection.find_one({'username': username}):
        return jsonify({"message": "Username already exists"}), 400
    
    add_user(username, name, password)
    return jsonify({"message": "User registered successfully"})

# Endpoint for password reset
@app.route('/reset_password', methods=['POST'])
def reset():
    username = request.json.get('username')
    new_password = request.json.get('new_password')
    return jsonify({"message": reset_password(username, new_password)})

# Protected route for accessing job recommendations (accessible only after login)
@app.route('/job_recommendations', methods=['GET'])
def job_recommendations():
    if 'username' not in session:
        return redirect(url_for('login_page'))  # Redirect to login if not logged in
    
    job_title = request.args.get('job_title')
    if job_title:
        # Placeholder for job recommendations (you can add a real API later)
        return jsonify({
            "jobs": [
                "Job 1: Data Scientist at Company XYZ",
                "Job 2: Data Scientist at Company ABC",
                "Job 3: Junior Data Scientist at Company DEF"
            ]
        })
    else:
        return jsonify({"message": "Please provide a job title."})

# Career Path Analysis (accessible only after login)
@app.route('/career_path_analysis', methods=['GET'])
def career_path_analysis():
    if 'username' not in session:
        return redirect(url_for('login_page'))  # Redirect to login if not logged in
    
    current_job = request.args.get('current_job')
    if current_job:
        # Placeholder for career path analysis (you can integrate AI or a dataset for better insights)
        return jsonify({
            "career_path": [
                "Suggested Career Path 1: Senior Developer -> Lead Developer -> CTO",
                "Suggested Career Path 2: Junior Developer -> Backend Developer -> Software Architect"
            ]
        })
    else:
        return jsonify({"message": "Please provide your current job title."})

# Resume Review (accessible only after login)
@app.route('/resume_review', methods=['POST'])
def resume_review():
    if 'username' not in session:
        return redirect(url_for('login_page'))  # Redirect to login if not logged in
    
    uploaded_resume = request.files['resume']
    if uploaded_resume:
        # Placeholder for resume review (you can later integrate AI models for feedback)
        return jsonify({"message": "Your resume looks good! Make sure to improve your skills in Python and Machine Learning."})
    else:
        return jsonify({"message": "Please upload a resume."})

# Logout route
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)  # Remove username from session
    return jsonify({"message": "Logged out successfully"})

# Forgot Password (Reset Password directly)
@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    username = request.json.get('username')
    new_password = request.json.get('new_password')
    
    if username and new_password:
        reset_response = reset_password(username, new_password)
        return jsonify({"message": reset_response})
    else:
        return jsonify({"message": "Please provide both username and new password."}), 400

# Set default page to login
if __name__ == '__main__':
    app.run(debug=True)
