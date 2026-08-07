import re
from models.project_keywords import PROJECT_KEYWORDS
import streamlit as st

PROJECT_HEADERS = [
    "projects",
    "project",
    "academic projects",
    "personal projects",
    "major projects",
    "minor projects",
    "key projects"
]

STOP_HEADERS = [
    "experience",
    "education",
    "skills",
    "technical skills",
    "certifications",
    "achievements",
    "hobbies",
    "interests",
    "summary",
    "profile",
    "contact"
]

TECH_WORDS = {
    "html","css","javascript","php","mysql",
    "python","java","react","mongodb",
    "node.js","computer vision",
    "opencv","tensorflow","pandas",
    "numpy","scikit-learn",
    "yolo","roboflow"
}


def is_project_title(line):
    
    text = line.strip()
    text = re.sub(
        r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}",
        "",
        text,
        flags=re.I
    ).strip()
    # print("CHECK TITLE:",repr(text))

    if len(text) < 3:
        return False

    # if len(text) > 80:
    #     return False

    lower = text.lower()

    # if "|" in text:
    #     return False

    if lower.startswith("tech:"):
        return False
    
    # Skip descriptions
    text = text.lstrip("•∗▪●■►*- ").strip()

    verbs = {
        "built","developed","implemented","designed",
        "created","engineered","worked","explored",
        "used","integrated","trained","achieved"
    }

    first = text.split()[0].lower()

    if first in verbs:
        return False

    if lower in TECH_WORDS:
        return False
    
    # Skip technologies
    # Skip technology-only lines
    if "," in text :

        # if not any(keyword in lower for keyword in PROJECT_KEYWORDS):
            return False

    # Skip URLs
    if re.search(r"https?://",lower):
        return False

    # Skip dates
    # if re.search(r"\b(19|20)\d{2}\b", text):
    #     return False

    # Skip percentages
    if "%" in text:
        return False

    # Skip sentences
    if text.endswith("."):
        return False

    # Mostly title case
    words = text.split()
    capital_words = sum(1 for w in words if w[:1].isupper())

    if capital_words >= max(2, len(words)//2):
        return True

    # Project numbering
    if re.match(r"^\d+[\).\-\:]\s+", text):
        return True

    # Roman numbering
    if re.match(r"^(I|II|III|IV|V|VI|VII|VIII|IX|X)[\).\-\:]\s+", text, re.IGNORECASE):
        return True

    # Detect using project keywords
    lower = text.lower()

    for keyword in PROJECT_KEYWORDS:
        if keyword in lower:
            return True

    # print("REJECTED:",repr(text))
    return False


def extract_projects(resume_text):
    
    # print("RUNNING EXTRACT project from :",__file__)

    lines = resume_text.split("\n")

    inside = False

    projects = []

    for line in lines:

        text = line.strip()
        text = re.sub(r"\s+github$", "",text, flags=re.I)

        lower = text.lower().rstrip(":").strip()
        
        if lower in PROJECT_HEADERS:
            # print("PROJECT HEADER FOUND:")

            inside = True

            continue

        if inside and any(stop in lower for stop in STOP_HEADERS):

            break

        if not inside:

            continue

        if "|" in text:
            parts = [text.split("|")[0].strip()]
        else:
            parts = [text]

        for part in parts:

            part = part.strip()
            
            if is_project_title(part):

                if part not in projects:
                    projects.append(part)

        # Continue to next line
        # print("LINE:",repr(text))
        if "|" in text or "\t" in text:
            for part in parts:
                part = part.strip()
                if is_project_title(part) and part not in projects:
                    projects.append(part)
            continue

        
        if is_project_title(text):
            
            if text not in projects:

                projects.append(text)
    print("\n========== PROJECTS FOUND ==========")
    for i, p in enumerate(projects, 1):
        print(i, repr(p))
    print("====================================")   

    return projects


def extract_project_count(resume_text):

    projects = extract_projects(resume_text)

    if projects is None:
        print("extract_projects() returned None")
        return 0

    print("Projects:", projects)

    return len(projects)