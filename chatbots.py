import streamlit as st
import yaml
import google.generativeai as genai
from pydub import AudioSegment
import uuid
from utils import load_lottieurl, display_lottie
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import json
import time
import PyPDF2 as pdf
import re
import tempfile
import requests

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Access configuration values
ASSEMBLY_AI_API_KEY = config['assemblyai_api_key']
GEMINI_AI_API_KEY = config['gemini_api_key']
# ...

@st.cache_data
def generate_response(prompt, model_name="gemini-1.5-flash"):
    """Generates a response from a specified Gemini model."""
    genai.configure(api_key=GEMINI_AI_API_KEY)
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text

# --- Helper Functions ---
def display_chat_history(messages):
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def get_user_input(prompt="Your message:"):
    return st.chat_input(prompt)

def add_user_message(messages, user_input):
    messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

def add_assistant_message(messages, response_text):
    messages.append({"role": "assistant", "content": response_text})
    with st.chat_message("assistant"):
        st.markdown(response_text)

# **1. Thesis Writer Assistant**
def thesis_writer_assistant():
    st.header("Thesis Writer Assistant")

    # Use a unique key for session state to avoid conflicts with other bots
    messages = st.session_state.setdefault("thesis_messages", []) 
    
    # Display the existing chat history
    display_chat_history(messages)

    # Get user input
    user_input = get_user_input("Describe your thesis topic or ask for assistance:")

    # Process user input
    if user_input:
        add_user_message(messages, user_input)

        # Generate AI response (Example - adjust based on user input)
        prompt = f"""Provide assistance for a thesis on: '{user_input}'."""
        response_text = generate_response(prompt)  

        add_assistant_message(messages, response_text)

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Prompt Template for ATS Bot (More explicit JSON formatting)
input_prompt = """
You are a skilled and experienced ATS (Application Tracking System) with a deep understanding 
of tech fields like software engineering, data science, data analysis, and big data engineering.

Your task is to evaluate the provided resume against the given job description. 
Consider the competitive job market and offer the best assistance for improving the resume. 

Assign a "JD Match" percentage based on how well the resume matches the job description and 
identify "MissingKeywords" that are present in the job description but not in the resume.
Also, provide a "Profile Summary" of the candidate's skills based on the resume. 

Resume:
{text}

Job Description:
{jd}

I want the response ONLY in valid JSON format with the following structure:
{{"JD Match":"%", "MissingKeywords":["keyword1", "keyword2", ...], "Profile Summary":"..."}}
"""

def resume_ats_score_bot():
    st.header("Resume ATS Score Bot")
    jd = st.text_area("Paste the Job Description")
    uploaded_file = st.file_uploader("Upload Your Resume", type="pdf")

    if st.button("Analyze Resume"):
        if uploaded_file and jd:
            text = input_pdf_text(uploaded_file)
            final_prompt = input_prompt.format(text=text, jd=jd)
            response = generate_response(final_prompt)

            try:
                # Directly parse the JSON response
                response_json = json.loads(response) 

                st.subheader("ATS Analysis:")
                st.write(f"**JD Match:** {response_json.get('JD Match', 'N/A')}")
                st.write(f"**Missing Keywords:** {', '.join(response_json.get('MissingKeywords', []))}")
                st.write(f"**Profile Summary:** {response_json.get('Profile Summary', 'N/A')}")

            except json.JSONDecodeError:
                st.error("Error: Invalid JSON response. Please check the prompt and API response.")
        else:
            st.warning("Please upload a resume and provide a job description.")

code_explainer_prompt = """
            You’re a proficient code educator with a specialization in breaking down complex programming concepts 
            into simple, easy-to-understand explanations. Your expertise lies in providing thorough line-by-line 
            explanations for code snippets that help learners grasp the underlying logic and structure of the code.

            Your task is to explain the following Python code comprehensively:

            Programming Language: Python
            Code Snippet: 
            ```python
            {code_snippet}  """

def code_explainer_bot():
    st.header("Code Explainer Bot")

    # Use a unique key for session state 
    messages = st.session_state.setdefault("code_explainer_messages", [])

    # Display chat history
    display_chat_history(messages)

    # Get code snippet from user
    code_snippet = st.text_area("Paste your Python code here:")
    key_concepts = st.text_input("Key Concepts to Focus On (comma-separated):")
    experience_level = st.selectbox("Target Audience Experience Level:", 
                                    ["Beginner", "Intermediate", "Advanced"])

    if st.button("Explain Code"):
        if code_snippet:
            # Format the prompt
            final_prompt = code_explainer_prompt.format(
                code_snippet=code_snippet,
                key_concepts=key_concepts,
                experience_level=experience_level
            )

            # Add user's code to the chat history
            add_user_message(messages, f"```python\n{code_snippet}\n```")

            # Get the explanation from the Gemini model
            explanation = generate_response(final_prompt)

            # Add the explanation to the chat history
            add_assistant_message(messages, explanation)

        else:
            st.warning("Please paste some Python code.")

