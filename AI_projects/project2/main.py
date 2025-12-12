import streamlit as st #learn some basics of streamlit
import PyPDF2 #for PDF text extraction
import io #for handling file streams
import os #for environment variables
from openai import OpenAI #OpenAI client
from dotenv import load_dotenv #for loading environment variables

load_dotenv()

st.set_page_config(page_title="AI Resume Critiquer", page_icon=":robot_face:", layout="centered")

st.title("AI Resume Critiquer")
st.markdown("Upload your resume and job description, and get AI-powered feedback!")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

uploaded_resume = st.file_uploader("Upload your Resume (PDF or TXT)", type=["pdf", "txt"])
job_role = st.text_input("Enter the Job Role/Description")

analyze = st.button("Analyze Resume")

def extract_text_from_PDF(uploaded_resume):
    pdf_reader = PyPDF2.PdfReader(uploaded_resume)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_file(uploaded_resume):
    if uploaded_resume.type == "application/pdf":
        return extract_text_from_PDF(io.BytesIO(uploaded_resume.read()))
    return uploaded_resume.read().decode("utf-8")
    
if analyze and uploaded_resume and job_role:
    try:
        file_content = extract_text_from_file(uploaded_resume)

        if not file_content.strip():
            st.error("Unsupported file type. Please upload a PDF or TXT file.")
            st.stop()
        
        prompt = f"""Please analyze this resume and provide constructive feedback based on the following job role/description:
Job Role/Description: {job_role}
        Focus on the following aspects:
        1. Relevance of skills and experience
        2. Clarity and conciseness
        3. Overall presentation and formatting
        Provide specific suggestions for improvement.
        Resume Content:
        {file_content}

        Please provide your feedback in a clear, structured format with specific suggestions for improvement."""

        client = OpenAI(api_key=OPENAI_API_KEY)

        prompt = f"Provide feedback on the following resume for the job role described below:\n\nJob Role/Description: {job_role}\n\nResume:\n{resume_text}\n\nFeedback:"
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert career advisor."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7,
        )

        feedback = response.choices[0].message.content
        st.subheader("AI Feedback on Your Resume")
        st.write(feedback)

        # st.markdown("### AI Feedback on Your Resume")
        # st.markdown(response.choices[0].message.content)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")