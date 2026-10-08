import streamlit as st
import google.generativeai as genai
from io import StringIO
import PyPDF2
from docx import Document

st.set_page_config(page_title="AI Text Summarizer", page_icon="✨", layout="wide")

st.markdown("""
<style>
    .main-header {font-size: 2.5rem; color: #1E90FF; text-align: center; margin-bottom: 10px;}
    .sub-header {font-size: 1.2rem; color: #555; text-align: center;}
    .stButton>button {background-color: #1E90FF; color: white; border-radius: 10px; padding: 10px 20px;}
    .stTextArea textarea {border-radius: 10px;}
    .success-box {background-color: #d4edda; color: #155724; padding: 15px; border-radius: 10px;}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">✨ AI Text Summarizer</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Smart • Fast • Beautiful Interface with File Upload & Multilingual Support</p>', unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    api_key = st.text_input("🔑 Gemini API Key", type="password", placeholder="Enter your key here")

    uploaded_file = st.file_uploader("📁 Upload File (TXT, PDF, DOCX)", type=["txt", "pdf", "docx"])
    text = st.text_area("📝 Or Paste your text here", height=200, placeholder="Enter the text you want to summarize...")

    if uploaded_file:
        if uploaded_file.type == "text/plain":
            text = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
        elif uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = "".join([page.extract_text() for page in pdf_reader.pages])
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(uploaded_file)
            text = "\n".join([p.text for p in doc.paragraphs])

with col2:
    summary_style = st.selectbox("📌 Summary Style", ["Short & Concise", "Bullet Points", "Detailed Explanation"])
    lang_option = st.selectbox("🌐 Output Language", ["Auto Detect", "English", "Bangla"])

if st.button("🚀 Generate Summary", use_container_width=True):
    if not api_key or not text.strip():
        st.warning("⚠️ Please enter API key and text.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")

            lang_prompt = ""
            if lang_option == "Bangla":
                lang_prompt = "Respond in Bangla."
            elif lang_option == "English":
                lang_prompt = "Respond in English."

            if summary_style == "Short & Concise":
                prompt = f"{lang_prompt} Summarize in 2-3 sentences:\n\n{text}"
            elif summary_style == "Bullet Points":
                prompt = f"{lang_prompt} Summarize in bullet points:\n\n{text}"
            else:
                prompt = f"{lang_prompt} Provide a detailed summary:\n\n{text}"

            response = model.generate_content(prompt)

            st.markdown('<div class="success-box">✅ Summary Ready!</div>', unsafe_allow_html=True)
            st.subheader("📄 Your Summary")
            summary_text = response.text
            st.write(summary_text)

            if st.button("📋 Copy to Clipboard"):
                st.toast("Copied successfully!")

        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")
st.caption("DATA X | Powered by Shafi Alam")
