import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from utils import *

st.set_page_config(page_title="AI ATS Screener", layout="wide")

st.title("🤖 AI ATS Resume Screening System")

threshold = st.sidebar.slider("Selection Threshold (%)", 0, 100, 40)

# Load Job Description
with open("job_description.txt", "r") as f:
    job_desc = f.read()

files = st.file_uploader("📤 Upload Resumes", type=["pdf"], accept_multiple_files=True)

if st.button("🚀 Analyze Resumes"):

    if files:

        names = []
        resumes = []

        skills_data = []
        proj_data = []
        intern_data = []
        grammar_data = []

        # -------------------------
        # Extract Resume Data
        # -------------------------
        for file in files:
            text = extract_text_from_pdf(file)

            resumes.append(text)
            names.append(file.name)

            skills_data.append(extract_skills(text))
            proj_data.append(extract_projects(text))
            intern_data.append(extract_internships(text))

            errors, ratio = check_grammar(text)
            grammar_data.append((errors, ratio))

        # -------------------------
        # Similarity (JD match)
        # -------------------------
        docs = [job_desc] + resumes
        tfidf = TfidfVectorizer().fit_transform(docs)
        sim = cosine_similarity(tfidf[0:1], tfidf[1:])[0]

        # -------------------------
        # ATS + Ranking Score
        # -------------------------
        ats_scores = []
        rank_scores = []

        for i in range(len(resumes)):

            ats = calculate_ats_score(
                sim[i],
                skills_data[i],
                proj_data[i],
                grammar_data[i][1]
            )

            ats_scores.append(ats)

            rank_scores.append(
                calculate_ranking_score(
                    proj_data[i],
                    intern_data[i]
                )
            )

        # -------------------------
        # Combine Results
        # -------------------------
        combined = []

        for i in range(len(names)):

            errors, ratio = grammar_data[i]

            if ratio > 0.20:
                status = "Rejected"
            else:
                status = "Selected" if ats_scores[i] >= threshold else "Rejected"

            combined.append((
                names[i],
                ats_scores[i],
                rank_scores[i],
                status,
                errors
            ))

        # -------------------------
        # Sorting
        # -------------------------
        ranked = sorted(
            combined,
            key=lambda x: (x[3] == "Selected", x[2], x[1]),
            reverse=True
        )

        # -------------------------
        # Display
        # -------------------------
        st.subheader("🏆 Final Ranked Candidates")

        results = []

        for rank, (name, ats, rscore, status, errors) in enumerate(ranked, start=1):

            i = names.index(name)

            st.markdown("---")
            st.markdown(f"## 🥇 Rank #{rank} - {name}")

            st.write(f"📊 ATS Score: {round(ats, 2)}%")
            st.write(f"🏆 Ranking Score: {rscore}")
            st.write(f"✍️ Grammar Errors: {errors}")

            st.progress(ats / 100)

            # Skills
            st.write("🧠 Skills:")
            st.write(", ".join(skills_data[i]) if skills_data[i] else "No skills found")

            # Projects (SAFE)
            st.write("🚀 Projects:")
            if i < len(proj_data) and proj_data[i]:
                for p in proj_data[i]:
                    if len(p) < 80:
                        st.write(f"• {p}")
            else:
                st.write("No projects found")

            # Internships
            st.write("💼 Internships:")
            if intern_data[i]:
                for x in intern_data[i]:
                    st.write(f"• {x}")
            else:
                st.write("No internships")

            # Status
            if status == "Selected":
                st.success("✅ Selected")
            else:
                st.error("❌ Rejected")

            results.append({
                "Rank": rank,
                "Name": name,
                "ATS Score": round(ats, 2),
                "Ranking Score": rscore,
                "Grammar Errors": errors,
                "Skills": ", ".join(skills_data[i]),
                "Projects": ", ".join(proj_data[i]),
                "Internships": ", ".join(intern_data[i]),
                "Status": status
            })

        # -------------------------
        # Download Excel
        # -------------------------
        df = pd.DataFrame(results)

        file_path = "ATS_Results.xlsx"
        df.to_excel(file_path, index=False)

        with open(file_path, "rb") as f:
            st.download_button(
                "📥 Download Excel Report",
                f,
                file_name="ATS_Results.xlsx"
            )

    else:
        st.warning("⚠️ Please upload resumes first!")