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
        body {
            background: linear-gradient(to right, #f7f7f7, #e7e7e7);
            overflow: hidden;  /* Ensure particles don't cause scrollbars */
            margin: 0;  /* Remove default margin */
            padding: 0;  /* Remove default padding */
        }
        .particle {
            position: absolute;
            background-image: url('https://upload.wikimedia.org/wikipedia/en/4/41/Flag_of_India.svg');  /* Indian flag image */
            background-size: cover;
            width: 30px;
            height: 20px;
            opacity: 0.8;
            animation: particleAnimation 10s linear infinite;
        }
        @keyframes particleAnimation {
            0% { transform: translateY(100vh) rotate(0deg); opacity: 0.8; }
            100% { transform: translateY(-100vh) rotate(360deg); opacity: 0; }
        }
        .big-font {
            font-size: 3rem;
            font-weight: bold;
            text-align: center;
            margin: 0;  /* Remove default margin */
            padding: 0;  /* Remove default padding */
        }
        .medium-font {
            font-size: 1.5rem;
            text-align: center;
            margin: 0;  /* Remove default margin */
            padding: 0;  /* Remove default padding */
        }
        .small-font {
            font-size: 1rem;
            text-align: center;
            margin: 0;  /* Remove default margin */
            padding: 0;  /* Remove default padding */
        }
        h1 {
            margin-bottom: 0.5rem;  /* Reduce the bottom margin */
        }
        h2 {
            margin-bottom: 0.5rem;  /* Reduce the bottom margin */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Add the canvas element (You'll need to implement the actual animation logic)
    st.markdown(
        """
        <canvas id="indian-flag-canvas"></canvas>
        <script>
        // JavaScript code for canvas animation (replace with your actual animation logic)
        const canvas = document.getElementById('indian-flag-canvas');
        const ctx = canvas.getContext('2d');

        // Ensure the canvas covers the entire viewport
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        // Example animation logic
        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            // Your drawing logic here
            requestAnimationFrame(draw);
        }
        draw();
        </script>
        """,
        unsafe_allow_html=True
    )

def create_indian_flag_particles(count=100):
    for _ in range(count):
        left = random.randint(0, 100)
        top = random.randint(0, 100)
        delay = random.uniform(0, 5)
        size = random.randint(5, 15)
        duration = random.uniform(4, 8)
        st.markdown(
            f"""
            <div class="particle" style="left: {left}vw; top: {top}vh; 
            animation-delay: {delay}s; width: {size}px; height: {size}px;
            animation-duration: {duration}s;"></div>
            """,
            unsafe_allow_html=True
        )

