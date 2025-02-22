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

# Function to load the external CSS file
def load_css(css_file):
    with open(css_file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load custom CSS
load_css('/Users/yateekagoyal/Desktop/Hackalytics/Hackalytics/styles.css')  # Ensure the path to your CSS file is correct

# Sidebar Navigation
def sidebar():
    st.sidebar.title('Career Coaching Platform')
    
    # Display different options depending on whether the user is logged in
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        options = ['Login', 'Sign Up']
    else:
        options = ['Job Recommendations', 'Career Path Analysis', 'Resume Review', 'Logout']
    
    choice = st.sidebar.radio('Select Option', options)
    
    return choice

# Job Recommendations UI
def job_recommendations():
    st.title('Job Recommendations')
    st.write('Enter a job title to find the best job opportunities:')
    
    job_title = st.text_input('Job Title', placeholder='e.g., Data Scientist')
    if job_title:
        st.write(f"Searching for jobs related to: {job_title}")
        # Placeholder for job recommendations (you can add a real API later)
        st.write("Job 1: Data Scientist at Company XYZ")
        st.write("Job 2: Data Scientist at Company ABC")
        st.write("Job 3: Junior Data Scientist at Company DEF")

# Career Path Analysis UI
def career_path_analysis():
    st.title('Career Path Analysis')
    st.write("Enter your current job title to receive career path insights:")
    
    current_job = st.text_input('Current Job Title', placeholder='e.g., Junior Developer')
    if current_job:
        st.write(f"Analyzing career paths for: {current_job}")
        # Placeholder for career path analysis (you can integrate AI or a dataset for better insights)
        st.write("Suggested Career Path 1: Senior Developer -> Lead Developer -> CTO")
        st.write("Suggested Career Path 2: Junior Developer -> Backend Developer -> Software Architect")

# Resume Review UI
def resume_review():
    st.title('Resume Review')
    st.write("Upload your resume for feedback:")
    
    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"])
    if uploaded_file is not None:
        st.write("Analyzing your resume...")
        # Placeholder for resume review (you can later integrate AI models for feedback)
        st.write("Your resume looks good! But make sure to improve your skills in Python and Machine Learning.")

# Login UI
def login_page():
    st.markdown('<div class="login-form">', unsafe_allow_html=True)
    st.subheader('Login')
    username = st.text_input('Username', key="login_username")
    password = st.text_input('Password', type='password', key="login_password")

    # Login Button in a Row
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        login_button = st.button('Login', key="login_btn")
    with col2:
        signup_button = st.button("Sign Up", key="signup_btn")
    with col3:
        reset_button = st.button("Forgot Password?", key="reset_btn")

    if login_button:
        if username and password:
            login_response = login(username, password)
            if login_response.get('message') == 'Login successful':
                st.session_state.logged_in = True
                st.session_state.page = 'Job Recommendations'  # Redirect to the job recommendations page
                st.success('Logged in successfully!')
            else:
                st.error('Invalid credentials. Please try again.')
        else:
            st.error('Please enter both username and password.')

    if signup_button:
        st.session_state.page = "signup"

    if reset_button:
        st.session_state.page = "reset_password"

    st.markdown('</div>', unsafe_allow_html=True)

# Sign Up UI
def signup_page():
    st.markdown('<div class="login-form">', unsafe_allow_html=True)
    st.subheader('Sign Up')
    username_signup = st.text_input('New Username', key="signup_username")
    name_signup = st.text_input('Full Name', key="signup_name")
    password_signup = st.text_input('Password', type='password', key="signup_password")

    # Buttons in a Row
    col1, col2 = st.columns([1, 1])
    with col1:
        signup_button = st.button('Sign Up', key="signup_btn_submit")
    with col2:
        back_button = st.button("Back to Login", key="signup_back_btn")

    if signup_button:
        if username_signup and name_signup and password_signup:
            register_response = register(username_signup, name_signup, password_signup)
            if register_response.get('message') == "User registered successfully":
                st.success('User registered successfully! Please log in.')
                st.session_state.page = "login"
            else:
                st.error(register_response.get('message'))
        else:
            st.error('Please fill in all fields.')

    if back_button:
        st.session_state.page = "login"

    st.markdown('</div>', unsafe_allow_html=True)

# Reset Password UI
def reset_password_page():
    st.title('Reset Password')
    username_reset = st.text_input('Username (for password reset)', key="reset_username")
    new_password = st.text_input('New Password', type='password', key="reset_password_input")

    reset_button = st.button('Reset Password', key="reset_btn_submit")
    if reset_button:
        if username_reset and new_password:
            reset_response = reset_password(username_reset, new_password)
            st.success(reset_response['message'])
        else:
            st.error('Please fill in both fields.')

    # Back to Login Page
    back_button = st.button("Back to Login", key="reset_back_btn")
    if back_button:
        st.session_state.page = "login"

# Logout function
def logout():
    st.session_state.logged_in = False
    st.session_state.page = "Login"
    st.success("Logged out successfully.")

# Set default page to login if not logged in
if 'page' not in st.session_state:
    st.session_state.page = "Login"

# Show the correct page based on session state
def main():
    choice = sidebar()
    
    if choice == 'Login':
        login_page()
    elif choice == 'Sign Up':
        signup_page()
    elif choice == 'Job Recommendations':
        if st.session_state.logged_in:
            job_recommendations()
        else:
            st.session_state.page = 'Login'
    elif choice == 'Career Path Analysis':
        if st.session_state.logged_in:
            career_path_analysis()
        else:
            st.session_state.page = 'Login'
    elif choice == 'Resume Review':
        if st.session_state.logged_in:
            resume_review()
        else:
            st.session_state.page = 'Login'
    elif choice == 'Logout':
        logout()

# Run the app
if __name__ == '__main__':
    main()
