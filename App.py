import streamlit as st
from streamlit_lottie import st_lottie
import json
from PIL import Image
import pandas as pd
import plotly.express as px

# Load Lottie animation files (replace with your actual file paths)
animation1 = "Animations/Animation - 1720882973633.json"
animation2 = "Animations/Animation - 1720883141611.json"

def load_lottie_animation(file_path):
    with open(file_path, "r") as f:
        animation_data = json.load(f)
    return animation_data

def main():
    
    # Display Lottie animation 1 (above profile image)
    st_lottie(load_lottie_animation(animation1), speed=1, width=200, height=200)

    # Load your profile photo (replace with your actual image)
    profile_image = Image.open("images/1.jpg").resize((150, 150))

    st.title("SHAHID NAZEERSYED - Data Science Portfolio")

    # Sidebar with profile photo
    st.sidebar.image(profile_image)
    st.sidebar.write("Kadapa, 516001")
    st.sidebar.write("+919912357968")
    st.sidebar.write("shahidnazeerds@gmail.com")
    st.sidebar.write("Personal Website")

    # Introduction
    st.write("## About Me")
    st.write("Enthusiastic Data Science fresher with hands-on experience in data preparation, machine learning, and statistical analysis gained during an internship at Ai Variant. Proficient in scripting, Microsoft AI/ML tools, and extensive data analysis. Adept at translating technical insights into customer-oriented solutions that align with business strategies. Strong collaborator, eager to drive business value through data-driven projects.")

    # Education
    st.write("## Education")
    st.write("- Bachelor of Technology (B.Tech.) - Computer Science")
    st.write("  Annamacharya Institute of Technology and Sciences, Kadapa")
    st.write("  Aug 2018 - Aug 2022")

    # Experience
    st.write("## Experience")
    st.write("- Data Science Intern")
    st.write("  Ai Variant, Bengaluru")
    st.write("  Mar 2023 - Dec 2023")
    st.write("  Led data-driven projects, deriving impactful insights that aligned with business goals.")

    # Sample data (replace with your actual skill levels)
    skills_data = {
        "Skill": ["Excel", "Python", "Power BI", "Machine Learning", "MySQL", "Tableau", "Deep Learning"],
        "Experience": ["Expert", "Expert", "Expert", "Expert", "Intermediate", "Intermediate", "Intermediate"]
    }

    # Create a DataFrame
    df = pd.DataFrame(skills_data)

    # Create a 3D scatter plot
    fig = px.scatter_3d(df, x="Skill", y="Experience", z="Experience", color="Skill",
                        title="Skills Proficiency in 3D")
    fig.update_layout(scene=dict(xaxis_title="Skill", yaxis_title="Experience", zaxis_title="Experience"))

    # Display the plot in Streamlit
    st.plotly_chart(fig)
    
    # Display Lottie animation 2 (below profile image)
    st_lottie(load_lottie_animation(animation2), speed=1, width=200, height=200)

    # Sample data (replace with your actual skill levels)
    skills_data = {
        "Skill": ["Excel", "Python", "Power BI", "Machine Learning", "MySQL", "Tableau", "Deep Learning"],
        "Experience": ["Expert", "Expert", "Expert", "Expert", "Intermediate", "Intermediate", "Intermediate"]
    }

    # Create a DataFrame
    df = pd.DataFrame(skills_data)

    # Create a radar chart
    fig = px.line_polar(df, r="Experience", theta="Skill", line_close=True,
                        title="Skills Proficiency (Radar Chart)")
    fig.update_traces(fill="toself")

    # Display the plot in Streamlit
    st.plotly_chart(fig)

    # Certifications
    st.write("## Licenses & Certifications")
    st.write("- Data Science 2023 (Excelr - 14727/EXCELR/29052023)")
    st.write("- Business Analytics 2023 (Internshala - 9ckfw5soqxk)")

    # Define your skills data (replace with actual values)
    skills_data = [
        {"Skill": "Data Cleaning", "Experience": 4, "Category": "Data Engineering"},
        {"Skill": "Data Visualization", "Experience": 5, "Category": "Data Communication"},
        {"Skill": "Machine Learning", "Experience": 3, "Category": "Modeling"},
        {"Skill": "Problem Solving", "Experience": 5, "Category": "Critical Thinking"},
        {"Skill": "Critical Thinking", "Experience": 4, "Category": "Analysis"},
    ]

    # Create a DataFrame from the skills data
    df = pd.DataFrame(skills_data)

    # Create a 3D scatter plot with color-coded categories
    fig = px.scatter_3d(
        df, 
        x="Skill", 
        y="Experience", 
        z="Experience", 
        color="Category", 
        title="Data Analyst Skills Proficiency",
        opacity=0.8  # Adjust opacity for better visibility
    )

    # Customize layout for a more interactive experience
    fig.update_layout(
        scene=dict(
            xaxis_title="Skill",
            yaxis_title="Experience",
            zaxis_title="Experience",
            # Enable camera rotation for better viewing angles
            camera=dict(
                eye=dict(x=1.2, y=-1.5, z=1.0)
            )
        ),
        # Add hover information for each skill point
        hovertemplate="<b>%{Skill}</b><br>Experience: %{Experience}<br>Category: %{Category}"
    )

    # Allow users to rotate the plot for better viewing angles
    st.plotly_chart(fig, use_container_width=True)  # Stretch plot to fill container width


if __name__ == "__main__":
    main()
