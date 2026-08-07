import re
from .resume_sections import detect_resume_sections

def calculate_resume_completeness(resume_text):

    text = resume_text.lower()

    sections = detect_resume_sections(resume_text)

    score = 0

    if sections["Contact Information"]:
        score += 20

    if sections["Education"]:
        score += 15

    if sections["Projects"]:
        score += 15

    if sections["Experience"]:
        score += 15

    if sections["Certifications"]:
        score += 10

    if sections["GitHub"]:
        score += 10

    if sections["LinkedIn"]:
        score += 10

    if sections["Skills"]:
        score += 5

    return score