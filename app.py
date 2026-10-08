import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI Text Summarizer", page_icon="✨", layout="centered")

st.title("✨ AI Text Summarizer")
st.markdown("### Smart • Fast • Accurate")

api_key = st.text_input("🔑 Enter your Gemini API Key", type="password")

text = st.text_area("📝 Enter text to summarize", height=200)

summary_style = st.selectbox(
    "📌 Choose Summary Style",
    ["Short & Concise", "Bullet Points", "Detailed Explanation"]
)

if st.button("🚀 Generate Summary", use_container_width=True):
    if not api_key:
        st.warning("⚠️ Please enter your Gemini API key.")
    elif not text.strip():
        st.warning("⚠️ Please provide some text first.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-3.8-flash")

            if summary_style == "Short & Concise":
                prompt = f"Summarize the following text in 2-3 sentences:\n\n{text}"
            elif summary_style == "Bullet Points":
                prompt = f"Summarize the following text in bullet points:\n\n{text}"
            else:
                prompt = f"Provide a detailed summary of the following text:\n\n{text}"

            response = model.generate_content(prompt)

            st.success("✅ Summary Generated Successfully!")
            st.subheader("📄 Summary")
            st.write(response.text)

            if st.button("📋 Copy Summary"):
                st.toast("Summary copied to clipboard!")

        except Exception as e:
            st.error(f"❌ Error: {e}")

st.markdown("---")
st.caption("DATA X | Powered by Shafi")
