# ATS Resume Analyzer

https://atsscorechecker-adiba.streamlit.app/

ATS Resume Analyzer is a Streamlit-based web application that evaluates a candidate's resume against a given job description using Google's Gemini Large Language Model.(Here "gemini-2.5-flash")

The application accepts resumes in PDF, DOCX, and DOC formats, extracts the textual content, and performs an AI-powered analysis to provide:

* Resume evaluation
* ATS-style scoring
* Skills matching analysis
* Missing keywords identification
* Areas of improvement
* Detailed scoring breakdown
---

## Approach

User Uploads Resume (PDF/DOCX/DOC) + Enters Job Description → 
Text Extraction (PyPDF / python-docx / textract) → 
Prompt Construction → 
Gemini 2.5 Flash Analysis → 
ATS Evaluation Engine → 
ATS Score, Skill Match Analysis, Missing Keywords, Strengths, Weaknesses & Recommendations Displayed in Streamlit

### 1. Resume Upload

The user uploads a resume in one of the following formats:

* PDF
* DOCX
* DOC

The system automatically detects the file type and extracts its textual content.

### 2. Text Extraction

Different extraction techniques are used based on the uploaded file format:

| Format | Extraction Method |
| ------ | ----------------- |
| PDF    | PyPDF             |
| DOCX   | python-docx       |
| DOC    | textract          |

### 3. Job Description Input

The recruiter or user provides a target job description.
The job description acts as the benchmark against which the resume is evaluated.

### 4. AI-Based Analysis

The extracted resume text and job description are provided to Gemini 2.5 Flash along with task-specific prompts.

The model performs:

* Resume review
* ATS scoring
* Keyword matching
* Skill gap analysis
* Improvement recommendations

### 5. Result Presentation

The system displays:

* ATS score
* Resume strengths
* Missing skills
* Recommendations
* Detailed category-wise evaluation

---

## Scoring Methodology

The ATS score is generated using a weighted scoring framework consisting of multiple evaluation categories.

### Category Weights

| Category                        | Weight |
| ------------------------------- | ------ |
| Contact & Professional Presence | 10     |
| Resume Structure & Formatting   | 15     |
| Skills Relevance                | 20     |
| Experience & Internships        | 20     |
| Projects                        | 15     |
| Education                       | 5      |
| Certifications & Achievements   | 5      |
| Impact & Quantification         | 10     |

Total Weight = 100

### Evaluation Criteria

#### Contact & Professional Presence (10)

* Name
* Email
* Phone Number
* LinkedIn Profile
* GitHub/Portfolio

#### Resume Structure & Formatting (15)

* Section headings
* Consistent formatting
* Bullet points
* Appropriate length
* ATS-friendly layout

#### Skills Relevance (20)

The resume is compared against the job description to determine skill alignment.
Higher alignment results in a higher score.

#### Experience & Internships (20)

* Relevant experience
* Internship details
* Technologies used
* Responsibilities described

#### Projects (15)

* Presence of projects
* Technology stack mentioned
* Quality of project descriptions
* GitHub links

#### Education (5)

* Degree
* Institution
* Graduation year
* CGPA/Percentage

#### Certifications & Achievements (5)

* Professional certifications
* Awards and achievements

#### Impact & Quantification (10)

Measures the use of numerical achievements such as:

* Increased efficiency by 30%
* Reduced cost by 15%
* Improved accuracy by 20%

Resumes with quantified impact generally receive higher scores.

### Final Score

The final ATS score is calculated out of 100 based on the weighted performance across all categories.
The ATS Match Percentage indicates how closely the resume aligns with the provided job description.

---

## Technology Stack

### Frontend

* Streamlit

### Backend

* Python

### AI Model

* Google Gemini 2.5 Flash

### Document Processing

* PyPDF
* python-docx
* textract
---

## Future Improvements

### Advanced Keyword Matching

Use NLP techniques such as:

* TF-IDF
* Sentence Embeddings
* Semantic Similarity Models

to improve skill matching accuracy.

### OCR Support

Add OCR capabilities for scanned resumes using:

* Tesseract OCR
* EasyOCR

### Multi-Resume Comparison

Allow recruiters to compare multiple candidates simultaneously.

### Resume Ranking System

Rank resumes automatically based on job suitability.

### Interactive Dashboard

Provide visual analytics such as:

* Skill match charts
* Score distribution
* Missing keyword heatmaps

### Resume Enhancement Suggestions

Generate optimized resume content and ATS-friendly rewrites.

### Support for Multiple Languages

Extend resume analysis capabilities beyond English.

---

## Conclusion

The ATS Resume Analyzer demonstrates how Generative AI can be combined with document processing and resume analysis to provide meaningful candidate feedback. The application offers an accessible way to evaluate resumes, identify skill gaps, and improve job-role alignment while simulating key functionalities of modern Applicant Tracking Systems.
