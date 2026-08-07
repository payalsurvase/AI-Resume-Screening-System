import pandas as pd
import re
import string
import streamlit as st

from skill_aliases import SKILL_ALIASES
from models.section_parser import extract_sections,clean_sections
# -----------------------------
# Load Skills from CSV
# -----------------------------
def load_skills():

    skills = []

    with open("data/skills.csv", "r", encoding="utf-8") as file:

        for line in file:

            line = line.strip()

            # Skip empty lines and comments
            if line == "" or line.startswith("#"):
                continue

            skills.append(line)

    return skills


def normalize_text(text):

    text = text.lower()

    text = text.replace("-", " ")
    text = text.replace("/", " ")

    # Keep important programming symbols
    allowed = "+#."

    remove = "".join(ch for ch in string.punctuation if ch not in allowed)

    text = text.translate(
        str.maketrans("", "", remove)
    )

    text = re.sub(r"\s+", " ", text)

    return text.strip()

def extract_skill_tokens(skill_text):
    
    tokens = []
    print(skill_text)
    lines = skill_text.split("\n")

    for i , line  in enumerate(lines):
        print(i,repr(line))
            

    # Join "Frameworks &" + "Tools: ..."
    i = 0
    while i < len(lines) - 1:
        if lines[i].strip().endswith("&"):
                lines[i] = lines[i].strip() + " " + lines[i + 1].strip()
                del lines[i + 1]
        else:
            i += 1

    for line in lines:

        
        line = line.strip()
        line = re.sub(r"^[•▪●■►]+\s*", "", line)

        if not line:
            continue

        # Remove section labels
        if re.match(r"^Machine Learning\s*:", line, flags=re.I):
            line = line.replace("Machine Learning:", "Machine Learning,", 1)

        elif re.match(r"^Languages\s*:", line, flags=re.I):
            line = line.replace("Languages:", "", 1)

        elif re.match(r"^Backend\s*:", line, flags=re.I):
            line = line.replace("Backend:", "", 1)

        elif re.match(r"^Frontend\s*:", line, flags=re.I):
            line = line.replace("Frontend:", "", 1)

        elif re.match(r"^Databases\s*:", line, flags=re.I):
            line = line.replace("Databases:", "", 1)

        elif re.match(r"^Frameworks\s*&\s*Tools\s*:", line, flags=re.I):
            line = line.replace("Frameworks & Tools:", "", 1)

        elif re.match(r"^Libraries\s*&\s*Databases\s*:", line, flags=re.I):
            line = line.replace("Libraries & Databases:", "", 1)

        elif re.match(r"^AI/ML\s*:", line, flags=re.I):
            line = line.replace("AI/ML:", "", 1)

        elif re.match(r"^Frameworks\s*:", line, flags=re.I):
            line = line.replace("Frameworks:", "", 1)

        elif re.match(r"^Libraries\s*:", line, flags=re.I):
            line = line.replace("Libraries:", "", 1)

        elif re.match(r"^Tools\s*:", line, flags=re.I):
            line = line.replace("Tools:", "", 1)

        elif re.match(r"^Soft Skills\s*:", line, flags=re.I):
            line = line.replace("Soft Skills:", "", 1)

        elif re.match(r"^Technical Skills\s*:?\s*$", line, flags=re.I):
            continue

        line = line.replace("&",",")
        line = line.replace("!",",")
        line = line.replace(";",",")

        parts = []

        # Resume uses one skill per line
        if "," not in line:
            parts = [line.strip()]

        else:
            for p in line.split(","):
                p = p.strip()
                if p:
                    parts.append(p)

        for i in range(len(parts)):
            if parts[i].lower() == "supervised":
                parts[i] = "Supervised Learning"

        HEADINGS = {
            "technical skills",
            "languages",
            "frontend",
            "backend & apis",
            "backend",
            "apis",
            "databases",
            "data science",
            "tools",
            "cs core",
            "certs"
        }

        parts = [p for p in parts if p.lower() not in HEADINGS]

        for part in parts:
            if part:
                 tokens.append(part)

        # print("\n===== TOKENS =====")
        # for t in tokens:
        #     print(repr(t))
            
    return tokens


def get_skill_section(text):

    lines = text.split("\n")

    headings = [
        "technical skills",
        "skills summary",
        "skills",
        "technical expertise",
        "technology stack",
        "core competencies"
    ]

    end_headings = [
        "experience",
        "professional experience",
        "internship experience",
        "projects",
        "education",
        "certifications",
        "achievements",
        "summary"
    ]

    start = None
    end = len(lines)

    # Find skill section start
    for i, line in enumerate(lines):

        if line.strip().lower() in headings:
            start = i + 1
            break

    if start is None:
        return text

    # Find next section
    for i in range(start, len(lines)):

        if lines[i].strip().lower() in end_headings:
            end = i
            break

    section = "\n".join(lines[start:end])

    print("======= SKILL SECTION =======")
    print(section)
    print("=============================")

    return section

# -----------------------------
# Extract Skills
# -----------------------------

def extract_skills(text, all_skills):

    skill_text = get_skill_section(text)

    print("======RAW SKILL TEXT======")
    print(skill_text)
    print("=========================")

    tokens = extract_skill_tokens(skill_text)

    found_skills = set()

    normalized_tokens = [normalize_text(token) for token in tokens]
    normalized_token_set = set(normalized_tokens)

    # ----------------------------
    # Exact Token Matching
    # ----------------------------
    for skill in all_skills:

        normalized_skill = normalize_text(skill)

        if normalized_skill in normalized_token_set:
            found_skills.add(skill)

    # ----------------------------
    # Alias Matching
    # ----------------------------
    for alias, original in SKILL_ALIASES.items():

        normalized_alias = normalize_text(alias)

        if normalized_alias in normalized_token_set:
            found_skills.add(original)

    # ----------------------------
    # Backup Text Search
    # ----------------------------
    normalized_text = normalize_text(skill_text)

    for skill in all_skills:

        normalized_skill = normalize_text(skill)

        if len(normalized_skill) <= 2:

            if normalized_skill in ["c", "r"]:
                continue

            pattern = r"\b" + re.escape(normalized_skill) + r"\b"

            if re.search(pattern, normalized_text):
                found_skills.add(skill)

        else:

            pattern = r"\b" + re.escape(normalized_skill) + r"\b"

            if re.search(pattern, normalized_text):
                found_skills.add(skill)

    # ----------------------------
    # Alias Backup Search
    # ----------------------------
    for alias, original in SKILL_ALIASES.items():

        normalized_alias = normalize_text(alias)

        pattern = r"\b" + re.escape(normalized_alias) + r"\b"

        if re.search(pattern, normalized_text):
            found_skills.add(original)

    # ----------------------------
    # Cleaning Duplicate Skills
    # ----------------------------
    cleaned = {}

    for skill in found_skills:

        key = skill.lower()

        if key == "t-sql":
            continue

        if key in ["html", "html5"]:
            cleaned["html"] = "HTML"

        elif key in ["css", "css3"]:
            cleaned["css"] = "CSS"

        elif key in ["react", "react.js"]:
            cleaned["react"] = "React"

        else:
            cleaned[key] = skill

    return sorted(cleaned.values())