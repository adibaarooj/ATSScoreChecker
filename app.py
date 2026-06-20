from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import tempfile
import google.generativeai as genai
from pypdf import PdfReader
from docx import Document
import textract

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def extract_text_from_file(uploaded_file):
    file_extension = os.path.splitext(uploaded_file.name)[1].lower()

    if file_extension == ".pdf":
        pdf_reader = PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text

    elif file_extension == ".docx":
        doc = Document(uploaded_file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text

    elif file_extension == ".doc":
        with tempfile.NamedTemporaryFile(delete=False, suffix=".doc") as temp_file:
            temp_file.write(uploaded_file.read())
            temp_path = temp_file.name

        text = textract.process(temp_path).decode("utf-8")
        os.remove(temp_path)
        return text

    else:
        raise ValueError("Unsupported file format")

def get_gemini_response(prompt, resume_text, job_description):
    model = genai.GenerativeModel("gemini-3.1-flash-lite")

    final_prompt = f"""
{prompt}

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}
"""

    response = model.generate_content(
        final_prompt,
        generation_config={
            "temperature": 0.2,
            "max_output_tokens": 1000
        }
    )
    return response.text

def get_gemini_response5(prompt, resume_text, job_description,fast=True):
    model = genai.GenerativeModel("gemini-2.5-flash")
    final_prompt = f"""
{prompt}

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}
"""

    response = model.generate_content(
        final_prompt,
        generation_config={
            "temperature": 0.2}
    )
    return response.text

st.set_page_config(page_title="ATS Resume Scorer", page_icon=":guardsman:", layout="wide")

st.header("ATS Scoring System")

input_text = st.text_area("Job Description:", key="input")

uploaded_file = st.file_uploader(
    "Upload your Resume (PDF, DOCX, DOC)",
    type=["pdf", "docx", "doc"]
)

if uploaded_file is not None:
    st.success("Resume Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("Areas of Improvement in the Resume")
submit3 = st.button("ATS Score of the Resume")
submit4 = st.button("Tell the Skills that Match and the Skills that are Missing in the Resume")
submit5 = st.button("ATS Score out of 100")

input_prompt1 = """
You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description.
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
all in points and not paragraphs
"""

input_prompt2 = """
You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description.
Please share your professional evaluation on how the candidate can improve their skills to better align with the role.
Highlight areas of improvement and suggest relevant training or experience that would enhance their profile.
Actionable recommendations to improve the resume...all in points and not paragraphs
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality,
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.

* An overall ATS-style score (out of 100)
* Key strengths identified in the resume
* Keywords missing from the resume
* Final thoughts on the candidate's fit for the role
"""

input_prompt4 = """
You are an experienced Technical Human Resource Manager, your task is to analyze the provided resume against the job description.
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality,
your task is to evaluate the resume against the provided job description.
Please identify the skills that match and the skills that are missing in the resume.
"""

input_prompt5 = """
SCORING_CONFIG = {
    "Contact & Professional Presence": {
        "weight": 10,
        "criteria": {
            "name": 1,
            "email": 2,
            "phone": 2,
            "linkedin": 2,
            "github": 2,
            "portfolio": 1
        }
    },
    "Resume Structure & Formatting": {
        "weight": 20,
        "criteria": {
            "section_headings": 7,
            "consistent_formatting": 5,
            "bullet_points": 3,
            "ideal_length": 2,
            "ats_friendly_layout": 3
        }
    },
    "Skills Relevance": {
        "weight": 20,
        "criteria": {
            "skill_match_percentage": {
                "90-100": 20,
                "75-89": 16,
                "60-74": 12,
                "40-59": 8,
                "0-39": 4
            }
        }
    },
    "Experience & Internships": {
        "weight": 25,
        "criteria": {
            "experience_section": 5,
            "internship_or_work_experience": 10,
            "technologies_mentioned": 5,
            "responsibilities_described": 5
        }
    },
    "Projects": {
        "weight": 15,
        "criteria": {
            "projects_present": 4,
            "technology_stack_mentioned": 4,
            "project_description_quality": 4,
            "github_links": 3
        }
    },
    "Education": {
        "weight": 5,
        "criteria": {
            "degree": 2,
            "institution": 1,
            "graduation_year": 1,
            "cgpa_or_percentage": 1
        }
    },
    "Certifications & Achievements": {
        "weight": 5,
        "criteria": {
            "certifications": 3,
            "achievements_or_awards": 2
        }
    }
}

Given the above scoring configuration, evaluate the resume text against the job description.give points on all the criterias and 
then give the total points gained in each category and then give the final ATS score out of 100 and also give the percentage match
of the resume with the job description. 

Display:
1. A detailed table with Category, Weight, Criteria, Score(as predefined), Points Gained, 
total of each category(sum of points gained) after each category, and Comments, in least number of tokens possible.
2. Final ATS Score out of 100.
"""

if submit1:
    if uploaded_file is not None:
        resume_text = extract_text_from_file(uploaded_file)
        response = get_gemini_response(input_prompt1, resume_text, input_text)
        st.subheader("Response")
        st.write(response)
    else:
        st.error("Please upload a resume")

elif submit2:
    if uploaded_file is not None:
        resume_text = extract_text_from_file(uploaded_file)
        response = get_gemini_response(input_prompt2, resume_text, input_text)
        st.subheader("Response")
        st.write(response)
    else:
        st.error("Please upload a resume")

elif submit3:
    if uploaded_file is not None:
        resume_text = extract_text_from_file(uploaded_file)
        response = get_gemini_response(input_prompt3, resume_text, input_text)
        st.subheader("Response")
        st.write(response)
    else:
        st.error("Please upload a resume")

elif submit4:
    if uploaded_file is not None:
        resume_text = extract_text_from_file(uploaded_file)
        response = get_gemini_response(input_prompt4, resume_text, input_text)
        st.subheader("Response")
        st.write(response)
    else:
        st.error("Please upload a resume")

elif submit5:
    if uploaded_file is not None:
        resume_text = extract_text_from_file(uploaded_file)
        response = get_gemini_response5(input_prompt5, resume_text, input_text)
        st.subheader("Response")
        st.write(response)
    else:
        st.error("Please upload a resume")