import streamlit as st
import google.generativeai as genai
import pdfplumber
from docx import Document
from PIL import Image
import io

# ===== SETUP =====
st.set_page_config(page_title="Free Data Summarizer", layout="centered")
st.title("📄 Summarize Anything – Free")

# Get your free API key at https://aistudio.google.com/apikey
API_KEY = st.text_input("Paste your Gemini API Key (free):", type="password")
if not API_KEY:
    st.info("Get a free key at https://aistudio.google.com/apikey – no credit card needed.")
    st.stop()

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-pro")

# ===== OUTPUT FORMAT CHOICE =====
output_style = st.selectbox(
    "Choose output format:",
    [
        "Bullet points (key takeaways)",
        "Table: Topic | Key Point | Action Item",
        "Summary + Key Points + Recommendations",
        "JSON (structured data)",
        "One‑paragraph summary"
    ]
)

# ===== INPUT METHOD =====
input_method = st.radio("How to input data?", ["Paste text", "Upload photo", "Upload file (PDF/DOCX/TXT)"])

text_input = ""
if input_method == "Paste text":
    text_input = st.text_area("Paste your data here:", height=200)
elif input_method == "Upload photo":
    uploaded_photo = st.file_uploader("Upload a photo (JPG, PNG):", type=["jpg", "jpeg", "png"])
    if uploaded_photo:
        image = Image.open(uploaded_photo)
        st.image(image, caption="Uploaded photo", use_column_width=True)
        # Gemini OCR
        prompt = "Extract all text from this image exactly as written."
        response = model.generate_content([prompt, image])
        text_input = response.text
        st.success("Text extracted from photo!")
        with st.expander("Show extracted text"):
            st.write(text_input)
else:  # File upload
    uploaded_file = st.file_uploader("Upload file:", type=["pdf", "docx", "txt"])
    if uploaded_file:
        if uploaded_file.name.endswith(".txt"):
            text_input = uploaded_file.read().decode("utf-8")
        elif uploaded_file.name.endswith(".pdf"):
            with pdfplumber.open(uploaded_file) as pdf:
                text_input = "".join(page.extract_text() for page in pdf.pages)
        elif uploaded_file.name.endswith(".docx"):
            doc = Document(uploaded_file)
            text_input = "\n".join(p.text for p in doc.paragraphs)

# ===== SUMMARIZE =====
if st.button("✨ Summarize Now") and text_input.strip():
    with st.spinner("Thinking..."):
        # Build prompt based on chosen output format
        prompt_map = {
            "Bullet points (key takeaways)": "Summarize the following text in 5‑10 bullet points. Start each bullet with a dash. Only output the bullet list.",
            "Table: Topic | Key Point | Action Item": "Summarize the following text as a markdown table with columns: Topic, Key Point, Action Item. Output only the table.",
            "Summary + Key Points + Recommendations": "Summarize the following text in three sections: **Summary**, **Key Points** (bullet list), **Recommendations** (bullet list). Use markdown headings.",
            "JSON (structured data)": "Summarize the following text and output the result as a JSON object with keys: 'summary', 'key_points' (array), 'recommendations' (array). Output ONLY valid JSON, no other text.",
            "One‑paragraph summary": "Summarize the following text in one clear, concise paragraph."
        }
        prompt = prompt_map[output_style]
        full_prompt = f"{prompt}\n\n---\n{text_input[:30000]}"  # limit to avoid token issues
        response = model.generate_content(full_prompt)
        st.subheader("✅ Structured Summary")
        st.markdown(response.text)
else:
    if text_input.strip() == "":
        st.warning("Please provide some data first.")
