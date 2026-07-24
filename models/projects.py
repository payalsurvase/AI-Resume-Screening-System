import re

PROJECT_HEADERS = [
    "projects",
    "project",
    "academic projects",
    "personal projects",
    "key projects"
]

STOP_HEADERS = [
    "education",
    "experience",
    "skills",
    "technical skills",
    "certifications",
    "achievements",
    "languages",
    "hobbies",
    "interests",
    "profile",
    "summary"
]


def extract_projects(resume_text):

    lines = resume_text.split("\n")

    inside = False

    projects = []

    for line in lines:

        text = line.strip()

        lower = text.lower()

        if lower in PROJECT_HEADERS:
            inside = True
            continue

        if inside and lower in STOP_HEADERS:
            break

        if not inside:
            continue

        if len(text) < 4:
            continue

        if len(text) > 70:
            continue

        if text.endswith("."):
            continue

        if re.search(r"\d{4}", text):
            continue

        if text not in projects:
            projects.append(text)

    return projects


def extract_project_count(resume_text):

    return len(extract_projects(resume_text))