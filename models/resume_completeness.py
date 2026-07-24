import re

def calculate_resume_completeness(resume_text):

    score = 0

    text = resume_text.lower()

    # Email
    if re.search(r"\S+@\S+", resume_text):
        score += 10

    # Phone
    if re.search(r"\+?\d[\d\s-]{8,15}", resume_text):
        score += 10

    # Education
    education_keywords = [
        "b.tech",
        "b.e",
        "m.tech",
        "degree",
        "university",
        "college"
    ]

    if any(word in text for word in education_keywords):
        score += 15

    # Projects
    if "project" in text:
        score += 15

    # Experience
    if "experience" in text or "internship" in text:
        score += 15

    # Certifications
    if "certificate" in text or "certification" in text:
        score += 10

    # GitHub
    if "github.com" in text:
        score += 10

    # LinkedIn
    if "linkedin.com" in text:
        score += 10

    # Skills Section
    if "skills" in text:
        score += 5

    return score