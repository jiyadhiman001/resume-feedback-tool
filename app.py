import os
import streamlit as st
import pdfplumber
import base64
import io
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="Resume Feedback Tool", page_icon="📄", layout="centered")
st.title("📄 Resume Feedback Tool")
st.subheader("Upload your resume and get AI-powered feedback instantly!")

uploaded_file = st.file_uploader("Upload your Resume (PDF only)", type="pdf")

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_image_pdf(file_bytes):
    import pypdfium2 as pdfium
    pdf = pdfium.PdfDocument(file_bytes)
    all_text = ""
    for page in pdf:
        bitmap = page.render(scale=2)
        pil_image = bitmap.to_pil()
        img_byte_arr = io.BytesIO()
        pil_image.save(img_byte_arr, format='PNG')
        base64_image = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract all text from this resume image. Return only the extracted text, nothing else."},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                ]
            }]
        )
        all_text += response.choices[0].message.content + "\n"
    return all_text

def get_resume_feedback(resume_text):
    prompt = f"""
    You are an expert HR professional and resume coach.
    Analyze the following resume and provide detailed feedback in this exact format:

    **Overall Score: X/10**

    **✅ Strengths:**
    - List key strengths

    **❌ Weaknesses:**
    - List main weaknesses

    **💡 Improvements:**
    - List specific improvements

    **🎯 ATS Tips:**
    - List ATS optimization tips

    Resume:
    {resume_text}
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

resume_text = ""
if uploaded_file is not None:
    with st.spinner("Reading your resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    if resume_text.strip() == "":
        st.warning("⚠️ Image-based PDF detected! Extracting text using AI Vision...")
        with st.spinner("AI is reading your image-based resume..."):
            resume_text = extract_text_from_image_pdf(uploaded_file.getvalue())
        if resume_text.strip() != "":
            st.success("✅ Resume extracted successfully!")
    else:
        st.success("✅ Resume uploaded successfully!")

    if resume_text.strip() != "":
        if st.button("Get Feedback from PDF 🚀"):
            with st.spinner("AI is analyzing your resume..."):
                feedback = get_resume_feedback(resume_text)
            st.markdown("---")
            st.markdown("## 📊 Your Resume Feedback")
            st.markdown(feedback)
            st.download_button(
                label="📥 Download Feedback",
                data=feedback,
                file_name="resume_feedback.txt",
                mime="text/plain"
            )

st.markdown("---")
st.markdown("### ✍️ Or paste your resume text manually:")
manual_text = st.text_area("Paste your resume here", height=300)

if st.button("Get Feedback 🚀"):
    if manual_text.strip() != "":
        with st.spinner("AI is analyzing your resume..."):
            feedback = get_resume_feedback(manual_text)
        st.markdown("---")
        st.markdown("## 📊 Your Resume Feedback")
        st.markdown(feedback)
        st.download_button(
            label="📥 Download Feedback",
            data=feedback,
            file_name="resume_feedback.txt",
            mime="text/plain"
        )
    else:
        st.error("❌ Please paste your resume text first!")