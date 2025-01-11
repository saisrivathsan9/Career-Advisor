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
                "",  
                key="input_box",
                placeholder="Type your message...",
            )
            st.button("Send", on_click=handle_input)
            st.button("Clear Chat", on_click=clear_chat)
                
    # Career Assessment Tab
    with Tabs[1]:
        submitted = False

        st.title("Career Assessment")
        st.write("Answer these questions to discover your career interests and strengths.")

        # Define questions and options
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

        # Initialize session state for responses and submission lock
        if "assessment_responses" not in st.session_state:
            st.session_state.assessment_responses = [None] * len(questions)
            st.session_state.submitted = False

        # Input collection loop
        for i, (question, options) in enumerate(questions):
            st.write(f"**{i + 1}. {question}**")
            st.session_state.assessment_responses[i] = st.radio(
                label="",
                options=options,
                key=f"question_{i}",
                index=options.index(st.session_state.assessment_responses[i])
                if st.session_state.assessment_responses[i] else 0
            )
        
        # Reset button logic
        def reset_assessment():
            st.session_state.assessment_responses = [None] * len(questions)
            st.session_state.submitted = False

        # Submit button logic
        def submit_assessment():
            if all(st.session_state.assessment_responses):
                st.session_state.submitted = True
                submitted = True

                # Display "Thinking..." message while processing
                thinking_placeholder = st.empty()
                thinking_placeholder.markdown("**Advisor:** Thinking... 🤔")

                user_responses = "\n".join(
                    [f"{i + 1}. {response}" for i, response in enumerate(st.session_state.assessment_responses)]
                )
                # Define the system prompt concisely
                system_prompt = (
                    "You are a career guidance assistant. Analyze the user's responses about strengths, "
                    "interests, and preferences. Suggest suitable career paths and provide concise, actionable advice."
                )

                # Construct the user responses string
                user_responses = "\n".join(
                    [f"{i + 1}. {response}" for i, response in enumerate(st.session_state.assessment_responses)]
                )

                # Build the messages list for the API
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_responses}
                ]

                # Simulate the API call
                try:
                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=messages,
                        max_tokens=300,  # Limit the response length for efficiency
                        temperature=0.7,  # Adjust creativity level as needed
                    )

                    # Replace "Thinking..." message with the AI's response
                    thinking_placeholder.empty()

                    # Extract and display the assistant's response
                    ai_response = response.choices[0].message.content.strip()
                    st.write("**Career Interest Assessment Results:**")
                    st.write(ai_response)
                    if st.button("Reset Assessment"):
                        reset_assessment()

                except Exception as e:
                    st.error(f"An error occurred while processing your assessment: {e}")

            else:
                st.warning("Please answer all the questions before submitting.")

        

        # Buttons
        if not submitted:
            if st.button("Submit Assessment"):
                submit_assessment()
            

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

            # Display "Thinking..." message while processing
            thinking_placeholder = st.empty()
            thinking_placeholder.markdown("**Advisor:** Thinking... 🤔")

            # Optimized System Prompt
            system_prompt = (
                "You are a career guidance assistant. Analyze the user's education, skills, weaknesses, and career goal to:\n"
                "1. List required skills for the target career.\n"
                "2. Suggest 3 resources to bridge skill gaps.\n"
                "3. Provide a concise 5-step career roadmap."
            )

            # Combine and optimize user input
            user_input = (
                f"Education: {education}. Career Interest: {career_interest}. "
                f"Current Skills: {skills}. Weaknesses: {weaknesses}."
            )

            # Messages for the OpenAI API
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]

            # Generate response
            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.5,  # Adjust temperature for concise, deterministic output
                max_tokens=500    # Limit output tokens for efficiency
            )

            # Replace "Thinking..." message with the AI's response
            thinking_placeholder.empty()

            # Display results
            st.write("**Skill Gap Analysis Results:**")
            st.write(response.choices[0].message.content)
            if(st.button("Reset Skill Gap Analysis")):
                education = ""
                career_interest = ""
                skills = ""
                weaknesses = ""

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
            messages=st.session_state.messages,
            temperature=0.5,  # Adjust temperature for more concise, deterministic responses
            max_tokens=500    # Limit output tokens to prevent excessively long responses
        )

    # Extract the advisor's response correctly
    ai_response = response.choices[0].message.content

    # Append the advisor's response to the message history
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

    # Return the AI response to display in the chat
    return ai_response

if __name__ == "__main__":
    main()
