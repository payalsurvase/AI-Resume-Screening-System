import re

# ----------------------------
# EMAIL
# ----------------------------

def extract_email(text):

    match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)

    if match:
        return match.group()

    return "Not Found"


# ----------------------------
# PHONE
# ----------------------------

def extract_phone(text):

    match = re.search(r"(\+91[- ]?)?[6-9]\d{9}", text)

    if match:
        return match.group()

    return "Not Found"


# ----------------------------
# LINKEDIN
# ----------------------------

def extract_linkedin(text):

    match = re.search(r"(https?://)?(www\.)?linkedin\.com/in/[A-Za-z0-9_-]+", text, re.I)

    if match:
        return match.group()

    return "Not Found"


# ----------------------------
# GITHUB
# ----------------------------

def extract_github(text):

    match = re.search(r"(https?://)?(www\.)?github\.com/[A-Za-z0-9_-]+", text, re.I)

    if match:
        return match.group()

    return "Not Found"


# ----------------------------
# EXPERIENCE
# ----------------------------

def extract_experience(text):

    matches = re.findall(r'(\d+)\+?\s*(?:years|year|yrs|yr)', text.lower())

    if matches:

        return max(int(x) for x in matches)

    return 0


# ----------------------------
# EDUCATION
# ----------------------------

def extract_education(text):

    t = text.lower()

    if "phd" in t:
        return "PhD"

    if "m.tech" in t or "master" in t or "m.e" in t or "mca" in t:
        return "Masters"

    if "b.tech" in t or "bachelor" in t or "b.e" in t or "bca" in t:
        return "Bachelors"

    return "Unknown"