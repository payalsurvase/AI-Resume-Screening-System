import re

SECTION_HEADERS = {

    "profile":[
        "profile",
        "summary",
        "professional summary",
        "career summary",
        "objective",
        "career objective",
        "about me"
    ],

    "experience":[
        "experience",
        "work experience",
        "professional experience",
        "employment",
        "employment history",
        "internship",
        "internships"
    ],

    "education":[
        "education",
        "academic",
        "academic details",
        "qualification",
        "qualifications",
        "education details"
    ],

    "projects":[
        "projects",
        "project",
        "academic projects",
        "personal projects",
        "major projects",
        "minor projects",
        "key projects"
    ],

    "skills":[
        "skills",
        "technical skills",
        "technical skill",
        "core skills",
        "professional skills",
        "key skills",
        "competencies"
    ],

    "certifications":[
        "certifications",
        "certificates",
        "licenses",
        "courses"
    ],

    "achievements":[
        "achievements",
        "awards",
        "accomplishments"
    ],

    "languages":[
        "languages"
    ],

    "hobbies":[
        "hobbies",
        "interests"
    ],

    "contact":[
        "contact"
    ],

    "soft_skills":[
        "personal skills",
        "soft skiils",
        "professional skills"
     ],

 }


def extract_sections(resume_text):

    sections = {}

    current_section = "other"

    sections[current_section] = []

    lines = resume_text.split("\n")

    for line in lines:

        line = line.strip()
        # Skip email
        if "@" in line:
            continue

        # Skip LinkedIn
        if "linkedin.com" in line.lower():
            continue

        # Skip phone number
        if re.fullmatch(r"[\+\d\s\-]{10,15}", line):
            continue

        if re.fullmatch(r"[-=*|_ ]+",line):
            continue

        if line == "":
            continue

        lower = line.lower().strip()
        lower = re.sub(r"[:|\-]+$", "",lower).strip()

        matched = False

        for section, headers in SECTION_HEADERS.items():

            for header in headers:

                if lower == header or lower.startswith(header):

                    current_section = section

                    if current_section not in sections:
                        sections[current_section] = []

                    matched = True
                    break

            if matched:
                break

        if not matched:

            sections[current_section].append(line)

    return sections


def clean_sections(sections):

    remove_words = [
        "linkedin.com",
        "@",
        "government college",
        "gov.college",
        "gov. college",
        "research lab",
        "maharashtra",
        "india"
    ]

    cleaned = {}

    for section, lines in sections.items():

        cleaned[section] = []

        for line in lines:

            text = line.lower()

            if any(word in text for word in remove_words):
                continue

            if len(line.strip()) <= 1:
                continue

            cleaned[section].append(line)

    return cleaned