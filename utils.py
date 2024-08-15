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
    """Displays a PDF file using st.components.v1."""
    with open(file_path, "rb") as f:
        pdf_data = f.read()
    base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
    pdf_display = f"""
    <embed src="data:application/pdf;base64,{base64_pdf}" type="application/pdf" width="700" height="1000" />
    """
    st.components.v1.html(pdf_display, height=1000)

@st.cache_data
def get_binary_file_downloader_html(file_path, file_label):
    with open(file_path, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(file_path)}">Download {file_label}</a>'
    return href
def show_video(video_file):
    """Displays a video."""
    st.markdown(f"""
    <div class="announcement-wrapper">
        <div class="announcement-video-container">
            <video autoplay muted loop class="announcement-video">
                <source src="data:video/mp4;base64,{video_file}" type="video/mp4">
            </video>
        </div>
    </div>

    <style>
    .announcement-wrapper {{
        display: flex;
        flex-direction: column; /* Stack video on top of message */
        padding: 10px; /* Reduced padding */
        margin: 10px 0; /* Reduced margin */
        border-radius: 10px;
        animation: slide-in 1s ease-out;
    }}
    .announcement-video-container {{
        border-radius: 10px 10px 0 0; /* Rounded top corners */
    }}
    .announcement-video {{
        width: 100%;
        height: 200px; /* Reduced height */
        object-fit: cover;
    }}
    @keyframes slide-in {{
        from {{
            transform: translateY(-100%);
            opacity: 0;
        }}
        to {{
            transform: translateY(0);
            opacity: 1;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

def show_announcement(message):
    """Displays an animated announcement with a close button."""
    st.markdown(f"""
    <div class="announcement-container">
        <div class="announcement-content">
            <div class="announcement-text">{message}</div>
            <div class="announcement-close" id="close-announcement">×</div>
        </div>
    </div>

    <style>
    .announcement-container {{
        position: relative;
        padding: 10px; /* Reduced padding */
        margin: 10px 0; /* Reduced margin */
        background: rgba(255, 165, 0, 0.8); /* Orange background */
        border-radius: 10px;
        animation: slide-in 1s ease-out, pulse 2s infinite;
        text-align: center;
    }}
    .announcement-content {{
        position: relative;
        z-index: 1;
    }}
    .announcement-text {{
        font-size: 1.2em; /* Reduced font size */
        color: white;
        text-shadow: 0 0 10px #00ffff;
    }}
    .announcement-close {{
        position: absolute;
        top: 5px; /* Adjusted position */
        right: 5px; /* Adjusted position */
        font-size: 1.2em; /* Reduced font size */
        cursor: pointer;
        transition: transform 0.3s;
    }}
    .announcement-close:hover {{
        transform: scale(1.2);
    }}
    @keyframes slide-in {{
        from {{
            transform: translateY(-100%);
            opacity: 0;
        }}
        to {{
            transform: translateY(0);
            opacity: 1;
        }}
    }}
    @keyframes pulse {{
        0% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
        100% {{ transform: scale(1); }}
    }}
    </style>
    """, unsafe_allow_html=True)
def show_announcement(message):
    """Displays an animated announcement with a close button and a GIF."""
    gif_url = "https://media.tenor.com/2k1Xz1z7yXgAAAAC/bh187-family-guy-peter-griffin-suss.gif"
    st.markdown(f"""
    <div class="announcement-container">
        <div class="announcement-content">
            <div class="announcement-text">{message}</div>
            <div class="announcement-gif">
                <img src="{gif_url}" alt="Announcement GIF">
            </div>
            <div class="announcement-close" id="close-announcement">×</div>
        </div>
    </div>

    <style>
    .announcement-container {{
        position: relative;
        padding: 10px; /* Reduced padding */
        margin: 10px 0; /* Reduced margin */
        background: linear-gradient(90deg, #ff7e5f, #feb47b); /* Gradient background */
        border-radius: 10px;
        animation: slide-in 1s ease-out, gradient-shift 5s infinite;
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}
    .announcement-content {{
        position: relative;
        z-index: 1;
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 100%;
    }}
    .announcement-text {{
        font-size: 1.2em; /* Reduced font size */
        color: white;
        text-shadow: 0 0 10px #00ffff;
        flex: 1;
    }}
    .announcement-gif {{
        flex: 0 0 auto;
        margin-left: 10px;
    }}
    .announcement-gif img {{
        width: 50px; /* Adjust size as needed */
        height: auto;
        border-radius: 5px;
        animation: bounce 2s infinite; /* Add bounce animation */
    }}
    .announcement-close {{
        position: absolute;
        top: 5px; /* Adjusted position */
        right: 5px; /* Adjusted position */
        font-size: 1.2em; /* Reduced font size */
        cursor: pointer;
        transition: transform 0.3s;
    }}
    .announcement-close:hover {{
        transform: scale(1.2);
    }}
    @keyframes slide-in {{
        from {{
            transform: translateY(-100%);
            opacity: 0;
        }}
        to {{
            transform: translateY(0);
            opacity: 1;
        }}
    }}
    @keyframes gradient-shift {{
        0% {{
            background: linear-gradient(90deg, #ff7e5f, #feb47b);
        }}
        50% {{
            background: linear-gradient(90deg, #6a11cb, #2575fc);
        }}
        100% {{
            background: linear-gradient(90deg, #ff7e5f, #feb47b);
        }}
    }}
    @keyframes bounce {{
        0%, 20%, 50%, 80%, 100% {{
            transform: translateY(0);
        }}
        40% {{
            transform: translateY(-30px);
        }}
        60% {{
            transform: translateY(-15px);
        }}
    }}
    </style>
    """, unsafe_allow_html=True)
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

def display_contact_form():
    """Displays the contact form."""
    with st.form("contact_form"): 
        name = st.text_input("Name", key="name_input")
        email = st.text_input("Email", key="email_input")
        message = st.text_area("Message", key="message_input")
        submit_button = st.form_submit_button("Send Message")
        if submit_button:
            if all([name, email, message]):
                st.success("Thanks for your message! I'll get back to you soon.")
            else:
                st.warning("Please fill in all fields before submitting.")

def get_resume_file_path(role, document_type):
    """Returns the file path for the resume or cover letter based on the role."""
    file_type = "resume" if document_type == "Resume" else "cover_letter"
    file_path = os.path.join("resume", f"{role.lower().replace(' ', '_')}_{file_type}.pdf")
    return file_path

def display_resume_section(role):
    """Displays the Resume/Cover Letter section."""
    st.subheader("Resume & Cover Letter")
    
    document_choice = st.radio(
        "Select document to view",
        options=["Resume", "Cover Letter"],
        key="document_choice"
    )
    
    file_path = get_resume_file_path(role, document_choice)
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

st.markdown(f"<link rel='stylesheet' href='style.css'>", unsafe_allow_html=True)