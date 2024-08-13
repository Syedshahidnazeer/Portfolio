import streamlit as st
from streamlit_lottie import st_lottie
import requests
import random  # Import the random module

# ... rest of your code ...

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# --- Load Lottie Animation ---
lottie_coding = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_vnikrcia.json")  # Replace with your chosen animation URL

# --- Particle Animation CSS ---
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(to right, #f7f7f7, #e7e7e7);
    }
    .particle {
        position: absolute;
        background-color: #888;
        border-radius: 50%;
        opacity: 0.5;
        animation: particleAnimation 5s linear infinite;
    }
    @keyframes particleAnimation {
        0% { transform: translate(0, 0); opacity: 0.5; }
        100% { transform: translate(100vw, -50vh); opacity: 0; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Create Particles ---
for _ in range(20):  # Adjust the number of particles as needed
    st.markdown(
        f'<div class="particle" style="left: {random.randint(0, 100)}vw; top: {random.randint(0, 100)}vh; width: {random.randint(2, 5)}px; height: {random.randint(2, 5)}px;"></div>',
        unsafe_allow_html=True,
    )

# --- Hero Section Content ---
st.markdown(
    """
    <div style="text-align: center;">
        <h1 style="font-size: 4rem; font-weight: bold;">Your Name</h1>
        <h2 style="font-size: 2rem; margin-bottom: 2rem;">Data Scientist | Python Developer | Streamlit Enthusiast</h2>
        <a href="#projects" style="padding: 1rem 2rem; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px;">View My Projects</a>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Lottie Animation ---
st_lottie(lottie_coding, speed=1, height=300, key="coding")