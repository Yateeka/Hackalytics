import random
from pymongo import MongoClient

# Establish a connection to MongoDB (local or cloud-based)
client = MongoClient("mongodb+srv://Yateeka:hacklytics@hackalytics.warwu.mongodb.net/") 
db = client['job_data']  # Database name
company_collection = db['companies']  # Collection for company data
job_collection = db['job_listings']  # Collection for job listings data

# Expanded list of companies by industry
industry_companies = {
    "Tech": ["Google", "Amazon", "Apple", "Microsoft", "Tesla", "Facebook", "Intel", "IBM", "Oracle", "Spotify"],
    "Finance": ["Goldman Sachs", "JP Morgan", "Wells Fargo", "Citigroup", "Barclays", "Morgan Stanley", "Bank of America"],
    "Healthcare": ["Pfizer", "Johnson & Johnson", "Merck", "CVS Health", "Medtronic", "UnitedHealth Group", "Cigna"],
    "Education": ["Harvard University", "MIT", "Stanford University", "University of California", "Yale University", "Princeton University"],
    "Retail": ["Walmart", "Target", "Costco", "Home Depot", "Best Buy", "Lowe's", "Nordstrom", "Macy's"],
    "Transportation": ["Uber", "Lyft", "FedEx", "UPS", "Tesla", "DHL", "Delta Airlines", "United Airlines"],
    "Entertainment": ["Disney", "Netflix", "Warner Bros", "Paramount", "Sony Pictures", "NBC Universal", "HBO", "Universal Studios"],
    "Energy": ["ExxonMobil", "Chevron", "Shell", "BP", "TotalEnergies", "ConocoPhillips", "Siemens Energy"],
    "Telecommunications": ["AT&T", "Verizon", "T-Mobile", "Sprint", "Comcast", "Charter Communications"],
    "Manufacturing": ["General Electric", "3M", "Caterpillar", "Cummings", "Lockheed Martin", "Siemens", "Honeywell"],
    "Construction": ["Bechtel", "Skanska", "Turner Construction", "Fluor", "Jacobs Engineering", "Kiewit Corporation"],
    "Hospitality": ["Marriott", "Hilton", "Hyatt", "InterContinental", "Accor Hotels", "Wyndham Hotels & Resorts"],
    "Agriculture": ["Bayer", "Cargill", "Archer Daniels Midland", "DuPont", "John Deere", "Syngenta", "BASF"],
    "Real Estate": ["CBRE", "JLL", "Colliers International", "Keller Williams", "Re/Max", "Coldwell Banker", "Century 21"],
    "Consulting": ["McKinsey & Company", "Boston Consulting Group", "Deloitte", "Accenture", "PwC", "EY"]
}

# Define the companies list based on industries
companies = [company for industry in industry_companies.values() for company in industry]

# Mapped job titles to required skills and descriptions
job_title_to_info = {
    "Software Engineer": {
        "description": "Design, develop, and maintain software applications and systems.",
        "required_skills": ["Python", "Java", "C++", "AWS", "SQL"]
    },
    "Data Scientist": {
        "description": "Analyze complex data sets to help companies make data-driven decisions.",
        "required_skills": ["Python", "Machine Learning", "Data Analysis", "R", "SQL"]
    },
    "Product Manager": {
        "description": "Oversee the product development process, manage product lifecycle, and work with teams to ensure product success.",
        "required_skills": ["Project Management", "Communication", "Leadership", "Problem Solving", "Agile"]
    },
    "Registered Nurse": {
        "description": "Provide patient care, monitor vital signs, and administer medications as prescribed.",
        "required_skills": ["Patient Care", "Medical Knowledge", "Compassion", "Healthcare", "Teamwork"]
    },
    "HR Specialist": {
        "description": "Manage recruitment, onboarding, and employee relations within the organization.",
        "required_skills": ["Recruitment", "Employee Relations", "Communication", "Leadership", "Talent Management"]
    },
    "Financial Analyst": {
        "description": "Analyze financial data and provide insights to help businesses make informed financial decisions.",
        "required_skills": ["Financial Modeling", "Excel", "Data Analysis", "Financial Reporting", "Accounting"]
    },
    "Construction Manager": {
        "description": "Oversee construction projects, ensuring completion on time and within budget while maintaining quality.",
        "required_skills": ["Construction Management", "Project Management", "Leadership", "Scheduling", "Budgeting"]
    },
    "Investment Banker": {
        "description": "Provide financial services to businesses, including mergers, acquisitions, and other financial transactions.",
        "required_skills": ["Financial Modeling", "Accounting", "Excel", "M&A", "Financial Analysis"]
    },
    "Teacher": {
        "description": "Plan and deliver lessons to students, assess their performance, and provide feedback.",
        "required_skills": ["Lesson Planning", "Classroom Management", "Communication", "Pedagogy", "Subject Knowledge"]
    },
    "Event Planner": {
        "description": "Organize and coordinate events from start to finish, ensuring everything runs smoothly.",
        "required_skills": ["Event Planning", "Communication", "Negotiation", "Time Management", "Budgeting"]
    },
    "Customer Service Representative": {
        "description": "Assist customers by answering inquiries, resolving complaints, and providing information about products or services.",
        "required_skills": ["Customer Service", "Communication", "Problem Solving", "Patience", "Teamwork"]
    }
}

