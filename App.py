import streamlit as st
from PIL import Image  # For image manipulation
import matplotlib.pyplot as plt  # For interactive charts

# Function to display progress bar with dynamic text
def progress_bar(text, complete=False):
    progress_bar = st.sidebar.progress(text)
    if complete:
        progress_bar.progress(100)

# Customizable data for portfolio sections
data = {
    "name": "Shahid Nazeersyed",
    "title": "Data Science Enthusiast",
    "location": "Kadapa, India",
    "contact": "+91 9912357968",
    "email": "shahidnazeerds@gmail.com",
    "website": "https://yourwebsite.com",  # Replace with your website link
    "about": """
        Enthusiastic Data Science fresher with hands-on experience in data preparation,
        machine learning, and statistical analysis gained during an internship at Ai
        Variant. Proficient in scripting, Microsoft AI/ML tools, and extensive data
        analysis. Adept at translating technical insights into customer-oriented
        solutions that align with business strategies. Strong collaborator, eager to
        drive business value through data-driven projects.
    """,
    "education": [
        {"institution": "Annamacharya Institute of Technology and Sciences, Kadapa",
         "degree": "Bachelor of Technology (B.Tech.) - Computer Science",
         "dates": "Aug 2018 - Aug 2022"},
    ],
    "experience": [
        {"company": "Ai Variant, Bengaluru",
         "position": "Data Science Intern",
         "dates": "Mar 2023 - Dec 2023",
         "description": "Led data-driven projects, deriving impactful insights that aligned with business goals."},
    ],
    "skills": {
        "expert": ["Excel", "Python", "Power BI", "Machine Learning"],
        "intermediate": ["MySQL", "Tableau", "Deep Learning"],
    },
    "certifications": [
        {"name": "Data Science 2023", "issuer": "Excelr (14727/EXCELR/29052023)"},
        {"name": "Business Analytics 2023", "issuer": "Internshala (9ckfw5soqxk)"},
    ],
    "projects": [  # Add project data here
        {"title": "Project Title 1",
         "description": "Brief description of project 1",
         "link": "https://project1.com",  # Replace with project link (optional)
         "technologies": ["Technology 1", "Technology 2"]},
        # ... Add more projects as needed
    ],
}

def main():
    # Set a cool and trendy color scheme
    st.set_page_config(
        page_title=data["name"] + " - Data Science Portfolio",
        layout="wide",  # Wide layout for better layout options
        initial_sidebar_state="expanded",  # Expand sidebar by default
    )

    # Load and resize profile image (optional)
    profile_image = Image.open("images/1.jpg").resize((200, 200))
    st.sidebar.image(profile_image)

    # Contact information in sidebar
    st.sidebar.markdown(f"""
        * Name: {data['name']}
        * Title: {data['title']}
        * Location: {data['location']}
        * Contact: {data['contact']}
        * Email: {data['email']}
        * Website: [{data['website']}]({data['website']})  # Link to website
    """, unsafe_allow_html=True)

    # Title section
    st.title(data["name"])
    st.subheader(data["title"])
    st.write(f"Location: {data['location']}")

    # About section
    st.write("## About Me")
    st.markdown(data["about"])

    # Education section
    st.write("## Education")
    for entry in data["education"]:
        st.subheader(entry["degree"])
        st.write(f"{entry['institution']}, {entry['dates']}")
