import re

def extract_github(resume_text):

    pattern = r"(https?://)?(www\.)?github\.com/[A-Za-z0-9_-]+"

    if re.search(pattern, resume_text, re.IGNORECASE):
        return 1

    return 0