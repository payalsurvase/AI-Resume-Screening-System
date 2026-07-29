import re

SECTION_HEADERS = {

    "profile":[
        "profile","summary","professional summary","career summary",
        "executive summary","about","about me","career objective",
        "objective","professional profile","introduction"
    ],

    "experience":[
        "experience","work experience","professional experience",
        "employment","employment history","career history",
        "work history","internship","internships",
        "industrial training","training","professional background"
    ],

    "education":[
        "education","academic","academic details",
        "academic background","qualification",
        "qualifications","education details",
        "educational qualification","academics"
    ],

    "projects":[
        "projects","project","academic projects",
        "personal projects","major projects",
        "minor projects","key projects",
        "live projects","industrial projects",
        "project experience"
    ],

    "skills":[
        "skills",
        "technical skills",
        "technical skill",
        "technical expertise",
        "technical proficiency",
        "technical competencies",
        "professional skills",
        "core skills",
        "core competencies",
        "key skills",
        "competencies",
        "expertise",
        "technology",
        "technologies",
        "tech stack",
        "tools",
        "software skills",
        "programming languages"
    ],

    "certifications":[
        "certifications",
        "certificates",
        "licenses",
        "courses",
        "professional certifications",
        "training certifications"
    ],

    "achievements":[
        "achievements",
        "awards",
        "honors",
        "accomplishments",
        "recognition"
    ],

    "languages":[
        "languages",
        "language proficiency"
    ],

    "hobbies":[
        "hobbies",
        "interests",
        "extra curricular activities",
        "extracurricular activities"
    ],

    "contact":[
        "contact",
        "contact information",
        "personal details",
        "personal information"
    ],

    "soft_skills":[
        "soft skills",
        "personal skills",
        "interpersonal skills",
        "professional skills",
        "behavioral skills"
    ]
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
        print("LINE:",repr(line))

        # Remove decorative symbols
        lower = lower.replace("|", " ")
        lower = lower.replace("•", " ")
        lower = lower.replace("*", " ")
        lower = re.sub(r"\s+"," ",lower)

        # Remove trailing : or -
        lower = re.sub(r"[:|\-]+$", "", lower).strip()

        # Detect merged section headings inside a line
        for section, headers in SECTION_HEADERS.items():

            for header in headers:

                pattern = r"\b" + re.escape(header) + r"\b"

                if re.search(pattern, lower):

                    idx = lower.find(header)

                    # If heading is not at beginning, split the line
                    if idx > 0:

                        before = line[:idx].strip()

                        after = line[idx:].strip()

                        if before:
                            sections[current_section].append(before)

                        line = after
                        lower = line.lower().strip()

                    break

        matched = False

        for section, headers in SECTION_HEADERS.items():

            for header in headers:
                if "technical" in lower:
                    print("FOUND LINE :",repr(lower))

                if re.fullmatch(rf"{re.escape(header)}[:\s]*",lower):

                    current_section = section

                    if current_section not in sections:
                        sections[current_section] = []

                    matched = True
                    break

            if matched:
                break

        if not matched:

            # Stop skills section if another section starts
            if current_section == "skills":

                stop_headers = [
                    "projects",
                    "experience",
                    "internship",
                    "education",
                    "certifications",
                    "achievements",
                    "extra curricular",
                    "extracurricular",
                    "hobbies"
                ]

                lower_line = line.lower()

                if lower_line.strip() in stop_headers:
                    current_section = "other"

                sections[current_section].append(line)
                
    print("\n========== PARSED SECTIONS ==========")

    for sec, content in sections.items():
        print("\nSECTION:", sec)
        print("--------------------------------")
        for x in content:
            print(x)
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