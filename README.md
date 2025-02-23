Job Search & Resume Feedback App

Description:
This web application is designed to help job seekers and employers alike. It allows users to:
1. Search for job listings.
2. Upload resumes for feedback.
3. Generate random interview questions based on job descriptions.
The app leverages Streamlit for creating the interactive front-end, MongoDB for storing job data,
OpenAI's GPT model for generating interview questions, and Flask for handling backend API requests.

The app is designed to improve the job application process by making it more streamlined.
Whether you're searching for a job, looking to get feedback on your resume, or preparing for interviews,
this app serves as an essential tool to support your career journey.

Features:
- Job Search: Search for jobs by title, employment type, and location.
- Resume Upload & Feedback: Upload your resume (PDF or DOCX) and get personalized feedback using OpenAI's GPT model.
- Mock Interview Generator: Generate random, job-specific interview questions based on a provided job description.
- User Authentication: Sign up, sign in, change password, and sign out to secure access.
- MongoDB Backend: Store and retrieve job listings, user data, and company information using MongoDB.

Technologies Used:
- Frontend:
  - Streamlit: Used to create the interactive user interface. Streamlit makes it easy to quickly build data-driven applications,
    offering a simple and intuitive way to create web applications with Python.
  
- Backend:
  - Flask: A lightweight web framework for Python that powers the backend of this application. It handles routes, requests,
    and responses, as well as integrates with MongoDB and OpenAI.
  - MongoDB: NoSQL database used to store job listings, user credentials, and company data. MongoDB allows for scalable
    and flexible data storage, which is crucial for large datasets like job listings.
  - OpenAI GPT: Used for generating interview questions based on job descriptions and providing resume feedback.

- File Processing:
  - PyMuPDF: Used to extract text from PDF resumes for analysis.
  - python-docx: Extracts text from DOCX files for analyzing uploaded resumes.
  
- Authentication & Security:
  - bcrypt: Used for securely hashing passwords before storing them in MongoDB, ensuring that user passwords are kept safe.
  - Flask-Session: Manages user sessions to track whether a user is logged in.

How It Works:
1. Job Search:
    - Users can search for job listings based on job title, employment type (Intern, Full-time, Part-time), and location.
    - The app queries MongoDB to retrieve matching job listings.
2. Resume Upload & Feedback:
    - Users upload their resumes in PDF or DOCX format.
    - The text is extracted from the file and processed using OpenAI’s GPT to provide feedback on the resume’s structure,
      clarity, and job market appeal.
3. Mock Interview Generator:
    - Users can input a job description, and the app uses OpenAI’s GPT to generate a set of random, job-specific interview questions.
    - This feature helps users prepare for job interviews by giving them practice questions tailored to the role.
4. User Authentication:
    - The app allows users to create an account, log in, change passwords, and log out.
    - The credentials are securely stored in MongoDB with password hashing.
5. MongoDB Database:
    - MongoDB is used to store job listings, user information, and company data.
    - This allows for efficient querying and management of large datasets related to jobs and users.

Installation Instructions:
1. Clone the Repository
    git clone https://github.com/your-username/job-search-resume-feedback-app.git
2. Install Dependencies
    Install the necessary Python libraries by running the following command:
    pip install -r requirements.txt
3. Set Up Environment Variables
    Create a .env file and add the following keys:
    API_KEY=your_openai_api_key
    MONGO_CONNECTION_STRING=your_mongodb_connection_string
    FLASK_SECRET_KEY=your_flask_secret_key
4. Run the Application
    To start the app, run:
    streamlit run app.py
    The application will be available at http://localhost:8501.
5. Running the Flask Backend
    To run the Flask backend, use the following command:
    python backend.py
    The backend will be available at http://localhost:5000.

Usage:
1. Sign In/Sign Up:
    - Users can sign in to their account or create a new account.
2. Job Search:
    - Enter job titles, employment types, and location preferences to search for jobs.
3. Upload Resume:
    - Upload a resume file (PDF or DOCX), and the app will generate feedback on the resume's content.
4. Mock Interview:
    - Enter a job description and generate mock interview questions based on the description.

Why This App Is Important:
- Job Seekers: The app provides an all-in-one platform to help job seekers search for jobs, get feedback on their resumes, and practice for interviews, all in one place.
- Employers & Hiring Managers: Employers can store and retrieve job listings, making the hiring process more efficient. The ability to generate interview questions and review resumes quickly can save valuable time.
- Resume Feedback: The resume feedback provided by GPT is essential for job seekers who want to improve the quality and relevance of their resumes, increasing their chances of landing a job.
- Interview Preparation: The mock interview feature allows job seekers to simulate interview scenarios, boosting their confidence and readiness for real-life interviews.
