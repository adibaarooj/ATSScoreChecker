from dotenv import load_dotenv

load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_cotent,prompt):
    model = genai.GenerativeModel("gemini-2.5-flash")
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        images = pdf2image.convert_from_bytes(
        uploaded_file.read(),
        poppler_path=r"C:\Program Files (x86)\Poppler\Library\bin"
)

        first_page=images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App

st.set_page_config(page_title="ATS Resume Scorer", page_icon=":guardsman:", layout="wide")
st.header("ATS Scoring System")
input_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF, DOCX, DOC)...",type=["pdf","DOCX","DOC"],key="file_uploader")


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")


submit1 = st.button("Tell Me About the Resume.")

submit2 = st.button("Areas of imporvement in the Resume.")

submit3 = st.button("ATS Score of the Resume.")

submit4 = st.button("Tell the skills that match and the skills that are missing in the resume.")

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
your task is to evaluate the resume against the provided job description 
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
            "github_or_portfolio": 3
        }
    },
    "Resume Structure & Formatting": {
        "weight": 15,
        "criteria": {
            "section_headings": 4,
            "consistent_formatting": 3,
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
        "weight": 20,
        "criteria": {
            "experience_section": 5,
            "internship_or_work_experience": 5,
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
    },
    "Impact & Quantification": {
        "weight": 10,
        "criteria": {
            "5_or_more_metrics": 10,
            "3_to_4_metrics": 7,
            "1_to_2_metrics": 4,
            "none": 0
        }
    }
}

Given the above scoring configuration, please evaluate the provided resume against the job description. and display in the 
format of a table with the following columns: Category, Weight, Criteria, Score,points gained and Comments.
also give a final score out of 100 and percentage based on the weighted average of the scores in each category.   
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit4:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt4,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit5:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt5,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")
