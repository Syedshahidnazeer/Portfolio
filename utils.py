import requests
from streamlit_lottie import st_lottie
import streamlit as st
import uuid
import base64
from fpdf import FPDF
import os

@st.cache_data
def load_lottieurl(url: str):
    """Loads a Lottie animation from a URL."""
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error loading Lottie animation from {url}: {e}")
        return None

def display_lottie(url, height=200, key=None):
    """Displays a Lottie animation."""
    lottie_json = load_lottieurl(url)
    if lottie_json:
        st_lottie(lottie_json, height=height, key=key)
    else:
        st.warning("Failed to load Lottie animation. Please check the URL.")
@st.cache_data
def display_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
@st.cache_data
def get_binary_file_downloader_html(file_path, file_label):
    with open(file_path, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(file_path)}">Download {file_label}</a>'
    return href
@st.cache_data
def show_announcement(message):
    """Displays an announcement with a close button."""
    st.markdown(f"""
    <div class="announcement-container">
        <div class="announcement-shine"></div>
        <div class="announcement-content">
            <div class="announcement-text">{message}</div>
            <div class="announcement-close" onclick="this.parentElement.parentElement.style.display='none'">×</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

@st.cache_data
def set_background(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded_string});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def display_contact_form():
    """Displays the contact form."""
    with st.form("contact_form"):  # Remove the key argument here
        name = st.text_input("Name", key="name_input")
        email = st.text_input("Email", key="email_input")
        message = st.text_area("Message", key="message_input")
        submit_button = st.form_submit_button("Send Message")
        if submit_button:
            if all([name, email, message]):
                st.success("Thanks for your message! I'll get back to you soon.")
            else:
                st.warning("Please fill in all fields before submitting.")

def display_resume_section(role):
    """Displays the Resume/Cover Letter section."""
    st.subheader("Resume & Cover Letter")
    
    document_choice = st.radio(
        "Select document to view",
        options=["Resume", "Cover Letter"],
        key="document_choice"
    )
    
    file_type = "resume" if document_choice == "Resume" else "cover_letter"
    file_path = os.path.join("resume", f"{role.lower().replace(' ', '_')}_{file_type}.pdf")
    file_label = f"{role} {document_choice}"
    
    try:
        display_pdf(file_path)
        st.markdown(get_binary_file_downloader_html(file_path, file_label), unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"The {file_label} file was not found. Please check if the file exists in the 'resume' folder.")

def contact_section(role):
    """Displays the Contact section of the portfolio."""
    st.header("Contact")

    # Display contact information
    contact_info = {
        "Phone": "+91-9912357968",
        "Email": "shahidnazeerds@gmail.com",
        "Location": "Hyderabad, India",
        "LinkedIn": "[LinkedIn Profile](https://www.linkedin.com/in/yourprofile)"
    }
    
    for key, value in contact_info.items():
        st.write(f"{key}: {value}")

    # Display the contact form
    display_contact_form()

    # Display the resume/cover letter section
    display_resume_section(role)

st.markdown(
    """
    <style>
        .contact-section {
            background-color: #f0f0f0;
            padding: 20px;
            border-radius: 5px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h2 class='contact-section'>Contact</h2>", unsafe_allow_html=True)