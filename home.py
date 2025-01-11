# Home page of the Career Chat web app
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI client with API key
client = OpenAI(api_key=os.environ.get("API_KEY"))

st.set_page_config(page_title="Career Chat", layout="wide")

# Function to handle user input
def handle_input():
    user_message = st.session_state.input_box.strip()
    if user_message:
        # Append the user's message to the chat history
        st.session_state.chat_history.append(("You", user_message))

        # Display a temporary "Thinking..." message
        thinking_placeholder = st.empty()
        thinking_placeholder.markdown("**Advisor:** Thinking... 🤔")

        # Process the user input to get the AI's response
        ai_response = process_user_input(user_message)

        # Replace the "Thinking..." message with the AI's actual response
        thinking_placeholder.empty()
        st.session_state.chat_history.append(("Advisor", ai_response))

        # Clear the input box
        st.session_state.input_box = ""

# Function to clear the chat history
def clear_chat():
    st.session_state.chat_history = [
        ("Advisor", 
         "Hi there! I'm here to help you with all your career-related questions. Whether you're exploring new job opportunities, planning your career path, or just need advice, feel free to ask away!\n\n"
         "💡 **Here are some things you can try:**\n"
         "- \"What are the best careers for someone with [your skills or interests]?\"\n"
         "- \"How do I prepare for an interview at [company name]?\"\n"
         "- \"What certifications can boost my resume in [your field]?\"\n"
         "- \"Can you help me write a professional LinkedIn headline?\"\n\n"
         "Type your message below to get started! 🚀")
    ]

def main():
    reset = True

    # Add a heading to the page
    st.title("Career Chat")

    # Create tabs for different functionalities
    Tabs = st.tabs(["Chat", "Career Interest Assessment", "Skill Gap Analysis"])

    # Chat tab content
    with Tabs[0]:
        # Initialize chat history in session state
        if "chat_history" not in st.session_state:
            clear_chat()  # Initialize with the system welcome message

        # Display the chat history
        chat_placeholder = st.container()
        with chat_placeholder:
            for sender, message in st.session_state.chat_history:
                if sender == "Advisor":
                    st.markdown(f"**{sender}:** {message}")
                else:
                    st.markdown(f"**{sender}:** {message}")

        # Input box and buttons at the bottom
        with st.container():
            input_field = st.text_input(
                "",  # No label text to avoid duplication
                key="input_box",
                placeholder="Type your message...",
            )
            st.button("Send", on_click=handle_input)
            st.button("Clear Chat", on_click=clear_chat)
    # Career Assessment Tab
    with Tabs[1]:
        st.title("Career Assessment")
        st.write("Answer these questions to discover your career interests and strengths.")

        
        # Display multiple-choice questions
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
        # Iterate through each question
        for i, (question, options) in enumerate(questions):
            # Display the question
            st.write(f"**{i + 1}. {question}**")

            # Use st.radio for the options, ensuring each question has a unique key
            selected_option = st.radio(
                label="",
                options=options,
                key=f"question_{i}",
            )

            # Store the user's response
            responses.append(selected_option)

        # Reset button logic
        if "assessment_responses" not in st.session_state:
            st.session_state.assessment_responses = [None] * len(questions)

        def reset_assessment():
            reset = True
            st.session_state.assessment_responses = [None] * len(questions)

        if reset:
            if st.button("Submit Assessment"):
                # Display "Thinking..." message while processing
                thinking_placeholder = st.empty()
                thinking_placeholder.markdown("**Advisor:** Thinking... 🤔")

                user_responses = "\n".join([f"{i + 1}. {response}" for i, response in enumerate(responses)])
                system_prompt = """
                You are an AI-powered career guidance assistant. Your task is to assess the user's career interests, 
                strengths, and aspirations based on their responses to a set of questions. Based on this assessment, 
                you will:
                1. Analyze the user's strengths, interests, and work preferences.
                2. Identify the user's character and suggest potential career paths that align with their strengths, 
                interests, and long-term goals.
                3. Provide tailored career advice that fits the user's aspirations and personality.
                4. Address the user directly as "you" in the advice and recommendations.
                """
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Here are the user's responses:\n{user_responses}"}
                ]
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=messages
                )

                # Replace "Thinking..." message with the AI's response
                thinking_placeholder.empty()
                st.write("**Career Interest Assessment Results:**")
                st.write(response.choices[0].message.content)

                # Reset button
                if st.button("Reset Assessment"):
                    reset_assessment()
            

    # Skill Gap Analysis Tab
    with Tabs[2]:
        st.title("Skill Gap Analysis")
        st.write("Identify your skills and gaps to achieve your career goals.")

        # Input form for skill gap analysis
        education = st.text_input("1. What is your highest education level? (e.g., Bachelor's, Master's, etc.)")
        career_interest = st.text_input("2. What career are you interested in? (e.g., Data Scientist, Software Engineer, etc.)")
        skills = st.text_area("3. What skills do you currently have? (List your skills separated by commas)")
        weaknesses = st.text_area("4. What are your weaknesses or areas where you feel you lack skills?")

        if st.button("Submit Skill Gap Analysis"):
            # Process responses with AI
            system_prompt = """
            You are an AI-powered career guidance assistant. Your purpose is to analyze skill gaps and 
            help users transition into their desired careers. Based on the user's highest education level, 
            current skills, weaknesses, and career of interest, you will:
            1. Identify the skills the user needs to acquire for the desired career.
            2. Suggest relevant resources such as online courses, certifications, books, or tools to bridge the gap.
            3. Provide a step-by-step roadmap to help the user achieve their career goals.
            """
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"My highest education level is: {education}.\n"
                                            f"My career of interest is: {career_interest}.\n"
                                            f"My current skills are: {skills}.\n"
                                            f"My weaknesses are: {weaknesses}."}
            ]
            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages
            )
            st.write("**Skill Gap Analysis Results:**")
            st.write(response.choices[0].message.content)

def process_user_input(user_input):
    # Initialize the messages array if not already in session state
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are an AI-powered career guidance assistant. Your purpose is to help students, job seekers, and professionals explore and plan their career paths based on their interests, skills, and goals. You provide personalized career advice, assess skill gaps, suggest relevant learning resources, and generate custom career roadmaps to help users achieve their career aspirations. You also offer real-time Q&A for users seeking guidance on career decisions, skill-building, and job transitions."}
        ]

    # Append the user's message to the message history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Make API call to OpenAI with the updated messages array
    response = client.chat.completions.create(
        model="gpt-4",  
        messages=st.session_state.messages
    )

    # Extract the advisor's response correctly
    ai_response = response.choices[0].message.content

    # Append the advisor's response to the message history
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

    # Return the AI response to display in the chat
    return ai_response

if __name__ == "__main__":
    main()
