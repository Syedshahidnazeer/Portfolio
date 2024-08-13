import streamlit as st
from pyvis.network import Network

@st.cache_data
def create_skills_network(role):
    """Creates a skill network graph based on the selected role."""

    if role == "Data Analyst":
        skills_data = {
            "nodes": [
                {"id": "SQL", "group": "Databases"},
                {"id": "Excel", "group": "Tools"},
                {"id": "Data Visualization", "group": "Analysis"},
                {"id": "Statistical Analysis", "group": "Analysis"},
                {"id": "Business Intelligence", "group": "Business"}
            ],
            "edges": [
                {"source": "SQL", "target": "Data Visualization", "label": "Data Insights"},
                {"source": "Excel", "target": "Data Visualization", "label": "Reporting"},
                {"source": "Statistical Analysis", "target": "Business Intelligence", "label": "Decision Making"},
                {"source": "Data Visualization", "target": "Business Intelligence", "label": "Actionable Insights"}
            ]
        }
    elif role == "Data Scientist":
        skills_data = {
            "nodes": [
                {"id": "Python", "group": "Programming"},
                {"id": "Machine Learning", "group": "AI/ML"},
                {"id": "Deep Learning", "group": "AI/ML"},
                {"id": "NLP", "group": "AI/ML"},
                {"id": "Big Data", "group": "Data"}
            ],
            "edges": [
                {"source": "Python", "target": "Machine Learning", "label": "Model Building"},
                {"source": "Python", "target": "Deep Learning", "label": "Neural Networks"},
                {"source": "Python", "target": "NLP", "label": "Text Analysis"},
                {"source": "Machine Learning", "target": "Big Data", "label": "Scalability"},
                {"source": "Deep Learning", "target": "Big Data", "label": "Large Datasets"}
            ]
        }
    else:  # Python Developer
        skills_data = {
            "nodes": [
                {"id": "Python", "group": "Programming"},
                {"id": "Django", "group": "Frameworks"},
                {"id": "Flask", "group": "Frameworks"},
                {"id": "API Development", "group": "Backend"},
                {"id": "Database Design", "group": "Databases"}
            ],
            "edges": [
                {"source": "Python", "target": "Django", "label": "Web Apps"},
                {"source": "Python", "target": "Flask", "label": "REST APIs"},
                {"source": "Django", "target": "Database Design", "label": "Data Models"},
                {"source": "Flask", "target": "API Development", "label": "Microservices"},
                {"source": "API Development", "target": "Database Design", "label": "Data Persistence"}
            ]
        }

    net = Network(height="600px", width="100%", notebook=True, heading=f"{role} Skill Network")

    # Add nodes with groups
    for node in skills_data["nodes"]:
        net.add_node(node["id"], group=node["group"])

    # Add edges with labels
    for edge in skills_data["edges"]:
        net.add_edge(edge["source"], edge["target"], title=edge["label"])

    # Configure interactivity options
    net.set_options("""
    {
      "physics": {
        "enabled": true,
        "barnesHut": {
          "gravitationalConstant": -2000,
          "centralGravity": 0.3,
          "springLength": 95,
          "springConstant": 0.04,
          "damping": 0.09
        },
        "maxVelocity": 50,
        "minVelocity": 0.1,
        "solver": "barnesHut",
        "timestep": 0.5
      },
      "nodes": {
        "font": {
          "size": 14
        }
      },
      "edges": {
        "smooth": {
          "enabled": true,
          "type": "dynamic"
        }
      },
      "interaction": {
        "hover": true,
        "tooltipDelay": 200,
        "navigationButtons": true
      }
    }
    """) 

    # Save and display the graph
    net.save_graph("skills_network.html")
    st.components.v1.html(open("skills_network.html", 'r').read(), height=650)

@st.cache_data
def create_project_network():
    """Creates a network graph of projects."""
    # Define project data here
    data = {
        "nodes": [
            {"id": "Project A", "group": "Data Science"},
            {"id": "Project B", "group": "Web Dev"},
            {"id": "Project C", "group": "Data Science"},
            {"id": "Project D", "group": "Data Viz"},
            {"id": "Project E", "group": "Web Dev"},
        ],
        "edges": [
            {"source": "Project A", "target": "Project C", "label": "Shared Data"},
            {"source": "Project B", "target": "Project E", "label": "Same Framework"},
            {"source": "Project A", "target": "Project D", "label": "Visualization"},
            {"source": "Project C", "target": "Project D", "label": "Visualization"},
        ]
    }

    net = Network(height="600px", width="100%", notebook=True, heading="Project Connections")

    # Add nodes with groups
    for node in data["nodes"]:
        net.add_node(node["id"], group=node["group"])

    # Add edges with labels
    for edge in data["edges"]:
        net.add_edge(edge["source"], edge["target"], title=edge["label"])

        # Configure interactivity options
    net.set_options("""
    {
      "physics": {
        "enabled": true,
        "barnesHut": {
          "gravitationalConstant": -2000,
          "centralGravity": 0.3,
          "springLength": 95,
          "springConstant": 0.04,
          "damping": 0.09
        },
        "maxVelocity": 50,
        "minVelocity": 0.1,
        "solver": "barnesHut",
        "timestep": 0.5
      },
      "nodes": {
        "font": {
          "size": 14
        }
      },
      "edges": {
        "smooth": {
          "enabled": true,
          "type": "dynamic"
        }
      },
      "interaction": {
        "hover": true,
        "tooltipDelay": 200,
        "navigationButtons": true
      }
    }
    """) 
    # Save and display the graph
    net.save_graph("project_network.html")
    st.components.v1.html(open("project_network.html", 'r').read(), height=650)