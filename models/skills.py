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

        elif re.match(r"^Technical Skills\s*:", line, flags=re.I):
            continue

        line = line.replace("&",",")
        line = line.replace("!",",")
        line = line.replace(";",",")

        # Split by comma only
        parts = [p.strip() for p in line.split(",")]
        for i in range(len(parts)):
            if parts[i].lower() == "supervised":
                parts[i] = "Supervised Learning"

        for part in parts:
            if part:
                 tokens.append(part)

    return tokens


def get_skill_section(text):

    text_lower = text.lower()

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
        "achievements"
        
    ]

    start = -1

    for heading in headings:

        match = re.search(
            r'^\s*' + re.escape(heading) + r'\s*$',
            text_lower,
            flags=re.IGNORECASE | re.MULTILINE
        )

        if match:
            start = match.start()
            break

    if start == -1:
        return text

    end = len(text)

    for heading in end_headings:

        match = re.search(
            r'^\s*' + re.escape(heading) + r'\s*$',
            text_lower[start + 10:],
            flags=re.IGNORECASE | re.MULTILINE
        )

        if match:
            pos = start + 10 + match.start()

            if pos < end:
                end = pos

    return text[start:end]

# -----------------------------
# Extract Skills
# -----------------------------

def extract_skills(text, all_skills):

    skill_text = get_skill_section(text)

    print("======RAW SKILL TEXT======")
    print(skill_text)
    print("=========================")
    
    tokens = extract_skill_tokens(skill_text)
    
    # print("\n===== TOKENS =====")
    # for t in tokens:
    #     print(repr(t))

    # print(tokens)
    # print([normalize_text(t) for t in tokens])

    found_skills = set()

    normalized_tokens = [normalize_text(token) for token in tokens]

    normalized_token_set = set(normalized_tokens)

    for skill in all_skills:

        normalized_skill = normalize_text(skill)

        if normalized_skill in normalized_token_set:
            # if skill.lower()=="tsql":
            #     print("TSQL added from token matching")
            found_skills.add(skill)
        # Alias Matching
        for alias, original in SKILL_ALIASES.items():

            normalized_alias = normalize_text(alias)

            if normalized_alias in normalized_token_set:
                found_skills.add(original)

        normalized_text = normalize_text(skill_text)

        for skill in all_skills:

            normalized_skill = normalize_text(skill)

            if len(normalized_skill) <= 2:

                # Skip single-letter programming languages
                if normalized_skill in ["c", "r"]:
                    continue

                pattern = r"\b" + re.escape(normalized_skill) + r"\b"

                if re.search(pattern, normalized_text):
                    
                    found_skills.add(skill)

            else:
                # Prevent SQL matching inside T-SQL / PL-SQL
                if normalized_skill in ["sql", "t-sql", "pl/sql"]:
                    pattern = r"\b" + re.escape(normalized_skill) + r"\b"

                    if re.search(pattern, normalized_text):
                        found_skills.add(skill)

                else:
                    pattern = r"\b" + re.escape(normalized_skill) + r"\b"
                    if re.search(pattern, normalized_text):
                            found_skills.add(skill)
                    # if normalized_skill in normalized_text:
                    #     found_skills.add(skill)

        for alias, original in SKILL_ALIASES.items():

            normalized_alias = normalize_text(alias)

            if len(normalized_alias) <= 2:
                pattern = r"\b" + re.escape(normalized_alias) + r"\b"

                if re.search(pattern, normalized_text):
                    found_skills.add(original)

            else:
                pattern = r"\b" + re.escape(normalized_alias) + r"\b"
                if re.search(pattern, normalized_text):
                    found_skills.add(original)

    # print("\n ===== FINAL FOUND SKILLS=====")
    # print(sorted(found_skills))

    cleaned = {}

    for skill in found_skills:

        key = skill.lower()

        # Remove T-SQL
        if key == "t-sql":
             continue

        # Merge duplicate display names
        if key in ["html5", "html"]:
            cleaned["html"] = "HTML"

        elif key in ["css3", "css"]:
                cleaned["css"] = "CSS"

        elif key in ["react.js", "react"]:
                cleaned["react"] = "React"

        else:
                cleaned[key] = skill

    return sorted(cleaned.values())