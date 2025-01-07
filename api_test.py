from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI client with API key
client = OpenAI(api_key=os.getenv("API_KEY"))

# Example query: Asking about a job change to the tech industry
response = client.chat.completions.create(
    model="gpt-4",  
    messages=[
        {"role": "system", "content":  "You are an AI-powered career guidance assistant. Your purpose is to help students, job seekers, and professionals explore and plan their career paths based on their interests, skills, and goals. You provide personalized career advice, assess skill gaps, suggest relevant learning resources, and generate custom career roadmaps to help users achieve their career aspirations. You also offer real-time Q&A for users seeking guidance on career decisions, skill-building, and job transitions."},
        {"role": "user", "content": "I am looking for a job in the tech industry. I am an accountant looking to change careers as a Data scientist. Need some advice"},
    ]
)

print(response.choices[0].message)