healerbeast_prompt = """
You are a kind and supportive friend named Healerbeast. Someone is reaching out to you feeling {current_feelings}.
They've said: "{user_message}". 

Respond in a way that is friendly, empathetic, and understanding. Offer encouragement or helpful advice, 
but remember, you are not a therapist. If the person seems to be in serious distress or mentions self-harm, 
strongly encourage them to seek help from a mental health professional. 
"""

def healerbeast_bff():
    st.header("Healerbeast (Your Virtual Friend)")

    # Unique session state key
    messages = st.session_state.setdefault("healerbeast_messages", [])

    # Display chat history
    display_chat_history(messages)

    # Get user input
    user_input = get_user_input("How are you feeling? Tell me anything.")

    if user_input:
        add_user_message(messages, user_input)

        # You can use NLP later to extract feelings more accurately
        current_feelings = user_input

        final_prompt = healerbeast_prompt.format(
            current_feelings=current_feelings,
            user_message=user_input
        )

        response_text = generate_response(final_prompt)
        add_assistant_message(messages, response_text)
            
def qanda_bot():
    st.header("Q&A Bot")

    # Initialize chat history if it doesn't exist
    if "qanda_messages" not in st.session_state:
        st.session_state["qanda_messages"] = []

    # Get user input OUTSIDE the 'if' block
    user_input = get_user_input("Ask a question:")

    # Process user input
    if user_input:
        add_user_message(st.session_state["qanda_messages"], user_input)
        prompt = f"Your Prompt for Q&A Bot using {user_input}" 
        response_text = generate_response(prompt)
        add_assistant_message(st.session_state["qanda_messages"], response_text)

    # Display chat history AFTER processing the input
    display_chat_history(st.session_state["qanda_messages"])

def transcribe_file(file_path):
    headers = {
        "authorization": ASSEMBLY_AI_API_KEY,
        "content-type": "application/json"
    }

    with open(file_path, "rb") as f:
        response = requests.post("https://api.assemblyai.com/v2/upload", headers=headers, data=f)
        response.raise_for_status()
    upload_url = response.json()["upload_url"]
    data = {"audio_url": upload_url}

    response = requests.post("https://api.assemblyai.com/v2/transcript", json=data, headers=headers)
    response.raise_for_status()
    transcript_id = response.json()["id"]

    while True:
        response = requests.get(f"https://api.assemblyai.com/v2/transcript/{transcript_id}", headers=headers)
        response.raise_for_status()
        status = response.json()["status"]

        if status == "completed":
            return response.json()["text"]
        elif status == "error":
            error_message = response.json().get("error", "Unknown error")
            raise Exception(f"Transcription failed: {error_message}")
        time.sleep(5)

# Function to create PDF
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    
    pdf_output = pdf.output(dest='S').encode('latin1')  # Output PDF as string
    return pdf_output

# Function to get summary from AssemblyAI
def get_summary(audio_url):
    headers = {
        "authorization": ASSEMBLY_AI_API_KEY,
        "content-type": "application/json"
    }

    data = {
        "audio_url": audio_url,
        "summarization": True,
    }

    response = requests.post("https://api.assemblyai.com/v2/transcript", json=data, headers=headers)
    response.raise_for_status()
    transcript_id = response.json()["id"]

    while True:
        response = requests.get(f"https://api.assemblyai.com/v2/transcript/{transcript_id}", headers=headers)
        response.raise_for_status()
        status = response.json()["status"]

        if status == "completed":
            return response.json()["summary"]
        elif status == "error":
            error_message = response.json().get("error", "Unknown error")
            raise Exception(f"Summarization failed: {error_message}")
        time.sleep(5)

def transcription_bot():
    st.header("Transcription Bot")

    uploaded_file = st.file_uploader(
        "Choose an audio or video file", type=["mp3", "mp4", "avi", "mov"]
    )

    if uploaded_file is not None:
        try:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(uploaded_file.getvalue())
                file_path = temp_file.name

            # Process video files
            if file_path.lower().endswith((".mp4", ".avi", ".mov")):
                audio = AudioSegment.from_file(file_path, format=file_path.split(".")[-1])
                audio_path = os.path.splitext(file_path)[0] + ".mp3"
                audio.export(audio_path, format="mp3")
                file_path = audio_path

            with st.spinner("Transcribing... This may take a few minutes."):
                transcript, summary, audio_url = process_audio(file_path)

            if transcript:
                st.success("Transcription complete!")
                st.text_area("Transcript:", transcript, height=300)

                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="Download Transcript as TXT",
                        data=transcript,
                        file_name="transcript.txt",
                        mime="text/plain",
                    )
                with col2:
                    pdf_output = create_pdf(transcript)
                    st.download_button(
                        label="Download Transcript as PDF",
                        data=pdf_output,
                        file_name="transcript.pdf",
                        mime="application/pdf",
                    )

                if summary:
                    st.header("Summary:")
                    st.write(summary)
            else:
                st.error("Transcription failed. Please try again.")

        except Exception as e:
            st.error(f"An error occurred: {e}")

