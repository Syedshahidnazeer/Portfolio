import streamlit as st
from PIL import Image
import pandas as pd
import plotly.express as px

def main():

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


if __name__ == "__main__":
    main()
