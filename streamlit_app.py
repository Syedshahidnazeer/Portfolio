import os
import streamlit as st

def main():
    # Get the current working directory
    current_dir = os.getcwd()

    st.title("My Portfolio")
    st.image(os.path.join(current_dir, "images", "1.jpg"), use_column_width=True)
    st.write("Hi, I'm [Your Name]. I'm passionate about data science and machine learning.")
    st.write("Studies:")
    st.write("- [Your Degree], [Your University]")
    st.write("Experiences:")
    st.write("- [Your Previous Job 1]")
    st.write("- [Your Previous Job 2]")

if __name__ == "__main__":
    main()
