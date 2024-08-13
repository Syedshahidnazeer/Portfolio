# Standard library imports
import os
import time
import tempfile
import random
import ast
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
                      code_explainer_bot,healerbeast_bff,qanda_bot,
                      transcription_bot,chatbot)
from utils import (load_lottieurl, display_lottie, display_pdf, 
                   get_binary_file_downloader_html, show_announcement,
                   set_background, contact_section, display_resume_section)
from charts import (create_chart, create_education_chart, display_work_experience,
                    create_skills_chart, create_project_impact_chart,
                    create_radar_chart, create_bar_chart, create_heatmap_chart)
from css import display_page_with_indian_flag_animation
from networks import create_skills_network,create_project_network
from projects import get_projects
from skills import get_skills_data


def main():  
    
    st.set_page_config(
    page_title="Syed Shahid Nazeer - Portfolio",
    layout="wide",
    initial_sidebar_state="expanded",  # Example: set sidebar to be expanded initially
)

    # Example usage
    display_page_with_indian_flag_animation("Home")
    
    show_announcement("🎉 New feature alert: Thesis Writer Assistant now available!")

    # Role Selection
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
            "nav-link": {"font-size": "calc(14px + 0.5vw)", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#02ab21"},
        },
        key="role_menu"
    )

    # Update session state with the selected role
    st.session_state.selectedRole = role

    # Set Background
    background_images = {
        "Data Analyst": "data_analyst_bg.jpg",
        "Data Scientist": "data_scientist_bg.jpg",
        "Python Developer": "python_developer_bg.jpg"
    }
    background_image = background_images.get(role, "default_bg.jpg")
    set_background(background_image)

    # Main Navigation
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
        key="main_menu"
    )

    if selected == "Home":
        role_descriptions = {
            "Data Analyst": '<p class="small-font">Experienced Data Analyst with a strong foundation in statistical analysis, data visualization, and business intelligence. Skilled in transforming complex datasets into actionable insights to drive data-informed decision-making.</p>',
            "Data Scientist": '<p class="small-font">Innovative Data Scientist with expertise in machine learning, predictive modeling, and advanced analytics. Passionate about leveraging data to solve complex problems and drive business value.</p>',
            "Python Developer": '<p class="small-font">Skilled Python Developer with a strong background in software engineering principles and best practices. Experienced in developing efficient, scalable, and maintainable code for various applications.</p>'
        }
        st.markdown(role_descriptions.get(role, ""), unsafe_allow_html=True)

        st.subheader("Education")
        st.write("B.Tech - CSE, Annamacharya Institute Of Technology & Sciences, Kadapa")
        st.write("August 2018 - August 2022")
        st.write("CGPA: 6.98 | Final Semester SGPA: 9.18")

        # Use the imported create_education_chart() function
        education_chart = create_education_chart()
        st.plotly_chart(education_chart, use_container_width=True)

        # Use the imported create_chart() function for the Radar Chart
        skills_data = pd.DataFrame({
            'Skill': ['Python', 'SQL', 'Data Viz', 'Machine Learning', 'Communication'],
            'Proficiency': [90, 85, 95, 80, 75]
        })
        radar_chart = create_chart(skills_data, 'line_polar', title="Technical Skill Proficiency",
                                   theta='Skill', line_close=True)
        radar_chart.update_traces(fill='toself')
        st.plotly_chart(radar_chart, use_container_width=True)

        st.subheader("My Journey (Animated)")
        display_work_experience()


        st.write("Let's connect! Choose your preferred platform:")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("[Visit my LinkedIn Profile](https://www.linkedin.com/in/yourprofile)")
        with col2:
            st.markdown("[Check out my GitHub](https://github.com/yourusername)")
        with col3:
            st.markdown("[Follow me on Twitter](https://twitter.com/yourhandle)")

    elif selected == "Skills":
        st.header(f"Skills & Expertise - {role}")

        # Get skills data from skills.py
        skills = get_skills_data(role)
        skills_data = skills["skills_data"]
        additional_skills = skills["additional_skills"]

        radar_chart = create_radar_chart(skills_data, "Data Scientist")
        st.plotly_chart(radar_chart, use_container_width=True)

        bar_chart = create_bar_chart(skills_data, "Data Scientist")
        st.plotly_chart(bar_chart, use_container_width=True)

        # --- Additional Skills ---
        st.subheader("Additional Skills")
        for skill in additional_skills:
            st.markdown(f'<span class="skill-tag">{skill}</span>', unsafe_allow_html=True)

        create_skills_network(role)

    elif selected == "Projects":
        st.header(f"Projects - {role}")
        st.subheader("Explore My Work")

        projects = get_projects(role)

        for project, description in projects.items():
            col1, col2 = st.columns([1, 3])
            with col1:
                with st.container():
                    st.markdown(f'<div class="project-card">', unsafe_allow_html=True)

                    image_file = f"{project.lower().replace(' ', '_')}.jpg"
                    image_path = os.path.join("project_images", image_file)

                    if os.path.exists(image_path):
                        st.image(image_path, use_column_width=True)
                    else:
                        st.warning(f"Image not found: {image_path}")

                    st.markdown(f'<div class="overlay"><h3>{project}</h3></div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                with st.container():
                    st.markdown(f'<div class="project-card">', unsafe_allow_html=True)
                    st.subheader(project)
                    with st.expander("See Details"):
                        st.write(description)
                        st.write("[Link to Project Repo/Demo]")  # Replace with actual link
                    st.markdown('</div>', unsafe_allow_html=True)

        # Create and display the project network graph
        create_project_network() 

    elif selected == "Contact":
        contact_section(role)
    elif selected == "Chat Bot":
        chatbot()

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.write("© 2024 Syed Shahid Nazeer")
    with col2:
        background_type = st.selectbox("Choose background type", ["Static", "Dynamic"], key="background_select")
        if background_type == "Dynamic":
            set_background("background.gif", is_gif=True)

if __name__ == "__main__":
    main()