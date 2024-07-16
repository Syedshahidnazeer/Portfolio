import streamlit as st
import plotly.express as px
import pandas as pd
import os
import base64
from streamlit_option_menu import option_menu

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
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href

def main():
    st.set_page_config(page_title="SYED SHAHID NAZEER - Portfolio", layout="wide")

    # Custom CSS for modern look
    st.markdown("""
    <style>
    .big-font {font-size:50px !important; color: #4A4A4A;}
    .medium-font {font-size:30px !important; color: #4A4A4A;}
    .small-font {font-size:20px !important; color: #4A4A4A;}
    .stSelectbox {max-width: 300px;}
    </style>
    """, unsafe_allow_html=True)

    # Role selection
    role = st.selectbox("Select Role", ["Data Analyst", "Data Scientist", "Python Developer"])

    # Navigation bar
    selected = option_menu(
        menu_title=None,
        options=["Home", "Skills", "Projects", "Contact"],
        icons=["house", "gear", "code-slash", "envelope"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "25px"}, 
            "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#02ab21"},
        }
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

    elif selected == "Skills":
        st.header(f"Skills & Expertise - {role}")
        
        if role == "Data Analyst":
            skills = ['SQL', 'Excel', 'Data Visualization', 'Statistical Analysis', 'Business Intelligence']
        elif role == "Data Scientist":
            skills = ['Python', 'Machine Learning', 'Deep Learning', 'NLP', 'Big Data']
        else:  # Python Developer
            skills = ['Python', 'Django', 'Flask', 'API Development', 'Database Design']
        
        skills_data = pd.DataFrame({
            'Skill': skills,
            'Proficiency': [85, 90, 80, 85, 75]  # Adjust these values as needed
        })
        
        fig = px.bar(skills_data, x='Skill', y='Proficiency', 
                     title=f'Core Skills - {role}',
                     labels={'Proficiency': 'Proficiency Level'},
                     color='Proficiency',
                     color_continuous_scale='Viridis')
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Additional Skills")
        if role == "Data Analyst":
            st.write("Power BI, Tableau, Data Cleaning, ETL processes, A/B Testing")
        elif role == "Data Scientist":
            st.write("TensorFlow, PyTorch, Time Series Analysis, Feature Engineering, Cloud Computing (AWS/GCP)")
        else:  # Python Developer
            st.write("RESTful APIs, Docker, Git, Agile Methodologies, Test-Driven Development")

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

    elif selected == "Contact":
        st.header("Contact")
        st.write("Phone: +91-9912357968")
        st.write("Email: shahidnazeerds@gmail.com")
        st.write("Location: Hyderabad, India")
        st.write("[LinkedIn Profile](https://www.linkedin.com/in/yourprofile)")  # Replace with your actual LinkedIn URL
        
        with st.form("contact_form"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            message = st.text_area("Message")
            submit_button = st.form_submit_button("Send Message")
        
        if submit_button:
            if name and email and message:
                st.success("Thanks for your message! I'll get back to you soon.")
                resume_path = os.path.join("resume", "resume.pdf")
                st.markdown(get_binary_file_downloader_html(resume_path, f'{role} Resume'), unsafe_allow_html=True)
            else:
                st.warning("Please fill in all fields before submitting.")

if __name__ == "__main__":
    main()