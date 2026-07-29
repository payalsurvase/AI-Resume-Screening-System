import re
from models.project_keywords import PROJECT_KEYWORDS
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
    "languages",
    "hobbies",
    "interests",
    "summary",
    "profile",
    "contact"
]


def is_project_title(line):

    text = line.strip()

    if len(text) < 3:
        return False

    if len(text) > 80:
        return False

    lower = text.lower()

    # Skip descriptions
    if text.startswith(("•", "-", "*")):
        return False

    # Skip technologies
    # Skip technology-only lines
    if "," in text:

        words = text.split()

        # If line contains a project keyword, keep it
        if not any(keyword in lower for keyword in PROJECT_KEYWORDS):
            return False

    # Skip URLs
    if "http" in lower or "github" in lower:
        return False

    # Skip dates
    if re.search(r"\b(19|20)\d{2}\b", text):
        return False

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
        
    return False


def extract_projects(resume_text):

    lines = resume_text.split("\n")

    inside = False

    projects = []

    for line in lines:

        text = line.strip()

        lower = text.lower().rstrip(":").strip()

        if lower in PROJECT_HEADERS:

            inside = True

            continue

        if inside and lower in STOP_HEADERS:

            break

        if not inside:

            continue

        # Split table columns
        parts = re.split(r"\||\t| {2,}", text)

        for part in parts:

            part = part.strip()

            if is_project_title(part):

                if part not in projects:
                    projects.append(part)

        # Continue to next line
        if "|" in text or "\t" in text:
            continue

        if is_project_title(text):

            if text not in projects:

                projects.append(text)

    return projects


def extract_project_count(resume_text):

    return len(extract_projects(resume_text))