import re
from datetime import datetime

def extract_experience(resume_text):

    text = resume_text.lower()

    # -----------------------------
    # Method 1 : Direct years
    # Example : 2 years, 3+ yrs
    # -----------------------------

    matches = re.findall(
        r'(\d+)\+?\s*(?:years|year|yrs|yr)',
        text
    )

    if matches:
        return max(int(x) for x in matches)

    # -----------------------------
    # Method 2 : Date ranges
    # Example :
    # Sept 2023 - Oct 2024
    # Jan 2022 - Present
    # Aug 2023 - Currently
    # -----------------------------

    year_matches = re.findall(
        r'(\d{4}).*?(?:-|to).*?(present|currently|\d{4})',
        text
    )

    if year_matches:

        total = 0

        current_year = datetime.now().year

        for start, end in year_matches:

            start = int(start)

            if end in ["present", "currently"]:
                end = current_year
            else:
                end = int(end)

            if end >= start:
                total += end - start

        return total

    return 0