locations = [
    "New York, NY", "San Francisco, CA", "Austin, TX", "Seattle, WA", 
    "Los Angeles, CA", "Chicago, IL", "Boston, MA", "Dallas, TX", "Denver, CO",
    "Miami, FL", "Atlanta, GA", "Washington, DC", "Phoenix, AZ", "San Diego, CA"
]

job_titles = list(job_title_to_info.keys())  # Get the job titles from the keys of the dictionary
job_descriptions = [info["description"] for info in job_title_to_info.values()]
skills_by_job_title = {title: info["required_skills"] for title, info in job_title_to_info.items()}

# Sub-positions (Employment Types)
employment_types = ["Intern", "Full-time", "Part-time"]

# Function to insert company data into MongoDB
def insert_company_data(companies, industries, locations, job_titles, job_title_to_info, job_descriptions):
    company_data = []
    
    for industry, industry_companies_list in industry_companies.items():
        for company in industry_companies_list:
            location = random.choice(locations)
            job_titles_sample = random.sample(job_titles, 3)  # Select 3 random job titles
            job_title_to_skills_sample = {job_title: job_title_to_info[job_title] for job_title in job_titles_sample}
            job_description = random.choice(job_descriptions)
            
            company_data.append({
                'company_name': company,
                'industry': industry,
                'location': location,
                'job_titles': job_titles_sample,
                'job_title_to_skills': job_title_to_skills_sample,
                'job_description': job_description
            })
    
    # Insert the data into MongoDB
    company_collection.insert_many(company_data)
    print("Company data inserted into MongoDB!")

# Function to insert job listings data into MongoDB
def insert_job_listings_data(companies, locations, job_titles, skills_by_job_title, job_descriptions, employment_types, num_rows=150):
    job_listings_data = []
    
    for _ in range(num_rows):  # Generate the desired number of rows
        company = random.choice(companies)
        job_title = random.choice(job_titles)
        required_skills = skills_by_job_title[job_title]  # Get skills related to the job title
        employment_type = random.choice(employment_types)  # Assign employment type (Intern, Full-time, Part-time)
        
        job_listing = {
            'job_title': job_title,
            'company_name': company,
            'location': random.choice(locations),
            'required_skills': required_skills,  # Skills based on job title
            'job_description': job_title_to_info[job_title]["description"],  # Description based on job title
            'employment_type': employment_type  # Sub-position (Intern, Full-time, Part-time)
        }
        
        job_listings_data.append(job_listing)
    
    # Insert the job listings data into MongoDB
    job_collection.insert_many(job_listings_data)
    print(f"Inserted {num_rows} job listings data into MongoDB!")

# Insert the company data and job listings data (with num_rows between 100-150)
insert_company_data(companies, industry_companies, locations, job_titles, job_title_to_info, job_descriptions)
insert_job_listings_data(companies, locations, job_titles, skills_by_job_title, job_descriptions, employment_types, num_rows=random.randint(100, 150))
