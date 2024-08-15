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
from streamlit_lottie import st_lottie
import google.generativeai as genai

# Streamlit imports
import streamlit as st

# InBuilt Functions Import
from chatbots import (thesis_writer_assistant, resume_ats_score_bot,
                      code_explainer_bot, healerbeast_bff, qanda_bot,
                      transcription_bot, chatbot)
from utils import (load_lottieurl, display_lottie, display_pdf,
                   get_binary_file_downloader_html, show_announcement,show_video,
                   set_background, contact_section, display_resume_section)
from charts import (create_chart, create_education_chart, display_work_experience,
                    create_skills_chart, create_project_impact_chart,
                    create_radar_chart, create_bar_chart, create_heatmap_chart)
from networks import create_skills_network, create_project_network
from css import apply_indian_flag_animation_style,create_indian_flag_particles
from projects import get_projects
from skills import get_skills_data


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
    radar_chart = create_chart(skills_data,
                               'line_polar',
                               title="Technical Skill Proficiency",
                               theta='Skill',
                               line_close=True)
    radar_chart.update_traces(fill='toself')
    st.plotly_chart(radar_chart, use_container_width=True)

    st.subheader("My Journey (Animated)")
    display_work_experience()

    st.write("Let's connect! Choose your preferred platform:")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            "[Visit my LinkedIn Profile](https://www.linkedin.com/in/yourprofile)"
        )
    with col2:
        st.markdown("[Check out my GitHub](https://github.com/yourusername)")
    with col3:
        st.markdown("[Follow me on Twitter](https://twitter.com/yourhandle)")


def display_skills_section(role):
    st.header(f"Skills & Expertise - {role}")

    @st.cache_data
    def get_cached_skills_data(role):
        return get_skills_data(role)

    skills = get_cached_skills_data(role)
    skills_data = skills["skills_data"]
    additional_skills = skills["additional_skills"]

    radar_chart = create_radar_chart(skills_data, "Data Scientist")
    st.plotly_chart(radar_chart, use_container_width=True)

    bar_chart = create_bar_chart(skills_data, "Data Scientist")
    st.plotly_chart(bar_chart, use_container_width=True)

    st.subheader("Additional Skills")
    for skill in additional_skills:
        st.markdown(f'<span class="skill-tag">{skill}</span>',
                    unsafe_allow_html=True)

    create_skills_network(role)


def display_projects_section(role):
    st.header(f"Projects - {role}")
    st.subheader("Explore My Work")

    @st.cache_data
    def get_cached_projects(role):
        return get_projects(role)

    projects = get_cached_projects(role)

    def display_project_card(project, description, image_file):
        # ... (Code for project card remains the same)

        for project, description in projects.items():
            image_file = f"{project.lower().replace(' ', '_')}.jpg"
            display_project_card(project, description, image_file)

    create_project_network()
# Define your dictionary of messages
messages = {
    "welcome": "Welcome to my Digital Realm! Dive into the world of Data Insights, Tech Innovations, and Software Mastery.",
    "update": "New Feature: Interactive AI! Engage with an intelligent assistant for tech insights and more!",
    "reminder": "Don't forget to check out our latest projects and updates!",
    "announcement": "Big News! We're launching a new series of tutorials next week. Stay tuned!"
}

def main():
    st.set_page_config(page_title="SYED SHAHID NAZEER - Portfolio",
                       layout="wide")

    st.markdown("""
<style>
    body {
        background-color: #1a1a2e;
        color: #ff00ff; /* Set default text color to pink */
    }
    .stApp {
        max-width: 100%;
    }
    .stButton>button {
        background-color: #00ffff;
        color: #1a1a2e;
        border: 2px solid #ff00ff;
        border-radius: 5px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #ff00ff;
        color: #00ffff;
        border-color: #00ffff;
        box-shadow: 0 0 15px #ff00ff;
    }
    /* Apply neon effect to navbars */
    .option-menu .nav-link {
        text-shadow: 0 0 5px #ff00ff, 0 0 10px #ff00ff; /* Pink neon glow */
        transition: all 0.3s ease;
    }
    .option-menu .nav-link:hover,
    .option-menu .nav-link-selected {
        text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff; /* Cyan neon glow */
    }
    .option-menu .nav-link-selected {
        background-color: #331a4d; /* Dark purple background for selected item */
    }
</style>
""", unsafe_allow_html=True)

    st.markdown(
        """
        <link rel="stylesheet" href="styles.css">
        """,
        unsafe_allow_html=True,
    )

    role = option_menu(menu_title=None,
                       options=["Data Analyst", "Data Scientist",
                                "Python Developer"],
                       icons=["bar-chart-fill", "gear-fill", "code-slash"],
                       menu_icon="cast",
                       default_index=0,
                       orientation="horizontal",
                       styles={
                           "container": {
                               "padding": "0!important",
                               "background-color": "rgba(250, 250, 250, 0.8)"
                           },
                           "icon": {
                               "color": "orange",
                               "font-size": "calc(16px + 0.5vw)"
                           },
                           "nav-link": {
                               "font-size": "calc(14px + 0.5vw)",
                               "text-align": "left",
                               "margin": "0px",
                               "--hover-color": "#eee"
                           },
                           "nav-link-selected": {
                               "background-color": "#02ab21"
                           },
                       })

    background_images = {
        "Data Analyst": "data_analyst_bg.jpg",
        "Data Scientist": "data_scientist_bg.jpg",
        "Python Developer": "python_developer_bg.jpg"
    }
    set_background(background_images[role])

    selected = option_menu(menu_title=None,
                       options=["Home", "Skills", "Projects", "Contact",
                                "Chat Bot"],
                       icons=["house", "gear", "code-slash", "envelope",
                              "chat-dots"],
                       menu_icon="cast",
                       default_index=0,
                       orientation="horizontal",
                       styles={
                           "container": {
                               "padding": "0!important",
                               "background-color": "rgba(250, 250, 250, 0.8)"
                           },
                           "icon": {
                               "color": "orange",
                               "font-size": "calc(16px + 0.5vw)"
                           },
                           "nav-link": {
                               "font-size": "calc(14px + 0.5vw)",
                               "text-align": "left",
                               "margin": "0px",
                               "--hover-color": "#eee"
                           },
                           "nav-link-selected": {
                               "background-color": "#02ab21"
                           },
                       })

    # Function to encode video file to base64
    def encode_video(video_path):
        with open(video_path, "rb") as video_file:
            video_bytes = video_file.read()
        return base64.b64encode(video_bytes).decode()

    # Select a random message from the dictionary
    selected_message = random.choice(list(messages.values()))

    # Encode the video file
    encoded_video = encode_video("Independence day.mp4")

    # Display the video
    show_video(encoded_video)

    # Display the announcement
    show_announcement(selected_message)

    # Remove extra container and display selected section directly
    if selected == "Home":
        display_home_section(role)
    elif selected == "Skills":
        display_skills_section(role)
    elif selected == "Projects":
        display_projects_section(role)
    elif selected == "Contact":
        contact_section(role)
    elif selected == "Chat Bot":
        chatbot()

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.write("© 2024 Syed Shahid Nazeer")
    with col2:
        background_type = st.selectbox("Choose background type",
                                       ["Static", "Dynamic"],
                                       key="background_select")
        if background_type == "Dynamic":
            set_background("background.gif", is_gif=True)
if __name__ == "__main__":
    main()