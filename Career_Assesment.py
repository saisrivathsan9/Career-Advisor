from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI client with API key
client = OpenAI(api_key=os.getenv("API_KEY"))

# Function to collect user data for career interest assessment
def collect_career_assessment_data():
    print("Welcome to the Career Interest Assessment Tool!\nPlease answer the following questions:")
    
    questions = [
        ("What activities or tasks make you feel most energized or excited?", [
            "Solving complex problems",
            "Helping others and providing support",
            "Creative work like designing or writing",
            "Organizing and managing tasks efficiently"
        ]),
        ("Do you prefer working with people, data, or things?", [
            "People",
            "Data and numbers",
            "Technology and tools",
            "Things (physical work with objects)"
        ]),
        ("What type of work environment do you thrive in?", [
            "Collaborative and team-oriented",
            "Independent and quiet",
            "Fast-paced and dynamic",
            "Structured and predictable"
        ]),
        ("What are your top 3 strengths in your current or past roles?", [
            "Analytical and problem-solving skills",
            "Communication and teamwork",
            "Creativity and innovation",
            "Leadership and decision-making"
        ]),
        ("What kind of problems do you enjoy solving?", [
            "Technical and analytical problems",
            "Helping individuals solve personal or social issues",
            "Creative and artistic challenges",
            "Organizational and strategic issues"
        ]),
        ("What skills do you excel at or enjoy using the most?", [
            "Programming and technical skills",
            "Communication and negotiation",
            "Design, writing, or artistic skills",
            "Project management and organization"
        ]),
        ("If money was not a factor, what would you love to spend your time doing?", [
            "Building software or working with technology",
            "Helping others and making a social impact",
            "Creating art, writing, or teaching",
            "Running a business, managing projects, or leading teams"
        ]),
        ("What is your preferred method of learning new things?", [
            "Hands-on, practical experience",
            "Theoretical and structured learning",
            "Visual learning through videos or diagrams",
            "Learning through discussions, mentorship, or group work"
        ]),
        ("How do you handle challenges or setbacks?", [
            "Step-by-step problem-solving approach",
            "Brainstorming multiple solutions and experimenting",
            "Seeking advice from mentors or peers",
            "Staying calm and working through it independently"
        ]),
        ("What are your long-term career goals or aspirations?", [
            "To work in a leadership or management role",
            "To specialize in a technical or expert role",
            "To work in a creative or artistic field",
            "To contribute to societal change or work in healthcare or education"
        ]),
        ("Which of these career paths interests you the most?", [
            "Software development, data science, or technology roles",
            "Healthcare or medicine, helping people improve their health",
            "Education, teaching, or research roles",
            "Business, marketing, or entrepreneurship"
        ])
    ]
    
    responses = []
    for question, options in questions:
        print(question)
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        while True:
            try:
                choice = int(input("Please select your answer (1-4): "))
                if 1 <= choice <= 4:
                    responses.append(options[choice - 1])
                    break
                else:
                    print("Invalid choice, please select a number between 1 and 4.")
            except ValueError:
                print("Invalid input, please enter a number between 1 and 4.")
    
    return responses

# Collect user data for career interest assessment
user_responses = collect_career_assessment_data()

# AI system prompt for career interest assessment
system_prompt = """
You are an AI-powered career guidance assistant. Your task is to assess the user's career interests, 
strengths, and aspirations based on their responses to a set of questions. Based on this assessment, 
you will:
1. Analyze the user's strengths, interests, and work preferences.
2. Identify the user's character and suggest potential career paths that align with their strengths, 
   interests, and long-term goals.
3. Provide tailored career advice that fits the user's aspirations and personality.
4. Address the user directly as "you" in the advice and recommendations.

For example, instead of using third person language (e.g., "the user"), refer to the user as "you". 
You will give personalized suggestions and advice based on the responses you receive from the user.
"""

# Prepare messages for AI
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": f"Here are the user's responses to the career interest assessment:\n"
                                 f"1. {user_responses[0]}\n"
                                 f"2. {user_responses[1]}\n"
                                 f"3. {user_responses[2]}\n"
                                 f"4. {user_responses[3]}\n"
                                 f"5. {user_responses[4]}\n"
                                 f"6. {user_responses[5]}\n"
                                 f"7. {user_responses[6]}\n"
                                 f"8. {user_responses[7]}\n"
                                 f"9. {user_responses[8]}\n"
                                 f"10. {user_responses[9]}\n"
                                 f"11. {user_responses[10]}"}
]

# Query the AI for career interest analysis
response = client.chat.completions.create(
    model="gpt-4",  
    messages=messages
)

# Print AI response with career suggestions
print("\nCareer Interest Assessment and Suggestions:")
print(response.choices[0].message.content)

# Collect user data for career interest assessment
user_responses = collect_career_assessment_data()

# AI system prompt for career interest assessment
system_prompt = """
You are an AI-powered career guidance assistant. Your task is to assess the user's career interests, 
strengths, and aspirations based on their responses to a set of questions. Based on this assessment, 
you will:
1. Analyze the user's strengths, interests, and work preferences.
2. Identify the user's character and suggest potential career paths that align with their strengths, 
   interests, and long-term goals.
3. Provide tailored career advice that fits the user's aspirations and personality.
4. Address the user directly as "you" in the advice and recommendations.

For example, instead of using third person language (e.g., "the user"), refer to the user as "you". 
You will give personalized suggestions and advice based on the responses you receive from the user.
"""

# Prepare messages for AI
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": f"Here are the user's responses to the career interest assessment:\n"
                                 f"1. {user_responses[0]}\n"
                                 f"2. {user_responses[1]}\n"
                                 f"3. {user_responses[2]}\n"
                                 f"4. {user_responses[3]}\n"
                                 f"5. {user_responses[4]}\n"
                                 f"6. {user_responses[5]}\n"
                                 f"7. {user_responses[6]}\n"
                                 f"8. {user_responses[7]}\n"
                                 f"9. {user_responses[8]}\n"
                                 f"10. {user_responses[9]}"}
]

# Query the AI for career interest analysis
response = client.chat.completions.create(
    model="gpt-4",  
    messages=messages
)

# Print AI response with career suggestions
print("\nCareer Interest Assessment and Suggestions:")
print(response.choices[0].message.content)