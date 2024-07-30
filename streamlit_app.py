import streamlit as st
import plotly.express as px
import pandas as pd
import os
import base64
import PyPDF2 as pdf
import json
import ast
import re 
from streamlit_option_menu import option_menu
import google.generativeai as genai

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

def create_project_impact_chart():
    project_data = pd.DataFrame({
        'Project': ['App Rating Prediction', 'Fake News Detection', 'Oil Price Prediction'],
        'Impact Score': [93, 85, 88]
    })
    
    fig = px.pie(project_data, values='Impact Score', names='Project', 
                 title='Project Impact',
                 hole=0.3)
    return fig

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
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    input_text = st.text_input("Input: ", key="input")
    submit = st.button("Ask the question")

    if submit and input_text:
        response = generate_response(input_text)
        
        # Add user query to chat history
        st.session_state['chat_history'].append(("You", input_text))  
        
        st.subheader("The Response is:")
        for chunk in response:
            st.write(chunk.text, end='') # Print the response chunk by chunk
            st.session_state['chat_history'].append(("Bot", chunk.text)) # Add to history

    st.subheader("The Chat History is:")
    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")
# Chatbot Selection
def chatbot():
    bot_choice = st.selectbox(
        "Select a Chatbot:",
        ["Thesis Writer Assistant", "Resume ATS Score Bot", "Code Explainer Bot", "Healerbeast (BFF)", "Q&A Bot"]
    )

    if bot_choice == "Thesis Writer Assistant":
        thesis_writer_assistant()
    elif bot_choice == "Resume ATS Score Bot":
        resume_ats_score_bot()
    elif bot_choice == "Code Explainer Bot":
        code_explainer_bot()
    elif bot_choice == "Healerbeast (BFF)":
        healerbeast_bff()
    elif bot_choice == "Q&A Bot":
        qanda_bot()  # Call the Q&A bot function

def main():
    st.set_page_config(page_title="SYED SHAHID NAZEER - Portfolio", layout="wide")

    # Responsive CSS
    st.markdown("""
    <style>
    .big-font {font-size:calc(30px + 2vw) !important; color: #4A4A4A;}
    .medium-font {font-size:calc(20px + 1vw) !important; color: #4A4A4A;}
    .small-font {font-size:calc(16px + 0.5vw) !important; color: #4A4A4A;}
    .stSelectbox {max-width: 300px;}
    @media (max-width: 768px) {
        .responsive-container {
            flex-direction: column;
        }
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

        # Add an interactive element
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

    elif selected == "Projects":
        st.header(f"Projects - {role}")
        
        if role == "Data Analyst":
            projects = {
                "Sales Dashboard Creation": 
                    "Developed interactive Power BI dashboards to visualize key sales metrics, resulting in a 15% increase in sales team efficiency.",
                "Customer Segmentation Analysis": 
                    "Performed cluster analysis on customer data to identify key segments, leading to targeted marketing campaigns and a 10% increase in customer retention.",
                "Supply Chain Optimization": 
                    "Analyzed supply chain data to identify inefficiencies, resulting in a 8% reduction in logistics costs."
            }
        elif role == "Data Scientist":
            projects = {
                "Predictive Maintenance Model": 
                    "Developed a machine learning model to predict equipment failures, reducing downtime by 25% and maintenance costs by 20%.",
                "Natural Language Processing for Customer Support": 
                    "Created an NLP model to automate customer support ticket classification, improving response times by 40%.",
                "Fraud Detection System": 
                    "Implemented an advanced anomaly detection system, resulting in a 30% increase in fraud detection rates."
            }
        else:  # Python Developer
            projects = {
                "E-commerce Platform Development": 
                    "Led the development of a scalable e-commerce platform using Django, resulting in a 50% increase in online sales.",
                "API Integration Service": 
                    "Developed a microservice-based API integration platform, reducing data processing time by 60%.",
                "Automated Testing Framework": 
                    "Created a comprehensive automated testing framework, increasing code coverage by 40% and reducing bug reports by 30%."
            }
        
        for project, description in projects.items():
            st.subheader(project)
            st.write(description)
        
        st.plotly_chart(create_project_impact_chart(), use_container_width=True)

        # Add a project filter
        project_filter = st.multiselect("Filter projects by type", ["Data Analysis", "Machine Learning", "Web Development"])
        st.write(f"Showing projects related to: {', '.join(project_filter)}")

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