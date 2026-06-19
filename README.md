# 📄 Resume Feedback Tool

An AI-powered resume analyzer that provides instant, detailed feedback to help job seekers improve their resumes.

## 🚀 Features

- 📤 Upload resume in PDF format (text-based or image-based)
- 🤖 AI Vision support for scanned/image-based resumes
- ✍️ Manual text input option
- 📊 Detailed feedback including:
  - Overall Score (out of 10)
  - Strengths
  - Weaknesses
  - Improvement suggestions
  - ATS optimization tips
- 📥 Download feedback as a text file

## 🛠️ Tech Stack

- **Python** - Core programming language
- **Streamlit** - Web app framework
- **Groq API** - Llama 3.3 (text feedback) & Llama 4 Scout (Vision for image-based resumes)
- **pdfplumber** - PDF text extraction
- **pypdfium2** - PDF to image conversion

## ⚙️ How It Works

1. User uploads a resume (PDF) or pastes resume text
2. If PDF is text-based → text extracted directly using pdfplumber
3. If PDF is image-based (scanned) → AI Vision (Groq's Llama 4 Scout) extracts text from the image
4. Extracted text sent to Llama 3.3 model for detailed analysis
5. Structured feedback displayed and available for download

## 📦 Installation

```bash
git clone https://github.com/jiyadhiman001/resume-feedback-tool.git
cd resume-feedback-tool
pip install -r requirements.txt
```

Create a `.env` file and add your Groq API key:
## ▶️ Run the App

```bash
streamlit run app.py
```

## 👩‍💻 Author

**Jiya Dhiman**  
AI Intern @ DevAlpha Foundation  
[LinkedIn](https://www.linkedin.com/in/jiya-dhiman-247b773b6) | [GitHub](https://github.com/jiyadhiman001)