import streamlit as st
import plotly.express as px
import pandas as pd
import os
import base64
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
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href

def chatbot():
    st.header("Gemini Chat Bot")
    st.header("Gemini Chat Bot")

    try:
        # Select Gemini model
        model_choice = st.selectbox("Select Gemini Model", ["gemini-pro", "gemini-pro-vision"])
        genai.configure(api_key="AIzaSyB_1wDDKexv5EPqB8kJZOhuISGOixPzHlM")

        # ... (rest of your chatbot code)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please make sure you have set up your API key correctly in the Streamlit secrets.")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    user_input = st.chat_input("Ask me anything!")

    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)

        # Generate AI response
        model = genai.GenerativeModel(model_choice)
        response = model.generate_content(user_input)

        # Add AI response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response.text})

        # Display AI response
        with st.chat_message("assistant"):
            st.markdown(response.text)


def main():
    st.set_page_config(page_title="SYED SHAHID NAZEER - Portfolio", layout="wide")

    # Responsive CSS
    st.markdown("""
    <style>
    .big-font {font-size:clamp(30px, 5vw, 50px) !important; color: #4A4A4A;}
    .medium-font {font-size:clamp(20px, 4vw, 30px) !important; color: #4A4A4A;}
    .small-font {font-size:clamp(16px, 3vw, 20px) !important; color: #4A4A4A;}
    .stSelectbox {max-width: 100%;}
    .stButton > button {width: 100%;}
    .responsive-container {display: flex; flex-wrap: wrap; gap: 10px; justify-content: space-between;}
    .responsive-container > div {flex: 1 1 200px;}
    @media (max-width: 768px) {
        .responsive-container {flex-direction: column;}
        .responsive-container > div {flex: 1 1 100%;}
    }
    .chart-container {width: 100%; overflow-x: auto;}
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
            "icon": {"color": "orange", "font-size": "clamp(16px, 3vw, 25px)"}, 
            "nav-link": {"font-size": "clamp(14px, 2.5vw, 20px)", "text-align": "center", "margin":"0px", "--hover-color": "#eee"},
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

    # Page selection navbar
    selected = option_menu(
        menu_title=None,
        options=["Home", "Skills", "Projects", "Contact", "Chat Bot"],
        icons=["house", "gear", "code-slash", "envelope", "chat-dots"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "rgba(250, 250, 250, 0.8)"},
            "icon": {"color": "orange", "font-size": "clamp(16px, 3vw, 25px)"}, 
            "nav-link": {"font-size": "clamp(14px, 2.5vw, 20px)", "text-align": "center", "margin":"0px", "--hover-color": "#eee"},
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

        # Wrap the chart in a container for better mobile view
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(create_education_chart(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

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
        
        # Wrap the chart in a container for better mobile view
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig = px.bar(skills_data, x='Skill', y='Proficiency', 
                     title=f'Core Skills - {role}',
                     labels={'Proficiency': 'Proficiency Level'},
                     color='Proficiency',
                     color_continuous_scale='Viridis')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.subheader("Additional Skills")
        if role == "Data Analyst":
            st.write("Power BI, Tableau, Data Cleaning, ETL processes, A/B Testing")
        elif role == "Data Scientist":
            st.write("TensorFlow, PyTorch, Time Series Analysis, Feature Engineering, Cloud Computing (AWS/GCP)")
        else:  # Python Developer
            st.write("RESTful APIs, Docker, Git, Agile Methodologies, Test-Driven Development")

        # Add an interactive skill rating system
        st.subheader("Rate Your Own Skills")
        user_skill = st.text_input("Enter a skill you want to rate")
        user_rating = st.slider("Rate your proficiency", 0, 100, 50)
        if st.button("Add Skill"):
            st.success(f"You rated your {user_skill} skill at {user_rating}%")

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

        # Wrap the chart in a container for better mobile view
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(create_project_impact_chart(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

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

        # Add a map
        st.subheader("My Location")
        st.map({"lat": [17.3850], "lon": [78.4867]})

    elif selected == "Chat Bot":
        # Call the chatbot function here
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