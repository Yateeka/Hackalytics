import streamlit as st
from backend import fetch_jobs, extract_text_from_pdf, extract_text_from_docx, get_resume_feedback, fetch_unique_job_titles, fetch_unique_employment_type
from pymongo import MongoClient
import subprocess
import requests
import openai
import os
import random

# MongoDB Connection
try:
    client = MongoClient("mongodb+srv://Yateeka:hacklytics@hackalytics.warwu.mongodb.net/")
    db = client['job_data']
    job_collection = db['job_listings']
except Exception as e:
    st.error(f"Database connection failed: {e}")

# Initialize session state for login and navigation
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Sign In"
    
# Enable detailed error messages
st.set_option('client.showErrorDetails', True)

# Initialize session state for login and navigation
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Sign In"

# ---------------------- Authentication Functions ----------------------

def sign_in():
    st.subheader("Sign In")
    username = st.text_input("Username", key="signin_username")
    password = st.text_input("Password", type="password", key="signin_password")
    if st.button("Sign In"):
        if username and password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.current_page = "Job Search"
            st.success(f"Welcome back, {username}!")
            st.rerun()
        else:
            st.error("Please enter valid credentials.")

def sign_up():
    st.subheader("Sign Up")
    username = st.text_input("New Username", key="signup_username")
    password = st.text_input("New Password", type="password", key="signup_password")
    if st.button("Sign Up"):
        st.success("Account created successfully!")
        st.session_state.current_page = "Sign In"
        st.rerun()

def change_password():
    st.subheader("Change Password")
    username = st.text_input("Username", key="change_user")
    old_password = st.text_input("Old Password", type="password", key="old_pass")
    new_password = st.text_input("New Password", type="password", key="new_pass")
    if st.button("Change Password"):
        st.success("Password changed successfully!")

def sign_out():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.current_page = "Sign In"
    st.success("Signed out successfully!")
    st.rerun()

# ---------------------- Job Search ----------------------

def job_search():
    st.subheader("Job Search")
    
    # Dropdown for Job Title selection
    job_title_input = st.selectbox(
        "Select Job Title", 
        options=["Select", 
                 "Software Engineer", 
                 "Data Scientist", 
                 "Product Manager", 
                 "Registered Nurse", 
                 "HR Specialist", 
                 "Financial Analyst", 
                 "Construction Manager", 
                 "Investment Banker", 
                 "Teacher", 
                 "Event Planner", 
                 "Customer Service Representative"],  # List of job titles
        index=0  # Default to 'Select'
    )
    
    # Dropdown for Employment Type selection
    employment_type_input = st.selectbox(
        "Select Employment Type", 
        options=["Select", "Intern", "Full-time", "Part-time"],  # Default option is 'Select'
        index=0  # By default, 'Select' will be the first option
    )

    if st.button("Search Jobs"):
        # Only proceed if valid selections are made
        if job_title_input == "Select":
            st.error("Please select a valid job title.")
            return
        if employment_type_input == "Select":
            st.error("Please select a valid employment type.")
            return

        # Process the job search based on the selected job title and employment type
        query = {
            'job_title': {'$regex': job_title_input, '$options': 'i'}
        }

        if employment_type_input != "Select":
            query['employment_type'] = {'$regex': employment_type_input, '$options': 'i'}  # Case-insensitive match for employment_type

        try:
            matching_jobs = list(job_collection.find(query))

            st.subheader("Search Results")
            if matching_jobs:
                for job in matching_jobs:
                    st.write(f"**{job.get('job_title', 'N/A')}** at {job.get('company_name', 'N/A')}")
                    st.write(f"📍 Location: {job.get('location', 'N/A')}")
                    st.write(f"💼 Employment Type: {job.get('employment_type', 'N/A')}")
                    st.write(f"🛠️ Required Skills: {', '.join(job.get('required_skills', []))}")
                    st.write(f"📝 Description: {job.get('job_description', 'N/A')}")
                    st.write(f"📝 Salary: {job.get('salary_range', 'N/A')}")
                    st.write("---")
            else:
                st.warning("No matching jobs found. Try different keywords or employment type.")
        except Exception as e:
            st.error(f"Error fetching data: {e}")

# ---------------------- Resume Upload and Feedback ----------------------

def upload_resume():
    st.subheader("Upload Resume")
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx"])

    if uploaded_file is not None:
        st.success(f"Uploaded: {uploaded_file.name}")

        # Extract text
        if uploaded_file.type == "application/pdf":
            resume_text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            resume_text = extract_text_from_docx(uploaded_file)
        else:
            st.error("Unsupported file type.")
            return

        if not resume_text.strip():
            st.error("Could not extract any text from the resume. Please try another file.")
            return

        user_question = st.text_input("Enter your question or specific field (e.g., Data Science):")

        if st.button("Get Feedback"):
            feedback = get_resume_feedback(resume_text, user_question)
            st.subheader("Resume Feedback")
            st.write(feedback)


# ---------------------- Chatbot Page ----------------------

def chatbot_page():
    st.subheader("Mock Interview Generator")
    job_description = st.text_area("Enter Job Description:", height=200)
    
    if st.button("Generate Interview Questions"):
        if job_description:
            # Generate random interview questions using OpenAI
            questions = generate_random_mock_interview_questions(job_description)
            st.write("### Generated Interview Questions:")
            for i, question in enumerate(questions, 1):
                st.write(f"{question}")
        else:
            st.error("Please enter a job description.")

# ---------------------- Function to generate random mock interview questions using OpenAI ----------------------

def generate_random_mock_interview_questions(job_description):
    try:
        # Use OpenAI's API to generate a list of questions based on the job description
        response = openai.ChatCompletion.create(
            model="gpt-4",  # You can use "gpt-3.5-turbo" or "gpt-4" depending on your access
            messages=[
                {"role": "system", "content": "You are an expert career coach."},
                {"role": "user", "content": f"Generate 5 random mock interview questions based on the following job description: {job_description}"}
            ]
        )

        # Extract the generated questions from the response and clean up the formatting
        questions = response['choices'][0]['message']['content'].strip().split('\n')
        
        # Clean up any numbering that OpenAI might include in the response
        clean_questions = []
        for question in questions:
            # Remove any leading number or period (e.g., "1." or "2)")
            clean_question = question.lstrip('0123456789.').strip()
            clean_questions.append(clean_question)
        
        return clean_questions

    except Exception as e:
        st.error(f"Error generating questions: {e}")
        return []

# ---------------------- Main App ----------------------

def main():
    if st.session_state.logged_in:
        menu = ["Job Search", "Upload Resume", "Go to Chatbot", "Sign Out"]
    else:
        menu = ["Sign In", "Sign Up", "Change Password"]

    choice = st.sidebar.radio("Navigation", menu, index=menu.index(st.session_state.current_page))

    if st.session_state.current_page != choice:
        st.session_state.current_page = choice

    if st.session_state.current_page == "Sign In":
        sign_in()
    elif st.session_state.current_page == "Sign Up":
        sign_up()
    elif st.session_state.current_page == "Change Password":
        change_password()
    elif st.session_state.current_page == "Job Search":
        job_search()
    elif st.session_state.current_page == "Upload Resume":
        upload_resume()
    elif st.session_state.current_page == "Go to Chatbot":
        chatbot_page()  # Navigate to the chatbot page
    elif st.session_state.current_page == "Sign Out":
        sign_out()

if __name__ == "__main__":
    main()
