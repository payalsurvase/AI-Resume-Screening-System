import re
from skill_aliases import SKILL_ALIASES

# -----------------------------------
# Clean Resume Text
# -----------------------------------
def clean_text(text):

    # Convert to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # Remove Email IDs
    text = re.sub(r"\S+@\S+", "", text)

    # Remove Phone Numbers
    text = re.sub(r"\+?\d[\d\s-]{8,15}", "", text)

    # Remove Special Characters
    text = re.sub(r"[^a-zA-Z0-9+#\-\s]", " ", text)

    # Remove Extra Spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text

# -----------------------------------
# Find Missing Skills
# -----------------------------------
def get_missing_skills(found_skills, required_skills):

    print("===== REPORT SKILL DEBUG =====")
    print("FOUND SKILLS:", found_skills)
    print("REQUIRED SKILLS:", required_skills)
    print("==============================")
    
    # Normalize found skills
    found = set(skill.lower() for skill in found_skills)

    # Also include aliases of found skills
    for alias, original in SKILL_ALIASES.items():
        if original.lower() in found:
            found.add(alias.lower())

    missing = []

    for skill in required_skills:

        skill_lower = skill.lower()

        if skill_lower in found:
            continue

        # Ignore spaces, dots and hyphens
        normalized_skill = (
            skill_lower.replace("-", "")
                       .replace(".", "")
                       .replace(" ", "")
        )

        matched = False

        for f in found:

            normalized_found = (
                f.replace("-", "")
                 .replace(".", "")
                 .replace(" ", "")
            )

            if normalized_skill == normalized_found:
                matched = True
                break

        if not matched:
            missing.append(skill)

    return sorted(missing)

# -----------------------------------
# Extract Required Skills from JD
# -----------------------------------
def extract_required_skills(job_description, all_skills):

    # Remove heading BEFORE cleaning
    jd = job_description.replace("Skills Required:", "")

    # Split first
    jd_skills = [clean_text(s.strip()) for s in jd.split(",") if s.strip()]

    print("\n===== JD SKILLS =====")
    print(jd_skills)

    required = set()

    # Match original skills
    for skill in all_skills:

        if clean_text(skill) in jd_skills:
            required.add(skill)

    # Match aliases
    for alias, original in SKILL_ALIASES.items():

        if clean_text(alias) in jd_skills:
            required.add(original)

    return sorted(required)