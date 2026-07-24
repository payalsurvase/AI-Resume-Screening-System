def extract_education(resume_text):

    text = resume_text.lower()

    if "phd" in text or "doctorate" in text:
        return "PhD"

    elif "master" in text or "m.tech" in text or "m.e" in text or "mca" in text:
        return "Masters"

    elif (
            "bachelor" in text
            or "b.tech" in text
            or "btech" in text
            or "b.e" in text
            or "be " in text
            or "bachelor of engineering" in text
            or "bachelor of technology" in text
            or "bca" in text
        ):
        return "Bachelors"

    else:
        return "High School"