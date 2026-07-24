import re

def extract_linkedin(resume_text):

    pattern = r"(https?://)?(www\.)?linkedin\.com/in/[A-Za-z0-9_-]+"

    if re.search(pattern, resume_text, re.IGNORECASE):
        return 1

    return 0