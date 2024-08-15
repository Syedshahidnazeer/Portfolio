import os
import time
import tempfile
import random
import ast
import base64
import re
import uuid

# Third-party library imports
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from pydub import AudioSegment
from fpdf import FPDF
from moviepy.editor import *
import PyPDF2 as pdf
import yaml
from pyvis.network import Network
from streamlit_option_menu import option_menu
import hydralit_components as hc
from streamlit_lottie import st_lottie
import google.generativeai as genai

# Streamlit imports
import streamlit as st

# InBuilt Functions Import
from chatbots import (thesis_writer_assistant, resume_ats_score_bot,
                      code_explainer_bot, healerbeast_bff, qanda_bot,
                      transcription_bot, chatbot)
from utils import (load_lottieurl, display_lottie, display_pdf,local_css,
                   get_binary_file_downloader_html, show_announcement,show_video,
                   set_background, contact_section, display_resume_section)
from charts import (create_chart, create_education_chart, display_work_experience,
                    create_skills_chart, create_project_impact_chart,
                    create_radar_chart, create_bar_chart, create_heatmap_chart)
from networks import create_skills_network, create_project_network
from projects import get_projects
from skills import get_skills_data
from analysis import data_analysis_page
from science import data_science_page


def display_home_section(role):
    role_descriptions = {
        "Data Analyst": '<p class="small-font">Experienced Data Analyst with a strong foundation in statistical analysis, data visualization, and business intelligence. Skilled in transforming complex datasets into actionable insights to drive data-informed decision-making.</p>',
        "Data Scientist": '<p class="small-font">Innovative Data Scientist with expertise in machine learning, predictive modeling, and advanced analytics. Passionate about leveraging data to solve complex problems and drive business value.</p>',
        "Python Developer": '<p class="small-font">Skilled Python Developer with a strong background in software engineering principles and best practices. Experienced in developing efficient, scalable, and maintainable code for various applications.</p>'
    }
    st.markdown(role_descriptions.get(role, ""), unsafe_allow_html=True)

    st.subheader("Education")
    st.write(
        "B.Tech - CSE, Annamacharya Institute Of Technology & Sciences, Kadapa"
    )
    st.write("August 2018 - August 2022")
    st.write("CGPA: 6.98 | Final Semester SGPA: 9.18")

    education_chart = create_education_chart()
    st.plotly_chart(education_chart, use_container_width=True)

    skills_data = pd.DataFrame({
        'Skill': ['Python', 'SQL', 'Data Viz', 'Machine Learning', 'Communication'],
        'Proficiency': [90, 85, 95, 80, 75]
    })

    # Create the radar chart
    fig = px.line_polar(
        skills_data,
        r='Proficiency',
        theta='Skill',
        line_close=True,
        title="Technical Skill Proficiency"
    )

    # Customize the chart
    fig.update_traces(fill='toself')
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        )
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("My Journey (Animated)")
    display_work_experience()

    st.write("Let's connect! Choose your preferred platform:")
    col1, col2 = st.columns(2)

    with col1:
        st.image("images/linkedin_logo.png", width=600)
        st.markdown("[LinkedIn Profile](https://www.linkedin.com/in/shahidnazeersyed/)")

    with col2:
        st.image("images/github_logo.png", width=700)
        st.markdown("[GitHub Profile](https://github.com/Syedshahidnazeer)")


def display_skills_section(role):
    st.header(f"Skills & Expertise - {role}")

    @st.cache_data
    def get_cached_skills_data(role):
        return get_skills_data(role)  # Use your get_skills_data function

    skills = get_cached_skills_data(role)
    skills_data = skills["skills_data"]
    additional_skills = skills["additional_skills"]

    radar_chart = create_radar_chart(skills_data, role)
    st.plotly_chart(radar_chart, use_container_width=True)

    bar_chart = create_bar_chart(skills_data, role)  # Pass the 'role' parameter
    st.plotly_chart(bar_chart, use_container_width=True)

    st.subheader("Additional Skills")
    for skill in additional_skills:
        st.markdown(f'<span class="skill-tag">{skill}</span>',
                    unsafe_allow_html=True)

    create_skills_network(role)


