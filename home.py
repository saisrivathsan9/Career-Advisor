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
    # Add a heading to the page
    st.title("Career Chat")

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

    # Input box at the bottom
    with st.container():
        col1, col2, col3 = st.columns([8, 1, 1])
        with col1:
            st.text_input(
                "Type your message here...",
                key="input_box",
                placeholder="Type your message...",
            )
        with col2:
            st.button("Send", on_click=handle_input)
        with col3:
            st.button("Clear Chat", on_click=clear_chat)

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
