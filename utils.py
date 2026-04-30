import re
import PyPDF2


# 📄 Extract text from PDF
def extract_text_from_pdf(file):
    text = ""
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


# -------------------------------
# 🧠 Skill extraction
# -------------------------------
def extract_skills(text):
    skills = [
        "python", "machine learning", "data analysis", "ai",
        "sql", "pandas", "numpy", "deep learning", "flask"
    ]
    return list(set([s for s in skills if s in text.lower()]))


# -------------------------------
# 🔥 SMART SECTION SPLITTER (MAIN FIX)
# -------------------------------
def split_sections(text):

    sections = {
        "projects": "",
        "internships": "",
        "skills": "",
        "languages": ""
    }

    current = None

    for line in text.split("\n"):
        l = line.lower().strip()

        # detect section headings
        if "project" in l:
            current = "projects"
            continue
        elif "internship" in l or "experience" in l:
            current = "internships"
            continue
        elif "skill" in l:
            current = "skills"
            continue
        elif "language" in l:
            current = "languages"
            continue

        # store content
        if current:
            sections[current] += line + "\n"

    return sections


# -------------------------------
# 🚀 FIXED PROJECT EXTRACTION
# -------------------------------
def extract_projects(text):
    projects = []

    text = text.replace("\r", "\n")
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    for line in lines:

        low = line.lower()

        # 🎯 detect project-like lines
        if any(keyword in low for keyword in [
            "project", "assistant", "prediction", "chatbot", "analysis"
        ]):

            # ❌ skip non-project garbage
            if any(bad in low for bad in [
                "language", "hindi", "english", "skill", "education"
            ]):
                continue

            # length filter
            if 5 < len(line) < 60:
                projects.append(line)

    # remove duplicates
    return list(dict.fromkeys(projects))


# -------------------------------
# 💼 FIXED INTERNSHIP EXTRACTION
# -------------------------------
def extract_internships(text):

    sections = split_sections(text)
    intern_text = sections["internships"]

    internships = []

    for line in intern_text.split("\n"):
        line = line.strip()

        if len(line) < 5:
            continue

        internships.append(line)

    return list(set(internships))


# -------------------------------
# 🎯 ATS Score
# -------------------------------
def calculate_ats_score(similarity, skills, projects, grammar_ratio):

    skill_score = len(skills) / 8
    project_score = min(len(projects) / 5, 1)

    grammar_penalty = max(0, 1 - grammar_ratio * 4)

    final = (
        0.55 * similarity +
        0.25 * skill_score +
        0.15 * project_score +
        0.05 * grammar_penalty
    )

    return min(final * 100, 100)


# -------------------------------
# 🏆 Ranking score
# -------------------------------
def calculate_ranking_score(projects, internships):
    return (len(projects) * 4) + (len(internships) * 6)


# -------------------------------
# 📝 Grammar Checker
# -------------------------------
def check_grammar(text):

    if not text:
        return 0, 0.0

    sentences = text.split(".")
    words = text.split()

    errors = 0

    # short sentences
    for s in sentences:
        if 0 < len(s.split()) < 4:
            errors += 1

    # repeated words
    for i in range(len(words) - 1):
        if words[i].lower() == words[i + 1].lower():
            errors += 1

    # lowercase start
    for s in sentences:
        s = s.strip()
        if s and s[0].islower():
            errors += 1

    total_words = max(len(words), 1)
    error_ratio = errors / total_words

    return errors, error_ratio