# src/utils/skill_extractor.py

import re

# Predefined technical skill set
SKILL_SET = {
    "python", "java", "c++", "javascript", "html", "css",
    "react", "node", "django", "flask", "fastapi",
    "mongodb", "mysql", "postgresql", "sql",
    "aws", "docker", "kubernetes",
    "tensorflow", "pytorch", "scikit-learn",
    "nlp", "deep learning", "machine learning",
    "linux", "git", "ci/cd", "rest", "api",
    "bootstrap"
}

def extract_skills(text):
    text = text.lower()
    found_skills = set()

    for skill in SKILL_SET:
        # match whole word skills
        if re.search(r"\b" + re.escape(skill) + r"\b", text):
            found_skills.add(skill)

    return found_skills
def calculate_skill_match(resume_text, job_description):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    if not job_skills:
        return 0, [], []

    matched = resume_skills.intersection(job_skills)
    missing = job_skills - resume_skills

    score = len(matched) / len(job_skills)

    return score, list(matched), list(missing)
