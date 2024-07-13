import os
import streamlit as st

def main():
    st.title("SHAHID NAZEERSYED - Data Science Portfolio")
    
    # Get the current working directory
    current_dir = os.getcwd()

    # Sidebar with profile photo
    st.sidebar.image(os.path.join(current_dir, "images", "1.jpg"), width=150)
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

    # Skills
    st.write("## Skills")
    st.write("- Expert in: Excel, Python, Power BI, Machine Learning")
    st.write("- Intermediate in: MySQL, Tableau, Deep Learning")

    # Certifications
    st.write("## Licenses & Certifications")
    st.write("- Data Science 2023 (Excelr - 14727/EXCELR/29052023)")
    st.write("- Business Analytics 2023 (Internshala - 9ckfw5soqxk)")

if __name__ == "__main__":
    main()


