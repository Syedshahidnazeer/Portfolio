import plotly.express as px
import streamlit as st
import pandas as pd

def create_chart(data, chart_type, title=None, x=None, y=None, **kwargs):
    """Creates a chart using Plotly Express."""

    chart_functions = {
        'bar': px.bar,
        'line': px.line,
        'pie': px.pie,
        'scatter': px.scatter,
        'line_polar': px.line_polar,
        'histogram': px.histogram,  # Add histogram chart type
        'box': px.box,  # Add box plot chart type
        'violin': px.violin,  # Add violin plot chart type
        'scatter_3d': px.scatter_3d,  # Add 3D scatter chart type
    }

    chart_func = chart_functions.get(chart_type)
    if chart_func:
        if chart_type == 'pie':
            fig = chart_func(data, values=y, names=x, title=title, **kwargs)
        elif chart_type == 'line_polar':
            # Remove 'r' and 'theta' from kwargs if they exist
            kwargs.pop('r', None)
            kwargs.pop('theta', None)
            fig = chart_func(data, r=y, theta=x, title=title, **kwargs)
        else:
            fig = chart_func(data, x=x, y=y, title=title, **kwargs)
        return fig
    else:
        st.error(f"Unsupported chart type: {chart_type}")
        return None

@st.cache_data
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

@st.cache_data
def display_work_experience():
    st.subheader("Work Experience")
    st.write("**Data Science Intern | AI Variant | Bangalore**")
    st.write("March 2023 - December 2023")
    
    experience_details = [
        "Collaborated on data-driven projects, contributing impactful insights aligned with business requirements.",
        "Managed data collection and preparation, ensuring clean and reliable datasets for analysis.",
        "Applied machine learning algorithms to achieve project goals and effectively communicated findings and potential risks.",
        "Designed experiments and operationalized models following AI and engineering best practices.",
        "Proficiently scripted in various languages and utilized Microsoft AI and ML tools for efficient analysis.",
        "Contributed to internal best practices for data collection and preparation, ensuring data integrity.",
        "Conducted extensive exploratory data analysis on large datasets, identifying valuable patterns and trends.",
        "Assisted in evaluating team models, recommending enhancements to ensure alignment with business objectives.",
        "Collaborated with cross-functional teams, enhancing solutions to drive business value.",
        "Maintained a customer-oriented approach by understanding business, product, and customer perspectives."
    ]
    
    with st.expander("View Details"):
        for detail in experience_details:
            st.write(f"• {detail}")

    # Add a chart or visualization related to your internship
    internship_impact = pd.DataFrame({
        'Metric': ['Projects Completed', 'Algorithms Implemented', 'Datasets Analyzed'],
        'Value': [5, 8, 15]  # Replace with actual values
    })
    fig = px.bar(internship_impact, x='Metric', y='Value', title='Internship Impact')
    st.plotly_chart(fig, use_container_width=True)

@st.cache_data
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

@st.cache_data
def create_project_impact_chart():
    project_data = pd.DataFrame({
        'Project': ['App Rating Prediction', 'Fake News Detection', 'Oil Price Prediction'],
        'Impact Score': [93, 85, 88]
    })
    
    fig = px.pie(project_data, values='Impact Score', names='Project', 
                 title='Project Impact',
                 hole=0.3)
    return fig
@st.cache_data
def create_radar_chart(skills_data, role):
    """Creates a radar chart for skill proficiency."""
    radar_chart = create_chart(skills_data,
                                'line_polar',
                                title=f"{role} Skill Proficiency",
                                theta='Skill',
                                line_close=True)
    radar_chart.update_traces(fill='toself')
    return radar_chart

@st.cache_data
def create_bar_chart(skills_data, role):
    """Creates a bar chart for core skills."""
    bar_chart = create_chart(skills_data,
                                'bar',
                                title=f'Core Skills - {role}',
                                x='Skill',
                                y='Proficiency',
                                color='Proficiency',
                                color_continuous_scale='Viridis',
                                hover_data=['Description'])
    bar_chart.update_traces(hovertemplate='Skill: %{x}<br>Proficiency: %{y}%<br>Description: %{customdata[0]}')
    return bar_chart

@st.cache_data
def create_heatmap_chart():
    """Creates a heatmap chart for skills over time."""
    df = pd.DataFrame({
        'Year': [2019, 2020, 2021, 2022, 2023] * 3,
        'Skill': ['Python'] * 5 + ['SQL'] * 5 + ['Data Viz'] * 5,
        'Proficiency': [70, 80, 90, 92, 95, 60, 75, 80, 85, 88, 50, 65, 80, 85, 90],
        'Area': ['Backend'] * 5 + ['Data'] * 5 + ['Frontend'] * 5
    })

    heatmap_chart = create_chart(df,
                                'scatter',
                                x='Skill',
                                y='Proficiency',
                                size='Proficiency',
                                color='Skill',
                                animation_frame="Year",
                                animation_group="Skill",
                                size_max=50,
                                range_y=[0, 100],
                                title="Skills Growth Over Time",
                                labels={"Proficiency": "Skill Level"})

    heatmap_chart.update_layout(
        updatemenus=[dict(
            type='buttons',
            showactive=False,
            buttons=[dict(
                label='Play',
                method='animate',
                args=[None, dict(frame=dict(duration=1000, redraw=True),
                                transition=dict(duration=500),
                                fromcurrent=True,
                                mode='immediate')]
            )]
        )],
        xaxis=dict(title='Skill'),
        yaxis=dict(title='Proficiency'),
        height=600,
        width=800,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return heatmap_chart