@st.cache_data  # Cache the results for performance
def process_audio(file_path):
    """Processes the audio file: uploads, transcribes, and summarizes."""
    headers = {"authorization": ASSEMBLY_AI_API_KEY}
    response = requests.post(
        "https://api.assemblyai.com/v2/upload",
        headers=headers,
        data=open(file_path, "rb"),
    )
    response.raise_for_status()
    audio_url = response.json()["upload_url"]

    transcript = transcribe_file(file_path)
    summary = get_summary(audio_url) if transcript else None

    return transcript, summary, audio_url

CHATBOTS = {
    "Thesis Writer": {
        "function": lambda: st.write("Thesis Writer function called"),
        "description": "Get help brainstorming, structuring, and writing your thesis.",
        "lottie": "https://assets5.lottiefiles.com/packages/lf20_khzniaya.json",
    },
    "Resume ATS Score": {
        "function": lambda: st.write("Resume ATS Score function called"),
        "description": "Analyze your resume for ATS compatibility and get improvement tips.",
        "lottie": "https://assets5.lottiefiles.com/private_files/lf30_gcroxmje.json",
    },
    "Code Explainer": {
        "function": lambda: st.write("Code Explainer function called"),
        "description": "Get clear and concise explanations of your Python code.",
        "lottie": "https://assets5.lottiefiles.com/packages/lf20_CTaizi.json",
    },
    "Healerbeast BFF": {
        "function": lambda: st.write("Healerbeast BFF function called"),
        "description": "Chat with a friendly and supportive virtual friend.",
        "lottie": "https://assets1.lottiefiles.com/private_files/lf30_bb9bkg1h.json",
    },
    "Q&A": {
        "function": lambda: st.write("Q&A function called"),
        "description": "Ask questions and get answers on a wide range of topics.",
        "lottie": "https://assets2.lottiefiles.com/packages/lf20_zw0djhar.json",
    },
    "Transcription": {
        "function": lambda: st.write("Transcription function called"),
        "description": "Transcribe and summarize your audio and video files.",
        "lottie": "https://assets1.lottiefiles.com/packages/lf20_wc1wtcet.json",
    },
}

fallback_icon = {
    "v": "5.5.7",
    "fr": 60,
    "ip": 0,
    "op": 60,
    "w": 100,
    "h": 100,
    "nm": "Fallback",
    "ddd": 0,
    "assets": [],
    "layers": [{
        "ddd": 0,
        "ind": 1,
        "ty": 4,
        "nm": "Shape Layer 1",
        "sr": 1,
        "ks": {
            "o": {"a": 0, "k": 100, "ix": 11},
            "r": {"a": 0, "k": 0, "ix": 10},
            "p": {"a": 0, "k": [50, 50, 0], "ix": 2},
            "a": {"a": 0, "k": [0, 0, 0], "ix": 1},
            "s": {"a": 0, "k": [100, 100, 100], "ix": 6}
        },
        "ao": 0,
        "shapes": [{
            "ty": "rc",
            "d": 1,
            "s": {"a": 0, "k": [50, 50], "ix": 2},
            "p": {"a": 0, "k": [0, 0], "ix": 3},
            "r": {"a": 0, "k": 0, "ix": 4},
            "nm": "Rectangle Path 1",
            "mn": "ADBE Vector Shape - Rect",
            "hd": False
        }],
        "ip": 0,
        "op": 60,
        "st": 0,
        "bm": 0
    }]
}
def chatbot():
    st.header("Choose Your AI Assistant")

    # Custom CSS for animation, layout, and spacing
    st.markdown(
        """
        <style>
        .chatbot-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 20px; 
        }
        .chatbot-card {
            /* ... your existing chatbot-card styles ... */
        }
        .stChatInputContainer {  /* Style the Streamlit chat input container */
            margin-top: 10px !important; /* Adjust margin as needed */
        }
        .stChatMessage { /* Style the Streamlit chat message container */
            margin-bottom: 10px !important; /* Adjust margin as needed */
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    # Selectbox for chatbot choice with animation container
    with st.container():
        st.markdown('<div class="selectbox-container">', unsafe_allow_html=True)
        bot_choice = st.selectbox(
            "Select an AI Assistant:",
            ["Thesis Writer Assistant", "Resume ATS Score Bot", "Code Explainer Bot", 
             "Healerbeast (BFF)", "Q&A Bot", "Transcription Bot"]
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # Call selected chatbot function
    if bot_choice == "Thesis Writer Assistant":
        thesis_writer_assistant()
    elif bot_choice == "Resume ATS Score Bot":
        resume_ats_score_bot()
    elif bot_choice == "Code Explainer Bot":
        code_explainer_bot()
    elif bot_choice == "Healerbeast (BFF)":
        healerbeast_bff()
    elif bot_choice == "Transcription Bot":
        st.title("AssemblyAI Multi-Bot Assistant")
        st.write("Welcome to your AI-powered assistant! Choose a bot to get started.")
        transcription_bot()
    elif bot_choice == "Q&A Bot":
        qanda_bot()