from flask import Flask, request, jsonify
from pymongo import MongoClient
from hashlib import sha256

# Establish a connection to MongoDB (cloud-based)
client = MongoClient("mongodb+srv://Yateeka:hacklytics@hackalytics.warwu.mongodb.net/")
db = client['job_data']  # Database name
user_collection = db['users']  # Collection for user data

# Initialize Flask app
app = Flask(__name__)

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
    return jsonify({"message": verify_user(username, password)})

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

if __name__ == '__main__':
    app.run(debug=True)
