import pandas as pd
import re
import string

from skill_aliases import SKILL_ALIASES

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

    text = text.replace("_", " ")

    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )

    text = re.sub(r"\s+", " ", text)

    return text

# -----------------------------
# Extract Skills
# -----------------------------

def extract_skills(text, all_skills):

    text = normalize_text(text)

    found_skills = set()

    # Detect all original skills
    for skill in all_skills:

        normalized_skill = normalize_text(skill)
        pattern = r"\b" + re.escape(normalized_skill) + r"\b"

        if re.search(pattern, text):
            found_skills.add(skill)

    # Detect aliases
    for alias, original in SKILL_ALIASES.items():

        normalized_alias = normalize_text(alias)
        pattern = r"\b" + re.escape(normalized_alias) + r"\b"

        if re.search(pattern, text):
            found_skills.add(original)

    return sorted(list(found_skills))