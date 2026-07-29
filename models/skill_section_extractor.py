import re

def extract_skill_section(text):

    text = text.replace("\r", "")

    patterns = [

        r"skills(.*?)(projects|experience|education|certifications|achievements|languages|$)",

        r"technical skills(.*?)(projects|experience|education|certifications|achievements|$)",

        r"core competencies(.*?)(projects|experience|education|certifications|achievements|$)",

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE | re.DOTALL
        )

        if match:

            return match.group(1)

    return ""