import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI Text Summarizer", page_icon="✨")
st.title("✨ AI Text Summarizer")
st.write("Paste your text below and get a short summary.")

api_key = st.text_input("Enter your Gemini API Key", type="password")
text = st.text_area("Enter text to summarize", height=220)

if st.button("✨ Summarize Now"):
    if not api_key:
        st.warning("Please enter your Gemini API key.")
    elif not text.strip():
        st.warning("Please provide some data first.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-3.8-flash")
            prompt = f"Summarize the following text in a short and clear way:\n\n{text}"
            response = model.generate_content(prompt)
            st.subheader("Summary")
            st.write(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