def display_projects_section(role):

    st.header(f"Projects - {role}")
    st.subheader("Explore My Work")
    # Custom CSS for animations and styling
    st.markdown("""
    <style>
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    .project-card {
        animation: fadeIn 0.5s ease-in;
        transition: all 0.3s ease;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .project-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }
    .project-title {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

    @st.cache_data
    def get_cached_projects(role):
        return get_projects(role)

    projects = get_cached_projects(role)

    def display_project_card(project, description, image_file):
        """Displays a project card with an image overlay and description."""
        col1, col2 = st.columns([1, 3])

        with col1:
            with st.container():
                st.markdown(
                    f'<div class="project-card">',
                    unsafe_allow_html=True,
                )

                image_path = os.path.join("project_images", image_file)

                if os.path.exists(image_path):
                    st.image(image_path, use_column_width=True)
                else:
                    st.warning(f"Image not found: {image_path}")

                # Add overlay with project title
                st.markdown(
                    f'<div class="overlay"><h3>{project}</h3></div>',
                    unsafe_allow_html=True,
                )
                st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            with st.container():
                st.markdown(
                    f'<div class="project-card">',
                    unsafe_allow_html=True,
                )
                with st.expander("See Details"):
                    st.write(description)
                    st.write("[Link to Project Repo/Demo]")  # Replace with actual link
                st.markdown("</div>", unsafe_allow_html=True)

    # Call display_project_card for each project (outside the function definition)
    for project, description in projects.items():
        image_file = f"{project.lower().replace(' ', '_')}.jpg"
        display_project_card(project, description, image_file) 

    create_project_network()
messages = [
    "Welcome to my Digital Realm!",
    "Explore my latest projects and skills!",
    "Don't forget to check out the Chat Bot!",
    "Thanks for visiting my portfolio!"
]

def main():
    st.set_page_config(
        page_title="SYED SHAHID NAZEER - Portfolio",
        page_icon=":bar_chart:",  # Add an icon
        layout="wide",
        initial_sidebar_state="collapsed"  # or "expanded"
    )
    st.markdown(
        """
        <style>
            body {
                background-color: #1f1f1f; /* Dark background */
                color: #ffffff; /* White text for general content */
            }
            h1, h2, h3, h4, h5, h6, p { /* Target headings and paragraphs */
                color: black;
            }
            .stApp {
                max-width: 100%; 
            }
            .stButton > button {
                background-color: #7400b8;  /* Purple button */
                color: white;
                border: none;
                border-radius: 5px; 
                transition: all 0.3s ease; 
            }
            .stButton>button:hover {
                background-color: #ffffff; /* White on hover */
                color: #7400b8; 
                box-shadow: 0 0 10px #7400b8; /* Purple glow */
            }
            .skill-tag { 
                background-color: #7400b8;
                color: white;
                padding: 5px 10px;
                border-radius: 5px;
                margin-right: 5px;
            } 
            /* ... Add more styles as needed ... */
        </style>
        """,
        unsafe_allow_html=True,
    )
    # Custom CSS for styling
    st.markdown(
        """
    <style>
        .stApp {
            background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%);
            color: white;
        }
        .stButton>button {
            color: white;
            background-color: rgba(255,255,255,0.1);
            border: 1px solid white;
        }
        .stButton>button:hover {
            background-color: rgba(255,255,255,0.2);
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Role Selection
    role_options = [
        {"icon": "bar-chart", "label": "Data Analyst"},
        {"icon": "graph-up", "label": "Data Scientist"},
        {"icon": "code-slash", "label": "Python Developer"}
    ]

    role = hc.option_bar(
        option_definition=role_options,
        override_theme={
            "background": "rgba(255,255,255,0.1)",
            "base": "light",
            "primaryColor": "#4b6cb7",
            "secondaryColor": "#182848",
            "font": "sans serif",
        },
        key="role_selector"
    )

    # Background Setting
    background_images = {
        "Data Analyst": "data_analyst_bg.jpg",
        "Data Scientist": "data_scientist_bg.jpg",
        "Python Developer": "python_developer_bg.jpg"
    }
    set_background(background_images[role])

    # Navigation
    nav_options = [
        {"icon": "gear", "label": "Skills"},
        {"icon": "code-slash", "label": "Projects"},
        {"icon": "envelope", "label": "Contact"},
        {"icon": "chat-dots", "label": "Chat Bot"},
        {"icon": "bar-chart-line", "label": "Data Analysis"},
        {"icon": "database", "label": "Data Science"}
    ]

    selected = hc.nav_bar(
        menu_definition=nav_options,
        override_theme={
            "background": "rgba(255,255,255,0.1)",
            "base": "light",
            "primaryColor": "#4b6cb7",
            "secondaryColor": "#182848",
            "font": "sans serif",
        },
        home_name="Home",
        sticky_nav=True,
        hide_streamlit_markers=True,
        sticky_mode="pinned",
        use_animation=True,
        key="main_nav"
    )
    with hc.HyLoader("Loading...", hc.Loaders.pacman):
        # Your code here
        time.sleep(2)

    # --- Function to encode video file to base64 ---
    def encode_video(video_path):
        with open(video_path, "rb") as video_file:
            video_bytes = video_file.read()
        return base64.b64encode(video_bytes).decode()
    # --- Encode the video file ---
    encoded_video = encode_video("Independence day.mp4")

    # --- Display the video ---
    show_video(encoded_video)

    show_announcement(messages)

    # --- Section Rendering ---
    if selected == "Home":
        display_home_section(role)
    elif selected == "Skills":
        display_skills_section(role)
    elif selected == "Projects":
        display_projects_section(role)
    elif selected == "Contact":
        local_css("contacts.css")
        contact_section(role)
    elif selected == "Chat Bot":
        chatbot()
    elif selected == "Data Analysis":
        data_analysis_page()
    elif selected == "Data Science":
        data_science_page()

    # --- Footer ---
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.write("© 2024 Syed Shahid Nazeer")
    with col2:
        background_type = st.selectbox("Choose background type", ["Static", "Dynamic"], key="background_select")
        if background_type == "Dynamic":
            set_background("background.gif", is_gif=True)

# Check if the user is on a mobile device
is_mobile = st.query_params.get("mobile", ["false"])[0] == "true"

# Adjust layout based on device
if is_mobile:
    st.markdown("""
    <style>
        .stApp {
            padding: 1rem;
        }
        .stButton>button {
            width: 100%;
            margin-bottom: 0.5rem;
        }
    </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()