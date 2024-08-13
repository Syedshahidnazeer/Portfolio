import streamlit as st
import random

def apply_indian_flag_animation_style():
    st.markdown(
        """
        <style>
        #indian-flag-canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1; /* Place the canvas behind other elements */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Add the canvas element
    st.markdown(
        """
        <canvas id="indian-flag-canvas"></canvas>
        <script>
        // JavaScript code for canvas animation (replace with your actual animation logic)
        const canvas = document.getElementById('indian-flag-canvas');
        const ctx = canvas.getContext('2d');

        // ... your animation code here ...
        </script>
        """,
        unsafe_allow_html=True
    )

def create_indian_flag_particles(count=100):
    colors = ['saffron', 'white', 'green', 'chakra']
    for i in range(count):
        left = random.randint(0, 100)
        top = random.randint(0, 100)
        delay = random.uniform(0, 5)
        color = colors[i % 4]
        size = random.randint(5, 15)
        duration = random.uniform(4, 8)
        st.markdown(
            f"""
            <div class="particle {color}" style="left: {left}vw; top: {top}vh; 
            animation-delay: {delay}s; width: {size}px; height: {size}px;
            animation-duration: {duration}s;"></div>
            """,
            unsafe_allow_html=True
        )

def display_page_with_indian_flag_animation(page_name):
    apply_indian_flag_animation_style()
    create_indian_flag_particles()
    st.title(page_name)
    st.write(f"This is the {page_name} page with an enhanced Indian flag particle animation.")
