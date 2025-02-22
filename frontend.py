import streamlit as st
import requests

# Backend URL (Flask app URL running locally or on a server)
BACKEND_URL = 'http://127.0.0.1:5000/'  # Change to the URL of your Flask app

# Function to handle user login
def login(username, password):
    response = requests.post(f"{BACKEND_URL}login", json={"username": username, "password": password})
    return response.json()

# Function to handle user registration (sign up)
def register(username, name, password):
    response = requests.post(f"{BACKEND_URL}register", json={"username": username, "name": name, "password": password})
    return response.json()

# Function to handle password reset
def reset_password(username, new_password):
    response = requests.post(f"{BACKEND_URL}reset_password", json={"username": username, "new_password": new_password})
    return response.json()

# Streamlit Custom CSS Styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Istok+Web:ital,wght@0,400;0,700;1,400;1,700&display=swap');
        
        html, body {
            margin: 0;
            font-family: "Istok Web", sans-serif;
            background-color: #f8d7da;
            color: #fb6f92;
            height: 100%;
            text-align: center;
        }

        .modal-content {
            background: transparent;
            color: #fb6f92;
            backdrop-filter: blur(10px);
            border-radius: 12px;
            padding: 30px 40px;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
            margin: 20px;
        }

        .btn {
            width: 100%;
            height: 45px;
            background: #fb6f92;
            border: none;
            border-radius: 40px;
            color: white;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: 0.3s;
            box-shadow: 0 0 10px #f8d7da;
        }

        .btn:hover {
            background: #d45b79;
        }

        .input-box input {
            width: 100%;
            height: 50px;
            background: transparent;
            border: 2px solid #fb6f92;
            border-radius: 40px;
            font-size: 16px;
            color: #fb6f92;
            padding: 10px;
        }

        .login-btn {
            padding: 10px 15px;
            border: none;
            background-color: #fb6f92;
            color: white;
            cursor: pointer;
            font-size: 1rem;
            border-radius: 5px;
            transition: 0.3s;
        }

        .login-btn:hover {
            background-color: #d45b79;
        }

        .register-link a {
            color: #fb6f92;
            text-decoration: none;
            font-weight: 600;
        }

        .register-link a:hover {
            text-decoration: underline;
        }
    </style>
""", unsafe_allow_html=True)

# Streamlit UI for Pages

def login_page():
    # Login Form
    st.subheader('Login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    login_button = st.button('Login')
    if login_button:
        if username and password:
            login_response = login(username, password)
            st.success(login_response['message'])
        else:
            st.error('Please fill in both fields.')

    # Navigation to signup page
    signup_button = st.button("Sign Up")
    if signup_button:
        st.session_state.page = "signup"

    # Navigation to reset password page
    reset_button = st.button("Forgot Password?")
    if reset_button:
        st.session_state.page = "reset_password"

def signup_page():
    # Sign Up Form
    st.subheader('Sign Up')
    username_signup = st.text_input('Username (Sign Up)')
    name_signup = st.text_input('Full Name')
    password_signup = st.text_input('Password (Sign Up)', type='password')

    signup_button = st.button('Sign Up')
    if signup_button:
        if username_signup and name_signup and password_signup:
            register_response = register(username_signup, name_signup, password_signup)
            if register_response['message'] == "User registered successfully":
                st.success('User registered successfully! Please log in.')
                st.session_state.page = "login"
            else:
                st.error(register_response['message'])
        else:
            st.error('Please fill in all fields.')

    # Back to Login Page
    back_button = st.button("Back to Login")
    if back_button:
        st.session_state.page = "login"

def reset_password_page():
    # Reset Password Form
    st.subheader('Reset Password')
    username_reset = st.text_input('Username (for password reset)')
    new_password = st.text_input('New Password', type='password')

    reset_button = st.button('Reset Password')
    if reset_button:
        if username_reset and new_password:
            reset_response = reset_password(username_reset, new_password)
            st.success(reset_response['message'])
        else:
            st.error('Please fill in both fields.')

    # Back to Login Page
    back_button = st.button("Back to Login")
    if back_button:
        st.session_state.page = "login"


# Set default page to login
if 'page' not in st.session_state:
    st.session_state.page = "login"

# Show the correct page based on session state
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "signup":
    signup_page()
elif st.session_state.page == "reset_password":
    reset_password_page()
