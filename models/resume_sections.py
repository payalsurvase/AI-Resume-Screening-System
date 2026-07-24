import re

def detect_resume_sections(resume_text):

    text = resume_text.lower()

    sections = {}

    # Contact Information
    email = bool(re.search(r"\S+@\S+", resume_text))
    phone = bool(re.search(r"\+?\d[\d\s-]{8,15}", resume_text))

    sections["Contact Information"] = email and phone

    # Education
    education_keywords = [
        "education",
        "b.tech",
        "b.e",
        "m.tech",
        "degree",
        "college",
        "university"
    ]

    sections["Education"] = any(word in text for word in education_keywords)

    # Skills
    sections["Skills"] = "skills" in text

    # Projects
    sections["Projects"] = "project" in text

    # Experience
    sections["Experience"] = (
        "experience" in text or
        "internship" in text
    )

    # Certifications
    sections["Certifications"] = (
        "certification" in text or
        "certificate" in text
    )

    # GitHub
    sections["GitHub"] = "github.com" in text

    # LinkedIn
    sections["LinkedIn"] = "linkedin.com" in text

    return sections