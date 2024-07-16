import streamlit as st
from PIL import Image
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
    
    # Define your proficiency levels for different chart types (adjust values)
    proficiency_levels = {
        "Scatter Plot": 4,
        "Line Graph": 5,
        "Bar Chart": 4,
        "Heatmap": 3,
    }

    # Create pie chart data
    chart_types = list(proficiency_levels.keys())
    proficiency_values = list(proficiency_levels.values())

    fig = go.Figure(data=[go.Pie(labels=chart_types, values=proficiency_values)])
    fig.update_layout(
        title="Data Visualization District",
        showlegend=False  # Remove default legend, add custom later
    )

    # Add click events and pop-ups for chart details (replace with your content)
    def show_chart_details(chart_type):
        st.write(f"**{chart_type} Details:**")
        st.write("Strengths: ...")
        st.write("Weaknesses: ...")

    fig.data[0].customdata = chart_types
    fig.update_traces(textposition='outside', textinfo='custom')
    fig.on_click(show_chart_details)

    st.plotly_chart(fig)

    # Add custom legend outside the pie chart
    st.write("Legend:")
    for chart_type, value in zip(chart_types, proficiency_values):
        color = fig.data[0].marker.colors[chart_types.index(chart_type)]
        st.write(f"- {chart_type} ({value})", unsafe_allow_html=True, style=f"color: {color}")


    # Define your skills data (replace with actual values)
    skills_data = [
        {"Skill": "Data Cleaning", "Experience": 4, "Category": "Data Engineering"},
        {"Skill": "Data Visualization", "Experience": 5, "Category": "Data Communication"},
        {"Skill": "Machine Learning", "Experience": 3, "Category": "Modeling"},
        {"Skill": "Problem Solving", "Experience": 5, "Category": "Critical Thinking"},
        {"Skill": "Critical Thinking", "Experience": 4, "Category": "Analysis"},
    ]

    # Create a DataFrame from the skills data
    df_skills = pd.DataFrame(skills_data)

    # Streamlit controls
    selected_category = st.selectbox("Filter by Category", df_skills['Category'].unique())

    # Filter data based on selection
    df_filtered = df_skills[df_skills['Category'] == selected_category]

    # Create a bar chart
    fig_skills = go.Figure(go.Bar(
        x=df_filtered['Skill'],
        y=df_filtered['Experience'],
        marker_color='royalblue',
        text=df_filtered['Experience'],
        textposition='auto'
    ))

    # Customize the layout
    fig_skills.update_layout(
        title='Skills Experience',
        xaxis_title='Skill',
        yaxis_title='Experience (Years)',
        paper_bgcolor='rgba(0, 0, 0, 0.1)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color='white')
    )

    # Display the chart
    st.plotly_chart(fig_skills)






if __name__ == "__main__":
    main()
