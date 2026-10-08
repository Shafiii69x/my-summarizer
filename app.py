import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI Text Summarizer", page_icon="✨", layout="wide")

st.markdown("""
<style>
    .main-header {font-size: 2.5rem; color: #1E90FF; text-align: center; margin-bottom: 10px;}
    .sub-header {font-size: 1.2rem; color: #555; text-align: center;}
    .stButton>button {background-color: #1E90FF; color: white; border-radius: 10px; padding: 10px 20px;}
    .stTextArea textarea {border-radius: 10px;}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">✨ AI Text Summarizer</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Smart • Fast • Beautiful Interface</p>', unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    api_key = st.text_input("🔑 Gemini API Key", type="password", placeholder="Enter your key here")
    text = st.text_area("📝 Paste your text here", height=280, placeholder="Enter the text you want to summarize...")

with col2:
    summary_style = st.selectbox("📌 Summary Style", ["Short & Concise", "Bullet Points", "Detailed Explanation"])

if st.button("🚀 Generate Summary", use_container_width=True):
    if not api_key or not text.strip():
        st.warning("⚠️ Please enter API key and text.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-3.8-flash")

            if summary_style == "Short & Concise":
                prompt = f"Summarize in 2-3 sentences:\n\n{text}"
            elif summary_style == "Bullet Points":
                prompt = f"Summarize in bullet points:\n\n{text}"
            else:
                prompt = f"Provide a detailed summary:\n\n{text}"

            response = model.generate_content(prompt)

            st.success("✅ Summary Ready!")
            st.subheader("📄 Your Summary")
            st.write(response.text)

            if st.button("📋 Copy to Clipboard"):
                st.toast("Copied successfully!")

        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")
st.caption("DATA X | Powered by Shafi")
