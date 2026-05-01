🚀 AI Resume Screener (ATS-Based)

An intelligent AI-powered Resume Screening System that analyzes resumes and ranks candidates based on job requirements using ATS (Applicant Tracking System) scoring

📌 Features
1. Upload multiple resumes (PDF format)
2. AI-based resume analysis
3. ATS Score calculation (in percentage)
4. Skill extraction from resumes
5. Project detection
6. Certificate identification
7. Candidate selection/rejection based on score
8. Clean and interactive UI using Streamlit

🛠️ Tech Stack
1. Python
2. Streamlit
3. Natural Language Processing (NLP)
4. PyPDF2 / PDFMiner (for text extraction)
5. Scikit-learn (for similarity scoring)

📂 Project Structure

RESUME_SCREENING_PROJECT/
│
├── app.py
├── utils.py
│
├── data/
│   ├── resumes/
│   ├── job_description.txt
│   └── ATS_Results.xlsx
│
├── requirements.txt
├── README.md
└── .gitignore


⚙️ Installation
1️⃣ Clone the repository
git clone https://github.com/your-username/ai-resume-screener.git
cd ai-resume-screener

2️⃣ Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate   # For Mac/Linux
venv\Scripts\activate      # For Windows

3️⃣ Install dependencies
pip install -r requirements.txt

▶️ Usage
Run the Streamlit app:
streamlit run app.py
        OR
open in browser:
http://localhost:8501

📊 How It Works
1. Upload resumes (PDF)
2. Extract text from each resume
3. Match resume content with job description
4. Calculate similarity score (ATS Score)
5. Extract:
   a. Skills
   b. Projects
   c. Certifications
6. Rank candidates
7. Display results with selection status


🧠 ATS Scoring Logic
Uses text similarity (TF-IDF / Cosine Similarity)
Scores range from 0 to 100%
Higher score = better match with job description

