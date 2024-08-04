import streamlit as st
import plotly.express as px
import pandas as pd
import os
import base64
import requests
from pydub import AudioSegment
from fpdf import FPDF
from moviepy.editor import *
import time
import PyPDF2 as pdf
import json
import ast
import re 
import plotly.graph_objects as go
from pyvis.network import Network
from streamlit_option_menu import option_menu
import google.generativeai as genai
import matplotlib.pyplot as plt

def set_background(image_file, is_gif=False):
    with open(image_file, "rb") as f:
        img_data = f.read()
    b64_encoded = base64.b64encode(img_data).decode()
    img_type = "gif" if is_gif else "png"
    style = f"""
        <style>
        .stApp {{
            background-image: url(data:image/{img_type};base64,{b64_encoded});
            background-size: cover;
            background-attachment: fixed;
        }}
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)

def create_skills_chart():
    skills_data = pd.DataFrame({
        'Skill': ['Python', 'SQL', 'Machine Learning', 'Data Visualization', 'Statistical Analysis'],
        'Proficiency': [90, 85, 80, 85, 80]
    })
    
    fig = px.bar(skills_data, x='Skill', y='Proficiency', 
                 title='Core Skills',
                 labels={'Proficiency': 'Proficiency Level'},
                 color='Proficiency',
                 color_continuous_scale='Viridis')
    return fig

def create_education_chart():
    education_data = pd.DataFrame({
        'Year': [2018, 2019, 2020, 2021, 2022],
        'SGPA': [7.0, 7.2, 7.5, 8.0, 9.18]
    })
    
    fig = px.line(education_data, x='Year', y='SGPA', 
                  title='Academic Performance',
                  labels={'SGPA': 'SGPA'},
                  markers=True)
    return fig

def display_work_experience():
    st.subheader("Work Experience")
    st.write("**Data Science Intern | AI Variant | Bangalore**")
    st.write("March 2023 - December 2023")
    
    experience_details = [
        "Collaborated on data-driven projects, contributing impactful insights aligned with business requirements.",
        "Managed data collection and preparation, ensuring clean and reliable datasets for analysis.",
        "Applied machine learning algorithms to achieve project goals and effectively communicated findings and potential risks.",
        "Designed experiments and operationalized models following AI and engineering best practices.",
        "Proficiently scripted in various languages and utilized Microsoft AI and ML tools for efficient analysis.",
        "Contributed to internal best practices for data collection and preparation, ensuring data integrity.",
        "Conducted extensive exploratory data analysis on large datasets, identifying valuable patterns and trends.",
        "Assisted in evaluating team models, recommending enhancements to ensure alignment with business objectives.",
        "Collaborated with cross-functional teams, enhancing solutions to drive business value.",
        "Maintained a customer-oriented approach by understanding business, product, and customer perspectives."
    ]
    
    with st.expander("View Details"):
        for detail in experience_details:
            st.write(f"• {detail}")

    # Add a chart or visualization related to your internship
    internship_impact = pd.DataFrame({
        'Metric': ['Projects Completed', 'Algorithms Implemented', 'Datasets Analyzed'],
        'Value': [5, 8, 15]  # Replace with actual values
    })
    fig = px.bar(internship_impact, x='Metric', y='Value', title='Internship Impact')
    st.plotly_chart(fig, use_container_width=True)

def create_project_impact_chart():
    project_data = pd.DataFrame({
        'Project': ['App Rating Prediction', 'Fake News Detection', 'Oil Price Prediction'],
        'Impact Score': [93, 85, 88]
    })
    
    fig = px.pie(project_data, values='Impact Score', names='Project', 
                 title='Project Impact',
                 hole=0.3)
    return fig

def create_skills_network(role):
    """Creates a skill network graph based on the selected role."""

    if role == "Data Analyst":
        skills_data = {
            "nodes": [
                {"id": "SQL", "group": "Databases"},
                {"id": "Excel", "group": "Tools"},
                {"id": "Data Visualization", "group": "Analysis"},
                {"id": "Statistical Analysis", "group": "Analysis"},
                {"id": "Business Intelligence", "group": "Business"}
            ],
            "edges": [
                {"source": "SQL", "target": "Data Visualization", "label": "Data Insights"},
                {"source": "Excel", "target": "Data Visualization", "label": "Reporting"},
                {"source": "Statistical Analysis", "target": "Business Intelligence", "label": "Decision Making"},
                {"source": "Data Visualization", "target": "Business Intelligence", "label": "Actionable Insights"}
            ]
        }
    elif role == "Data Scientist":
        skills_data = {
            "nodes": [
                {"id": "Python", "group": "Programming"},
                {"id": "Machine Learning", "group": "AI/ML"},
                {"id": "Deep Learning", "group": "AI/ML"},
                {"id": "NLP", "group": "AI/ML"},
                {"id": "Big Data", "group": "Data"}
            ],
            "edges": [
                {"source": "Python", "target": "Machine Learning", "label": "Model Building"},
                {"source": "Python", "target": "Deep Learning", "label": "Neural Networks"},
                {"source": "Python", "target": "NLP", "label": "Text Analysis"},
                {"source": "Machine Learning", "target": "Big Data", "label": "Scalability"},
                {"source": "Deep Learning", "target": "Big Data", "label": "Large Datasets"}
            ]
        }
    else:  # Python Developer
        skills_data = {
            "nodes": [
                {"id": "Python", "group": "Programming"},
                {"id": "Django", "group": "Frameworks"},
                {"id": "Flask", "group": "Frameworks"},
                {"id": "API Development", "group": "Backend"},
                {"id": "Database Design", "group": "Databases"}
            ],
            "edges": [
                {"source": "Python", "target": "Django", "label": "Web Apps"},
                {"source": "Python", "target": "Flask", "label": "REST APIs"},
                {"source": "Django", "target": "Database Design", "label": "Data Models"},
                {"source": "Flask", "target": "API Development", "label": "Microservices"},
                {"source": "API Development", "target": "Database Design", "label": "Data Persistence"}
            ]
        }

    # Create a Pyvis network graph
    net = Network(height="600px", width="100%", notebook=True, heading=f"{role} Skill Network")

    # Add nodes with groups
    for node in skills_data["nodes"]:
        net.add_node(node["id"], group=node["group"])

    # Add edges with labels
    for edge in skills_data["edges"]:
        net.add_edge(edge["source"], edge["target"], title=edge["label"])

            # Configure interactivity options
# Configure interactivity options (CORRECTED)
    net.set_options("""
    const options = {
      "physics": {
        "enabled": true,
        "barnesHut": {
          "gravitationalConstant": -2000,
          "centralGravity": 0.3,
          "springLength": 95,
          "springConstant": 0.04,
          "damping": 0.09
        },
        "maxVelocity": 50,
        "minVelocity": 0.1,
        "solver": "barnesHut",
        "timestep": 0.5
      },
      "nodes": {
        "font": {
          "size": 14
        }
      },
      "edges": {
        "smooth": {
          "enabled": true,
          "type": "dynamic"
        }
      },
      "interaction": {
        "hover": true,
        "tooltipDelay": 200,
        "navigationButtons": true
      }
    }
    """)

    # Save and display the graph
    net.save_graph("skills_network.html")
    st.components.v1.html(open("skills_network.html", 'r').read(), height=650)

def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}" class="download-btn">Download {file_label}</a>'
    return href

def display_pdf(file_path):
    """Displays a PDF file within the Streamlit app."""
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def generate_response(prompt, model_name="gemini-1.5-flash"):
    """Generates a response from a specified Gemini model."""
    genai.configure(api_key="AIzaSyB_1wDDKexv5EPqB8kJZOhuISGOixPzHlM")
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text

# **1. Thesis Writer Assistant**
def thesis_writer_assistant():
    st.header("Thesis Writer Assistant")
    # Use st.session_state to manage chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("Describe your thesis topic or ask for assistance:")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Generate AI response (Example - adjust based on user input)
        prompt = f"""Provide assistance for a thesis on: '{user_input}'."""
        response_text = generate_response(prompt)  

        st.session_state.messages.append({"role": "assistant", "content": response_text})
        with st.chat_message("assistant"):
            st.markdown(response_text)

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
    uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

    if st.button("Analyze Resume"):
        if uploaded_file is not None and jd:
            text = input_pdf_text(uploaded_file)
            final_prompt = input_prompt.format(text=text, jd=jd)
            response = generate_response(final_prompt)
            st.write(response)  # Print the raw response for debugging

            # Extract JSON using a regular expression
            json_match = re.search(r'{.*}', response, re.DOTALL)

            if json_match:
                try:
                    response_json = json.loads(json_match.group(0))
                    st.subheader("ATS Analysis:")
                    st.write(f"**JD Match:** {response_json.get('JD Match', 'N/A')}")
                    st.write(f"**Missing Keywords:** {', '.join(response_json.get('MissingKeywords', []))}")
                    st.write(f"**Profile Summary:** {response_json.get('Profile Summary', 'N/A')}")

                except json.JSONDecodeError:
                    st.error("Error: The extracted JSON is still invalid. Please refine the prompt.")
            else:
                st.error("Error: Could not find valid JSON in the response. Please refine the prompt.")
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

            # Get the explanation from the Gemini model
            explanation = generate_response(final_prompt)

            # Display the explanation
            st.subheader("Code Explanation:")
            st.write(explanation)

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

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("How are you feeling? Tell me anything.")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Get user's feeling from the message
        current_feelings = user_input  # You can use NLP later to extract feelings more accurately

        final_prompt = healerbeast_prompt.format(
            current_feelings=current_feelings,
            user_message=user_input
        )

        response_text = generate_response(final_prompt)

        st.session_state.messages.append({"role": "assistant", "content": response_text})
        with st.chat_message("assistant"):
            st.markdown(response_text)
def qanda_bot():
    st.header("Q&A Bot")

    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    input_text = st.text_input("Input: ", key="input")
    submit = st.button("Ask the question")

    if submit and input_text:
        response = generate_response(input_text)

        # Add user query and bot response to chat history
        st.session_state['chat_history'].append(("You", input_text)) 
        st.session_state['chat_history'].append(("Bot", response))

    st.subheader("Chat History:")
    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}") 
# Set your AssemblyAI API key
ASSEMBLY_AI_API_KEY = "ef55ef0e076444d399575c7859de966c"

# Function to transcribe audio/video files
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
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        pdf_path = temp_file.name
        pdf.output(pdf_path)
    
    return pdf_path

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

# Streamlit UI for the transcription bot
def transcription_bot():
    st.subheader("Transcription Bot")

    uploaded_file = st.file_uploader("Choose an audio or video file", type=["mp3", "mp4", "avi", "mov"])
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix="." + uploaded_file.name.split(".")[-1]) as temp_file:
            temp_file.write(uploaded_file.getvalue())
            file_path = temp_file.name

        if uploaded_file.name.lower().endswith((".mp4", ".avi", ".mov")):
            audio = AudioSegment.from_file(file_path, format=file_path.split(".")[-1])
            audio_path = os.path.splitext(file_path)[0] + ".mp3"
            audio.export(audio_path, format="mp3")
            file_path = audio_path

        with st.spinner("Transcribing... This may take a few minutes."):
            # Upload the file to AssemblyAI (Get the audio_url here)
            headers = {
                "authorization": ASSEMBLY_AI_API_KEY,
            }
            response = requests.post(
                "https://api.assemblyai.com/v2/upload",
                headers=headers,
                data=open(file_path, "rb"),
            )
            response.raise_for_status()
            audio_url = response.json()["upload_url"]  # Correctly define audio_url

            transcript = transcribe_file(file_path)

        if 'transcript' in locals():
            st.success("Transcription complete!")
            st.text_area("Transcript:", transcript, height=300)

            # ... (Download as TXT and PDF buttons - Implementation remains the same)

            # Get and display summary
            with st.spinner("Generating Summary..."):
                summary = get_summary(audio_url)  # Now you can use audio_url here
            st.header("Summary:")
            st.write(summary)

# Chatbot Selection
def chatbot():
    bot_choice = st.selectbox(
        "Select a Chatbot:",
        ["Thesis Writer Assistant", "Resume ATS Score Bot", "Code Explainer Bot", "Healerbeast (BFF)", "Q&A Bot", "Transcription Bot"]  # Added "Transcription Bot" here
    )

    if bot_choice == "Thesis Writer Assistant":
        thesis_writer_assistant()
    elif bot_choice == "Resume ATS Score Bot":
        resume_ats_score_bot()
    elif bot_choice == "Code Explainer Bot":
        code_explainer_bot()
    elif bot_choice == "Healerbeast (BFF)":
        healerbeast_bff()
    elif bot_choice == "Transcription Bot":  # Changed from "transcription_bot" to "Transcription Bot"
        st.title("AssemblyAI Multi-Bot Assistant")
        st.write("Welcome to your AI-powered assistant! Choose a bot to get started.")
        transcription_bot()
    elif bot_choice == "Q&A Bot":
        qanda_bot()  # Call the Q&A bot function

def main():
    st.set_page_config(page_title="SYED SHAHID NAZEER - Portfolio", layout="wide")

    st.markdown("""
    <style>
    /* Base styles */
    body {
        color: #333333;
        background-color: #ffffff;
    }

    .big-font { 
        font-size: calc(24px + 2vw) !important; 
        color: #333333 !important; 
    }
    .medium-font { 
        font-size: calc(18px + 1vw) !important; 
        color: #333333 !important; 
    }
    .small-font { 
        font-size: calc(14px + 0.5vw) !important; 
        color: #333333 !important; 
    }
    .stSelectbox { 
        max-width: 300px; 
    }

    /* Styles for mobile devices */
    @media (max-width: 768px) {
        body {
            color: #333333 !important;
        }
        .big-font { 
            font-size: 24px !important; 
            color: #333333 !important;
        }
        .medium-font { 
            font-size: 18px !important; 
            color: #333333 !important;
        }
        .small-font { 
            font-size: 14px !important; 
            color: #333333 !important;
        }
        .responsive-container {
            flex-direction: column;
        }
        .stApp {
            background-attachment: scroll; 
        }
        iframe {
            height: 600px;
        }
        /* Ensure text is visible on all backgrounds */
        .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6 {
            color: #333333 !important;
            text-shadow: 1px 1px 2px rgba(255,255,255,0.5);
        }
    }

    /* Additional styles to ensure visibility */
    .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6 {
        color: #333333 !important;
    }

    /* Style for links to ensure visibility */
    a {
        color: #0066cc !important;
        text-decoration: underline;
    }

    /* Style for buttons to ensure visibility */
    .stButton>button {
        color: #ffffff !important;
        background-color: #0066cc !important;
        border-color: #0066cc !important;
    }

    </style>
    """, unsafe_allow_html=True)

    # Role selection navbar
    role = option_menu(
        menu_title=None,
        options=["Data Analyst", "Data Scientist", "Python Developer"],
        icons=["bar-chart-fill", "gear-fill", "code-slash"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "rgba(250, 250, 250, 0.8)"},
            "icon": {"color": "orange", "font-size": "calc(16px + 0.5vw)"}, 
            "nav-link": {"font-size": "calc(14px + 0.5vw)", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#02ab21"},
        }
    )

    # Set background based on role
    background_images = {
        "Data Analyst": "data_analyst_bg.jpg",
        "Data Scientist": "data_scientist_bg.jpg",
        "Python Developer": "python_developer_bg.jpg"
    }
    set_background(background_images[role])

    selected = option_menu(
        menu_title=None,
        options=["Home", "Skills", "Projects", "Contact", "Chat Bot"],
        icons=["house", "gear", "code-slash", "envelope", "chat-dots"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#f8f8f8"},
            "icon": {"color": "#02ab21", "font-size": "calc(16px + 0.5vw)"},
            "nav-link": {
                "font-size": "calc(14px + 0.5vw)",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#eee",
                "transition": "background-color 0.3s ease",
            },
            "nav-link-selected": {"background-color": "#02ab21"},
        },
    )
    if selected == "Home":
        st.markdown(f'<p class="big-font">SYED SHAHID NAZEER</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="medium-font">{role.upper()}</p>', unsafe_allow_html=True)
        
        if role == "Data Analyst":
            st.markdown('<p class="small-font">Experienced Data Analyst with a strong foundation in statistical analysis, data visualization, and business intelligence. Skilled in transforming complex datasets into actionable insights to drive data-informed decision-making.</p>', unsafe_allow_html=True)
        elif role == "Data Scientist":
            st.markdown('<p class="small-font">Innovative Data Scientist with expertise in machine learning, predictive modeling, and advanced analytics. Passionate about leveraging data to solve complex problems and drive business value.</p>', unsafe_allow_html=True)
        else:  # Python Developer
            st.markdown('<p class="small-font">Skilled Python Developer with a strong background in software engineering principles and best practices. Experienced in developing efficient, scalable, and maintainable code for various applications.</p>', unsafe_allow_html=True)
        
        st.subheader("Education")
        st.write("B.Tech - CSE, Annamacharya Institute Of Technology & Sciences, Kadapa")
        st.write("August 2018 - August 2022")
        st.write("CGPA: 6.98 | Final Semester SGPA: 9.18")
        
        st.plotly_chart(create_education_chart(), use_container_width=True)

                # *** Radar Chart ***
        skills_data = pd.DataFrame({
            'Skill': ['Python', 'SQL', 'Data Viz', 'Machine Learning', 'Communication'],
            'Proficiency': [90, 85, 95, 80, 75]
        })
        fig = px.line_polar(skills_data, r='Proficiency', theta='Skill', line_close=True, 
                            title="Technical Skill Proficiency")
        fig.update_traces(fill='toself')
        st.plotly_chart(fig)

        st.subheader("My Journey (Animated)")

        # Create the DataFrame
        df = pd.DataFrame({
            'Year': [2019, 2020, 2021, 2022, 2023],
            'Python': [70, 80, 90, 92, 95],
            'SQL': [60, 75, 80, 85, 88],
            'Data Viz': [50, 65, 80, 85, 90]
        })

        # Create the figure
        fig = go.Figure()

        # Add traces for each skill
        for skill in ['Python', 'SQL', 'Data Viz']:
            fig.add_trace(
                go.Bar(
                    x=df[skill], 
                    y=[skill],
                    orientation='h',
                    name=skill
                )
            )

        # Create frames for animation
        frames = []
        for year in df['Year']:
            frame = go.Frame(
                data=[go.Bar(x=df.loc[df['Year'] == year, skill], y=[skill]) for skill in ['Python', 'SQL', 'Data Viz']],
                name=str(year)
            )
            frames.append(frame)

        fig.frames = frames

        # Update layout
        fig.update_layout(
            title='Skills Progression Over Years',
            xaxis=dict(range=[0, 100], title='Skill Level'),
            yaxis=dict(title='Skill'),
            updatemenus=[dict(
                type='buttons',
                showactive=False,
                buttons=[dict(
                    label='Play',
                    method='animate',
                    args=[None, dict(
                        frame=dict(duration=1000, redraw=True),
                        fromcurrent=True,
                        transition=dict(duration=300, easing='quadratic-in-out')
                    )]
                )]
            )],
            sliders=[dict(
                steps=[
                    dict(
                        method='animate',
                        args=[[f.name], dict(
                            mode='immediate',
                            frame=dict(duration=300, redraw=True),
                            transition=dict(duration=300)
                        )],
                        label=f.name
                    )
                    for f in frames
                ],
                transition=dict(duration=300),
                x=0,
                y=0,
                currentvalue=dict(visible=True, prefix='Year: ', xanchor='right', font=dict(size=20, color='#666'))
            )]
        )

        # Show the plot
        st.plotly_chart(fig, use_container_width=True)

        display_work_experience()

        st.write("Let's connect! Choose your preferred platform:")

        col1, col2, col3 = st.columns(3) 
        with col1:
            if st.button("LinkedIn"):
                st.markdown("[Visit my LinkedIn Profile](https://www.linkedin.com/in/yourprofile)") 
        with col2:
            if st.button("GitHub"):
                st.markdown("[Check out my GitHub](https://github.com/yourusername)") 
        with col3:
            if st.button("Twitter"):
                st.markdown("[Follow me on Twitter](https://twitter.com/yourhandle)")

    elif selected == "Skills":
        st.header(f"Skills & Expertise - {role}")

        # *** Radar Charts for Skills (Role-Specific) ***
        if role == "Data Analyst":
            skills_data = pd.DataFrame({
                'Skill': ['SQL', 'Excel', 'Data Viz', 'Statistical Analysis', 'BI Tools'],
                'Proficiency': [85, 90, 80, 85, 75] 
            })
        elif role == "Data Scientist":
            skills_data = pd.DataFrame({
                'Skill': ['Python', 'ML', 'Deep Learning', 'NLP', 'Big Data'],
                'Proficiency': [90, 85, 80, 75, 70]
            })
        else:  # Python Developer
            skills_data = pd.DataFrame({
                'Skill': ['Python', 'Django', 'Flask', 'API Dev', 'Databases'],
                'Proficiency': [95, 80, 75, 85, 80]
            })

        fig = px.line_polar(skills_data, r='Proficiency', theta='Skill', line_close=True, 
                            title=f"{role} Skill Proficiency")
        fig.update_traces(fill='toself')
        st.plotly_chart(fig)

        if role == "Data Analyst":
            skills_data = pd.DataFrame({
                'Skill': ['SQL', 'Excel', 'Data Visualization', 'Statistical Analysis', 'Business Intelligence'],
                'Proficiency': [85, 90, 80, 85, 75],
                "Description": [
                    "Strong SQL skills for querying and data manipulation.",
                    "Proficient in Excel for data analysis and reporting.",
                    "Experienced with data visualization tools like Tableau and Power BI.",
                    "Solid understanding of statistical analysis techniques.",
                    "Knowledge of business intelligence concepts and tools."
                ]
            })
            additional_skills = ["Power BI", "Tableau", "Data Cleaning", "ETL Processes", "A/B Testing"]
        elif role == "Data Scientist":
            skills_data = pd.DataFrame({
                'Skill': ['Python', 'Machine Learning', 'Deep Learning', 'NLP', 'Big Data'],
                'Proficiency': [90, 85, 80, 75, 70],  
                "Description": [
                    "Proficient in Python for data analysis, scripting, and machine learning.",
                    "Strong understanding of machine learning algorithms and techniques.",
                    "Experience with deep learning frameworks like TensorFlow and PyTorch.",
                    "Knowledge of Natural Language Processing (NLP) concepts and libraries.",
                    "Familiar with big data technologies and tools." 
                ]
            })
            additional_skills = ["TensorFlow", "PyTorch", "Time Series Analysis", "Feature Engineering", "Cloud Computing (AWS/GCP)"]
        else:  # Python Developer
            skills_data = pd.DataFrame({
                'Skill': ['Python', 'Django', 'Flask', 'API Development', 'Database Design'],
                'Proficiency': [95, 80, 75, 85, 80],  
                "Description": [
                    "Expert in Python programming language and its ecosystem.",
                    "Experienced with Django framework for building web applications.",
                    "Familiar with Flask framework for developing web services and APIs.",
                    "Strong understanding of API development principles (RESTful APIs).",
                    "Proficient in database design and SQL."
                ]
            })
            additional_skills = ["RESTful APIs", "Docker", "Git", "Agile Methodologies", "Test-Driven Development"]

        fig = px.bar(skills_data, 
                    x='Skill', 
                    y='Proficiency', 
                    title=f'Core Skills - {role}',
                    labels={'Proficiency': 'Proficiency Level'},
                    color='Proficiency',
                    color_continuous_scale='Viridis', 
                    hover_data=['Description'],
                    )
        fig.update_traces(hovertemplate='Skill: %{x}<br>Proficiency: %{y}%<br>Description: %{customdata[0]}')
        st.plotly_chart(fig, use_container_width=True)

                # *** Heatmap for Skill Proficiency (alternative to Radar Chart) ***
        st.subheader("My Skills Over Time")

        # Create the DataFrame for skills progression
        df = pd.DataFrame({
            'Year': [2019, 2020, 2021, 2022, 2023] * 3,  # Repeat years for each skill
            'Skill': ['Python'] * 5 + ['SQL'] * 5 + ['Data Viz'] * 5,
            'Proficiency': [70, 80, 90, 92, 95, 60, 75, 80, 85, 88, 50, 65, 80, 85, 90],
            'Area': ['Backend'] * 5 + ['Data'] * 5 + ['Frontend'] * 5 
        })

        # Create the animated scatter plot
        fig = px.scatter(df, x='Skill', y='Proficiency', 
                        size='Proficiency', color='Skill', 
                        animation_frame="Year", animation_group="Skill",
                        size_max=50, # Adjust bubble size
                        range_y=[0,100], # Adjust y-axis range
                        title="Skills Growth Over Time",
                        labels={"Proficiency": "Skill Level"} # Customize labels
                        )

        # Customize the animation
        fig.update_layout(
            updatemenus=[dict(
                type='buttons',
                showactive=False,
                buttons=[dict(
                    label='Play',
                    method='animate',
                    args=[None, dict(frame=dict(duration=1000, redraw=True), 
                                    transition=dict(duration=500),
                                    fromcurrent=True,
                                    mode='immediate')]
                )]
            )],
            xaxis=dict(title='Skill'),
            yaxis=dict(title='Proficiency'),
            height=600,
            width=800
        )

        # Improve layout
        fig.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        # Display the chart
        st.plotly_chart(fig, use_container_width=True)

        # Additional Skills (Using tags)
        st.subheader("Additional Skills")
        for skill in additional_skills:
            st.markdown(f'<span class="skill-tag">{skill}</span>', unsafe_allow_html=True) 

        # CSS for skill tags
        st.markdown(
            """
            <style>
            .skill-tag {
                background-color: #f2f2f2;
                padding: 5px 10px;
                border-radius: 5px;
                margin-right: 5px;
                margin-bottom: 5px;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        
        create_skills_network(role)

    elif selected == "Projects":
        st.header(f"Projects - {role}")
        st.subheader("Explore My Work")

        if role == "Data Analyst":
            projects = {
                        "Sales Dashboard Creation": """
                        - **Project Overview:** Imagine a symphony of sales data—revenue notes, customer crescendos, and profit harmonies. That’s what our Sales Dashboard Creation is all about.
                        - **The Challenge:** Our sales team needed a compass—a dashboard that would guide them through the labyrinth of metrics. Enter Power BI, our maestro.
                        - **The Crescendo:** We composed interactive dashboards that danced with KPIs: revenue trends pirouetting, conversion rates waltzing, and customer churn doing the cha-cha.
                        - **The Encore:** Efficiency soared by 15%, like a soprano hitting a high note. Our sales team? They became virtuosos, armed with insights and ready to conquer markets.
                        """,
                        "Customer Segmentation Analysis": """
                        - **Project Prelude:** Picture a kaleidoscope of customer data—purchase histories, demographics, and behavioral quirks. Our mission? Unravel the patterns.
                        - **The Clusters:** We donned our Sherlock hats and performed cluster analysis. Voilà! Customer segments emerged: the Loyal Larks, the Bargain Hunters, and the Impulse Buyers.
                        - **The Marketing Sonata:** Armed with insights, marketing campaigns became laser-focused. Personalized emails serenaded the Loyal Larks, while flash sales beckoned the Impulse Buyers.
                        - **The Standing Ovation:** Customer retention swirled like a waltz—up by 10%. The audience (read: stakeholders) cheered. Encore, please!
                        """,
                        "Supply Chain Optimization": """
                        - **Project Prelude (in Minor Key):** Our supply chain resembled rush hour traffic—bottlenecks, detours, and missed deliveries. Chaos reigned.
                        - **The Data Expedition:** Armed with logistics data, we embarked on a quest. Our goal? Efficiency nirvana.
                        - **The Hidden Paths:** We analyzed routes, inventory levels, and lead times. Inefficiencies trembled. Bottlenecks quivered.
                        - **The Symphony of Savings:** Logistics costs bowed out gracefully—down by 8%. Our supply chain? Now a well-choreographed ballet, pirouetting toward cost-effectiveness.
                        """
                    }
        elif role == "Data Scientist":
            projects = {
                        "Rating Prediction of Google Play Store Apps Using Data Mining Techniques": """
                        - **Project Prelude (in Data Science Symphony):** Imagine a bustling app store, a sea of apps vying for attention. Developers struggle to understand what makes an app soar to the top, or why some crash and burn.  Our mission?  Unlock the secrets of app success using data.
                        - **The Algorithm's Maestro:** We donned our data scientist hats and conducted a symphony of data mining. Over 100,000 apps, their reviews, features, and categories, became our musical score.  We trained our algorithms on this vast orchestra of data, seeking the hidden patterns that predict app success.
                        - **The Rating's Crescendo:**  Our model, like a maestro conducting an orchestra, predicted app ratings with 93% accuracy. Developers, armed with this knowledge, could now compose apps that resonated with users. It was a concerto of data-driven app development, leading to increased downloads and higher rankings.
                        - **The Standing Ovation:** The app store's stage was now illuminated by data-driven decisions, as developers composed apps that captivated users, achieving greater success and making the app store a truly harmonious experience.
                        """,
                        "Real-Time News Verification Web App": """
                        - **Project Prelude (in Digital Journalism's Dilemma):**  Picture a world awash in information, but where truth is increasingly elusive.  Fake news spreads like wildfire, leaving people confused and questioning reality. Our mission?  To build a beacon of truth in a digital sea of misinformation.
                        - **The NLP's Sleuth:**  We crafted a web app powered by advanced NLP, trained on over 80,000 articles. It became our digital detective, analyzing the language of news stories, seeking inconsistencies and identifying telltale signs of fakery.
                        - **The Verification Tango:** This web app, like a swift and accurate dance, could verify the authenticity of news within milliseconds.  It eliminated the time-consuming and often inaccurate manual verification process, empowering users to trust the news they consume.
                        - **The Spotlight on Truth:**  Our app became a spotlight, shining brightly on the truth in a world saturated with misinformation.  Users could now confidently navigate the digital landscape, knowing they had access to reliable and verified news.
                        """,
                        "Oil Price Prediction Application": """
                        - **Project Prelude (in Energy Market's Volatility):**  Imagine a global market where the price of oil can fluctuate wildly, throwing businesses and economies into turmoil.  Our mission?  To tame the chaos and bring predictability to the oil industry.
                        - **The Data's Oracle:**  We delved into over 35 years of historical oil price data, a vast collection of numbers representing the ebb and flow of the energy market. We trained our predictive models on this vast dataset, seeking the patterns that could unlock the secrets of oil price fluctuations.
                        - **The Prediction's Compass:** Our application, like a skilled navigator charting the course through stormy seas, provided oil price forecasts with a prediction variance of just 1.2% to 2%. This gave businesses and investors a valuable tool for strategic planning and decision-making in the volatile oil market.
                        - **The Oil Industry's Stability:** The oil industry, once plagued by unpredictable price swings, now had a valuable tool to navigate the market effectively. Our app brought stability and confidence to an industry that had long faced volatility, enabling better decision-making and fostering growth. 
                        """
                    }

        else:  # Python Developer
            projects = {
                        "E-commerce Platform Development": """
                        - **Project Prelude:** Imagine an online marketplace—the hustle, the clicks, the virtual cash registers ringing. Our mission? To build a platform that could handle the shopping frenzy.
                        - **The Django Symphony:** We donned our developer capes and danced with Django. Scalability was our muse, and we crafted an e-commerce wonderland. Product listings pirouetted, carts cha-chaed, and checkout flows waltzed.
                        - **The Sales Crescendo:** Online sales soared—up by 50%. Customers clicked, bought, and left with virtual shopping bags full of joy. Our platform? The grand stage for this retail ballet.
                        """,
                        "API Integration Service": """
                        - **Project Prelude (in Microservice Notes):** Picture a data orchestra—each service playing its part, harmonizing like well-tuned instruments. But what if these services spoke different languages? Chaos, my friend.
                        - **The Polyglot Maestro:** We composed a microservice-based API integration platform. REST, GraphQL, SOAP—they all bowed to our conductor. Data flowed seamlessly, like a symphony in sync.
                        - **The Tempo Accelerando:** Data processing time? Reduced by 60%. Our platform? The bridge connecting disparate systems. APIs high-fived, and business logic danced a jig.
                        """,
                        "Automated Testing Framework": """
                        - **Project Prelude (in Code Coverage Notes):** Imagine a codebase—the notes, the harmonies, the occasional dissonance (read: bugs). Our mission? To ensure every note played true.
                        - **The Testing Sonata:** We composed a comprehensive testing framework. Unit tests, integration tests, end-to-end tests—they swirled like musical motifs. Code coverage climbed, bugs trembled.
                        - **The Bug-Free Finale:** Bug reports? Down by 30%. Our framework? The vigilant conductor, ensuring every line of code sang its best. Developers smiled, users hummed along.
                        """
                    }

        # Create Project Impact Data 
        project_impact_data = pd.DataFrame({
            'Project': list(projects.keys()),
            'Impact': [9, 8, 7]  # Replace with actual impact scores
        })

        for project, description in projects.items():
            col1, col2 = st.columns([1, 3]) 
            with col1:
                with st.container():
                    st.markdown(f'<div class="project-card">', unsafe_allow_html=True)

                    # Construct the image file name from the project title
                    image_file = f"{project.lower().replace(' ', '_')}.jpg"  
                    image_path = os.path.join("project_images", image_file)
                    
                    if os.path.exists(image_path):
                        st.image(image_path, use_column_width=True)
                    else:
                        st.warning(f"Image not found: {image_path}")  # Display warning if image doesn't exist

                    st.markdown(f'<div class="overlay"><h3>{project}</h3></div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            with col2:
                with st.container():
                    st.markdown(f'<div class="project-card">', unsafe_allow_html=True)
                    st.subheader(project)
                    with st.expander("See Details"):
                        st.write(description)  # Display description on click
                        st.write("[Link to Project Repo/Demo]")  # Replace with actual link
                    st.markdown('</div>', unsafe_allow_html=True)

        # *** Replace Pie Chart with Bar Chart (Corrected) ***
        project_impact_data = pd.DataFrame({
            'Project': list(projects.keys()),
            'Impact': [9, 8, 7]  # Make sure this has the same length as projects.keys()
        })
        fig = px.bar(project_impact_data, x='Project', y='Impact', 
                    title="Project Impact", color_discrete_sequence=["#00CC96"])
        st.plotly_chart(fig, use_container_width=True)

        # Create a dictionary of project titles and frequencies
        project_frequencies = {
            "Sales Dashboard": 15,
            "Customer Segmentation": 12,
            "Supply Chain Optimization": 8,
            # ... add more projects and frequencies
        }
        # Sample Project Data (Replace with your own)
        data = {
            "nodes": [
                {"id": "Project A", "group": "Data Science"},
                {"id": "Project B", "group": "Web Dev"},
                {"id": "Project C", "group": "Data Science"},
                {"id": "Project D", "group": "Data Viz"},
                {"id": "Project E", "group": "Web Dev"},
            ],
            "edges": [
                {"source": "Project A", "target": "Project C", "label": "Shared Data"},
                {"source": "Project B", "target": "Project E", "label": "Same Framework"},
                {"source": "Project A", "target": "Project D", "label": "Visualization"},
                {"source": "Project C", "target": "Project D", "label": "Visualization"},
            ]
        }
                # Create a Pyvis network graph
        net = Network(height="600px", width="100%", notebook=True, heading="Project Connections")

        # Add nodes with groups
        for node in data["nodes"]:
            net.add_node(node["id"], group=node["group"])

        # Add edges with labels
        for edge in data["edges"]:
            net.add_edge(edge["source"], edge["target"], title=edge["label"])

        # Configure interactivity options
        net.set_options("""
        const options = {
        "physics": {
            "enabled": true,
            "barnesHut": {
            "gravitationalConstant": -2000,
            "centralGravity": 0.3,
            "springLength": 95,
            "springConstant": 0.04,
            "damping": 0.09
            },
            "maxVelocity": 50,
            "minVelocity": 0.1,
            "solver": "barnesHut",
            "timestep": 0.5
        },
        "nodes": {
            "font": {
            "size": 14
            }
        },
        "edges": {
            "smooth": {
            "enabled": true,
            "type": "dynamic"
            }
        },
        "interaction": {
            "hover": true,
            "tooltipDelay": 200,
            "navigationButtons": true
        }
        }
        """)

        # Save the graph as an HTML file
        net.save_graph("project_network.html")

        # Display the interactive graph in Streamlit
        st.components.v1.html(open("project_network.html", 'r').read(), height=650) 

        # Create DataFrame (or adapt from your existing project data)
        df_projects = pd.DataFrame({
            'Project': ['Sales Dashboard', 'Customer Segmentation', 'Supply Chain Optimization'],
            'Frequency': [15, 12, 8]
        })

        fig = px.bar(df_projects, x='Project', y='Frequency', title='Project Frequencies',
                    color='Frequency', color_continuous_scale='Viridis')
        st.plotly_chart(fig, use_container_width=True)

    elif selected == "Contact":
        st.header("Contact")

        st.write("Phone: +91-9912357968")
        st.write("Email: shahidnazeerds@gmail.com")
        st.write("Location: Hyderabad, India")
        st.write("[LinkedIn Profile](https://www.linkedin.com/in/yourprofile)") 

        with st.form("contact_form"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            message = st.text_area("Message")
            submit_button = st.form_submit_button("Send Message")

        if submit_button:
            if name and email and message:
                st.success("Thanks for your message! I'll get back to you soon.")
            else:
                st.warning("Please fill in all fields before submitting.")

        # Resume and Cover Letter Section (Now below the contact form)
        st.subheader("Resume & Cover Letter")

        document_choice = st.radio(
            "Select document to view",
            options=["Resume", "Cover Letter"]
        )

        if document_choice == "Resume":
            file_path = os.path.join("resume", f"{role.lower().replace(' ', '_')}_resume.pdf")
            file_label = f"{role} Resume"
        else:
            file_path = os.path.join("resume", f"{role.lower().replace(' ', '_')}_cover_letter.pdf")
            file_label = f"{role} Cover Letter"

        try:
            # Display the PDF
            display_pdf(file_path)  

            # Add download button
            st.markdown(get_binary_file_downloader_html(file_path, file_label), unsafe_allow_html=True)

        except FileNotFoundError:
            st.error(f"The {file_label} file was not found. Please check if the file exists in the 'resume' folder.")


    elif selected == "Chat Bot":
        chatbot()

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.write("© 2024 Syed Shahid Nazeer")
    with col2:
        background_type = st.selectbox("Choose background type", ["Static", "Dynamic"])
        if background_type == "Dynamic":
            set_background("background.gif", is_gif=True)

if __name__ == "__main__":
    main()