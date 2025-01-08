from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI client with API key
client = OpenAI(api_key=os.getenv("API_KEY"))

# Function to collect user data
def collect_user_data():
    print("Welcome to the Skill Gap Analysis Tool!\nPlease answer the following questions:")
    education = input("1. What is your highest education level? (e.g., Bachelor's, Master's, etc.): ")
    career_interest = input("2. What career are you interested in? (e.g., Data Scientist, Software Engineer, etc.): ")
    skills = input("3. What skills do you currently have? (List your skills separated by commas): ")
    weaknesses = input("4. What are your weaknesses or areas where you feel you lack skills? (List them separated by commas): ")
    return {
        "education": education,
        "career_interest": career_interest,
        "skills": skills,
        "weaknesses": weaknesses
    }

# Collect user data
user_data = collect_user_data()

# AI system prompt for skill gap analysis
system_prompt = """
You are an AI-powered career guidance assistant. Your purpose is to analyze skill gaps and 
help users transition into their desired careers. Based on the user's highest education level, 
current skills, weaknesses, and career of interest, you will:
1. Identify the skills the user needs to acquire for the desired career.
2. Suggest relevant resources such as online courses, certifications, books, or tools to bridge the gap.
3. Provide a step-by-step roadmap to help the user achieve their career goals.
"""

# Prepare messages for AI
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": f"My highest education level is: {user_data['education']}.\n"
                                 f"My career of interest is: {user_data['career_interest']}.\n"
                                 f"My current skills are: {user_data['skills']}.\n"
                                 f"My weaknesses are: {user_data['weaknesses']}."}
]

# Query the AI
response = client.chat.completions.create(
    model="gpt-4",  
    messages=messages
)

# Print AI response
print("\nSkill Gap Analysis and Recommendations:")
print(response.choices[0].message.content)