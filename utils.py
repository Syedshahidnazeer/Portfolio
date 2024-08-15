import requests
from streamlit_lottie import st_lottie
import streamlit as st
import uuid
import base64
from fpdf import FPDF
import os
import pandas as pd
from io import BytesIO
from datetime import datetime
from itertools import cycle
import json

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

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

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
    
    
def show_announcement(messages):
    """Displays an animated announcement with scrolling messages and Peter Griffin GIF."""
    gif_path = "images/Peter Griffin Dancing.gif"  # Make sure this path is correct
    
    messages_cycle = cycle(messages)
    # Read and encode the GIF file
    with open(gif_path, "rb") as gif_file:
        gif_data = gif_file.read()
        gif_base64 = base64.b64encode(gif_data).decode("utf-8")

    messages_json = json.dumps(messages)
    st.markdown(
        f"""
    <div class="announcement-container">
        <img src="data:image/gif;base64,{gif_base64}" alt="Peter Griffin GIF" class="peter-gif"> 
        <div class="announcement-content">
            <div class="announcement-text" id="scrolling-text"></div> 
        </div>
        <div class="announcement-close" id="close-announcement">×</div>
    </div>

    <style>
    .announcement-container {{
        position: relative;
        padding: 15px;
        margin: 15px 0;
        background: linear-gradient(90deg, #ff7e5f, #feb47b);
        border-radius: 15px;
        animation: slide-in 1s ease-out, gradient-shift 10s infinite;
        text-align: center;
        overflow: hidden;
    }}
    .peter-gif {{
        position: absolute;
        left: 10px;
        top: 50%;
        transform: translateY(-50%);
        width: 60px;
        height: 60px;
        border-radius: 50%;
        object-fit: cover;
    }}
    .announcement-content {{
        margin-left: 70px;
        position: relative;
        z-index: 1;
    }}
    .announcement-container {{
        /* ... (rest of your existing CSS) ... */
    }}
    .announcement-text {{
        font-size: 1.3em;
        color: white;
    }}
    .announcement-close {{
        position: absolute;
        top: 5px;
        right: 10px;
        font-size: 1.5em;
        cursor: pointer;
        transition: transform 0.3s;
    }}
    .announcement-close:hover {{
        transform: scale(1.2);
    }}
    @keyframes slide-in {{
        from {{ transform: translateY(-100%); opacity: 0; }}
        to {{ transform: translateY(0); opacity: 1; }}
    }}
    @keyframes gradient-shift {{
        0% {{ background: linear-gradient(90deg, #ff7e5f, #feb47b); }}
        25% {{ background: linear-gradient(90deg, #6a11cb, #2575fc); }}
        50% {{ background: linear-gradient(90deg, #00c6ff, #0072ff); }}
        75% {{ background: linear-gradient(90deg, #ed4264, #ffedbc); }}
        100% {{ background: linear-gradient(90deg, #ff7e5f, #feb47b); }}
    }}
    </style>

    <script>
    const messages = {messages_json}; 
    const scrollingText = document.getElementById('scrolling-text');
    let currentIndex = 0;

    function updateText() {{
        scrollingText.style.animation = 'none';
        scrollingText.offsetHeight; 
        scrollingText.textContent = messages[currentIndex];
        scrollingText.style.animation = 'scroll-left 15s linear';
        currentIndex = (currentIndex + 1) % messages.length;
    }}

    updateText();
    setInterval(updateText, 15000); 

    scrollingText.addEventListener('animationend', updateText);

    document.getElementById('close-announcement').addEventListener('click', function() {{
        this.closest('.announcement-container').style.display = 'none';
    }});
    </script>

    <style>
    @keyframes scroll-left {{
        0% {{ transform: translateX(100%); }}
        100% {{ transform: translateX(-100%); }}
    }}
    </style>
    """, unsafe_allow_html=True)
    

def set_background(image_file, is_gif=False):
    """Sets the background image of the Streamlit app."""
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

def get_binary_file_downloader_html(bin_file, file_label='File'):
    bin_str = base64.b64encode(bin_file).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_label}">Download {file_label}</a>'
    return href

def get_resume_file_path(role, document_type):
    file_type = "resume" if document_type == "Resume" else "cover_letter"
    return f"resume/{role.lower().replace(' ', '_')}_{file_type}.pdf"

def display_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def display_resume_section(role):
    st.subheader("Resume & Cover Letter")
    
    col1, col2 = st.columns(2)
    with col1:
        document_choice = st.radio("Select document to view", ["Resume", "Cover Letter"])
    
    file_path = get_resume_file_path(role, document_choice)
    file_label = f"{role} {document_choice}"
    
    try:
        display_pdf(file_path)
        with col2:
            st.markdown(get_binary_file_downloader_html(open(file_path, "rb").read(), file_label), unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"The {file_label} file was not found. Please check if the file exists in the 'resume' folder.")

def save_contact_data(data):
    df = pd.DataFrame([data])
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    return csv_buffer

def display_saved_data():
    try:
        df = pd.read_csv('contact_data.csv')
        st.write(df)
    except FileNotFoundError:
        st.write("No data found.")

def display_contact_form():
    st.markdown("<h2 style='text-align: center; color: #4A4A4A;'>Send me a message</h2>", unsafe_allow_html=True)
    
    # Load Lottie animation
    lottie_contact = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_u25cckyh.json")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if lottie_contact:
            st_lottie(lottie_contact, key="contact_animation", height=300)
        else:
            st.warning("Failed to load contact animation.")
    
    with col2:
        with st.form("contact_form", clear_on_submit=True):
            name = st.text_input("Name", key="name_input")
            email = st.text_input("Email", key="email_input")
            message = st.text_area("Message", key="message_input")
            submit_button = st.form_submit_button("Send Message")

            if submit_button:
                if all([name, email, message]):
                    data = {
                        'Name': name,
                        'Email': email,
                        'Message': message,
                        'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    # Save the data to a CSV file
                    csv_buffer = save_contact_data(data)
                    with open('contact_data.csv', 'ab') as f:
                        f.write(csv_buffer.getvalue())
                    
                    st.success("Thanks for your message! I'll get back to you soon.")
                    
                    # Load and play the local video file
                    video_file = open('nsync_bye_bye_bye.mp4', 'rb')
                    video_bytes = video_file.read()
                    st.video(video_bytes)
                    
                    # Add a fun animation on successful submission
                    success_animation = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_touohxv0.json")
                    if success_animation:
                        st_lottie(success_animation, key="success_animation", height=200)
                    else:
                        st.warning("Failed to load success animation.")
                else:
                    st.warning("Please fill in all fields before submitting.")
            display_saved_data()
def contact_section(role):
    st.markdown("<h1 style='text-align: center; color: #2E86C1;'>Contact Me</h1>", unsafe_allow_html=True)
    
    # Load Lottie animation for contact info
    lottie_contact_info = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_fclga8fl.json")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if lottie_contact_info:
            st_lottie(lottie_contact_info, key="contact_info_animation", height=300)
        else:
            st.warning("Failed to load contact info animation.")
    
    with col2:
        st.markdown("<h3 style='color: #4A4A4A;'>Contact Information</h3>", unsafe_allow_html=True)
        contact_info = {
            "Phone": "+91-9912357968",
            "Email": "shahidnazeerds@gmail.com",
            "Location": "Hyderabad, India",
            "LinkedIn": "[LinkedIn Profile](https://www.linkedin.com/in/yourprofile)"
        }
        for key, value in contact_info.items():
            st.markdown(f"<p><strong>{key}:</strong> {value}</p>", unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    display_contact_form()
