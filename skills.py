import pandas as pd
import streamlit as st

def get_skills_data(role):
    """Returns skills data based on the selected role."""

    skills = {
        "Data Analyst": {
            "skills_data": pd.DataFrame({
                'Skill': ['SQL', 'Excel', 'Data Viz', 'Statistical Analysis', 'BI Tools'],
                'Proficiency': [85, 90, 80, 85, 75],
                "Description": [
                    "Strong SQL skills for querying and data manipulation.",
                    "Proficient in Excel for data analysis and reporting.",
                    "Experienced with data visualization tools like Tableau and Power BI.",
                    "Solid understanding of statistical analysis techniques.",
                    "Knowledge of business intelligence concepts and tools."
                ]
            }),
            "additional_skills": ["Power BI", "Tableau", "Data Cleaning", "ETL Processes", "A/B Testing"]
        },
        "Data Scientist": {
            "skills_data": pd.DataFrame({
                'Skill': ['Python', 'ML', 'Deep Learning', 'NLP', 'Big Data'],
                'Proficiency': [90, 85, 80, 75, 70],
                "Description": [
                    "Proficient in Python for data analysis, scripting, and machine learning.",
                    "Strong understanding of machine learning algorithms and techniques.",
                    "Experience with deep learning frameworks like TensorFlow and PyTorch.",
                    "Knowledge of Natural Language Processing (NLP) concepts and libraries.",
                    "Familiar with big data technologies and tools." 
                ]
            }),
            "additional_skills": ["TensorFlow", "PyTorch", "Time Series Analysis", "Feature Engineering", "Cloud Computing (AWS/GCP)"]
        },
        "Python Developer": {
            "skills_data": pd.DataFrame({
                'Skill': ['Python', 'Django', 'Flask', 'API Development', 'Database Design'],
                'Proficiency': [95, 80, 75, 85, 80],
                "Description": [
                    "Expert in Python programming language and its ecosystem.",
                    "Experienced with Django framework for building web applications.",
                    "Familiar with Flask framework for developing web services and APIs.",
                    "Strong understanding of API development principles (RESTful APIs).",
                    "Proficient in database design and SQL."
                ]
            }),
            "additional_skills": ["RESTful APIs", "Docker", "Git", "Agile Methodologies", "Test-Driven Development"]
        }
    }
    return skills.get(role)

def display_skills(role):
    skills_data = get_skills_data(role)

    st.header("Skills")

    # Dropdown for role selection
    selected_role = st.selectbox("Select Your Role", ["Data Analyst", "Data Scientist", "Python Developer"])

    # Display skills dynamically based on selected role
    if selected_role:
        skills_df = skills_data["skills_data"]

        # Display skills as cards
        for index, row in skills_df.iterrows():
            skill = row["Skill"]
            proficiency = row["Proficiency"]
            description = row["Description"]

            st.markdown(f"**{skill}**: {proficiency}%")
            st.markdown(f"{description}")
            st.progress(proficiency / 100)  # Display progress bar