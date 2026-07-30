import re
from datetime import datetime,date

MONTHS = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5,
    "jun": 6, "june": 6,
    "jul": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12
}


def merge_intervals(intervals):
    if not intervals:
        return []

    intervals.sort()

    merged = [intervals[0]]

    for current in intervals[1:]:

        last = merged[-1]

        if current[0] <= last[1]:
            merged[-1] = (last[0], max(last[1], current[1]))
        else:
            merged.append(current)

    return merged

def extract_experience(resume_text):

    text = get_experience_section(resume_text)

    print("START SECTION")
    print(text[:300])
    # print("==============================")

    date_pattern = re.compile(
    r'('
    r'(?:\d{1,2}\s+)?'
    r'(?:jan|january|feb|february|mar|march|apr|april|may|jun|june|jul|july|aug|august|sep|sept|september|oct|october|nov|november|dec|december)'
    r'\s+\d{4}'
    r'|\d{1,2}/\d{4}'
    r'|\d{4}'
    r'|present'
    r'|current'
    r')'
    r'\s*(?:-|–|—|to)\s*'
    r'('
    r'(?:\d{1,2}\s+)?'
    r'(?:jan|january|feb|february|mar|march|apr|april|may|jun|june|jul|july|aug|august|sep|sept|september|oct|october|nov|november|dec|december)'
    r'\s+\d{4}'
    r'|\d{1,2}/\d{4}'
    r'|\d{4}'
    r'|present'
    r'|current'
    r')',
    re.IGNORECASE
)

    intervals = []
    print("===== EXPERIENCE TEXT =====")
    print(repr(text))
    print("===========================")

    print("===== DATE MATCHES =====")
    print(date_pattern.findall(text))

    for start_text, end_text in date_pattern.findall(text):

        window = text.lower()

        education_keywords = [
            "education",
            "b.e",
            "btech",
            "b.tech",
            "computer engineering",
            "degree",
            "university",
            "college"
        ]

        # Check if this date range belongs to Education
        date_string = f"{start_text} {end_text}"

        date_pos = window.find(start_text.lower())

        if date_pos != -1:
            context = window[max(0, date_pos - 100): date_pos + 100]

            if any(keyword in context for keyword in education_keywords):
                continue

        print("DATE FOUND:", start_text, "------>", end_text)

        start = parse_date(start_text)

        end = parse_date(end_text)

        # print("PARSED:", start, "------>", end)

        if start is not None and end is not None and end >= start:
            intervals.append((start, end))

    # merged = merge_intervals(intervals)

    total_months = 0

    for start, end in intervals:

        months = end - start

        # If internship starts and ends in the same month,
        # count it as 1 month instead of 0.
        if months == 0:
            months = 1

        total_months += months

    years = total_months // 12

    months = total_months % 12

    print("Intervals:", intervals)
    # print("Merged:", merged)
    print("Total Months:", total_months)
    print("Years:", years)
    print("Months:", months)

    return {
        "years": years,
        "months": months,
        "total_months": total_months,
        "experience": f"{years} Years {months} Months"
    }

   


def get_experience_section(text):

    text = text.lower()

    headings = [
    "professional experience",
    "work experience",
    "employment",
    "employment history",
    "experience",
    "internship",
    "internships"
]

    end_headings = [
    "projects",
    "technical skills",
    "skills",
    "education",
    "certifications",
    "achievements",
    "languages",
    "publications",
    "hobbies",
    "interests"
]
    start = -1

    for heading in headings:

        match = re.search(
            r'^\s*' + re.escape(heading) + r'\s*$',
            text,
            flags=re.IGNORECASE | re.MULTILINE
        )

        if match:
            start = match.start()
            break

    
    if start == -1:
        return text

    end = len(text)

    for heading in end_headings:

        match = re.search(
            r"\b" + re.escape(heading) + r"\b",
            text[start + 20:]
        )

        if not match:
            continue

        pos = start + 20 + match.start()

        if pos < end:
            end = pos

    return text[start:end]

import calendar

def parse_date(date_str):

    date_str = date_str.lower().strip()

    current = datetime.now()

    if "present" in date_str or "current" in date_str:
        return current.year * 12 + current.month

    patterns = [

        r'(\d{1,2})\s+([a-zA-Z]+)\s+(\d{4})',

        r'([a-zA-Z]+)\s+(\d{4})',

        r'(\d{1,2})/(\d{4})',

        r'(\d{4})'

    ]

    for pattern in patterns:

        m = re.fullmatch(pattern, date_str)

        if not m:
            continue

        if pattern == patterns[0]:

            day, month, year = m.groups()

            month = MONTHS[month[:3]]

            return int(year) * 12 + month

        elif pattern == patterns[1]:

            month, year = m.groups()

            month = MONTHS[month[:3]]

            return int(year) * 12 + month

        elif pattern == patterns[2]:

            month, year = m.groups()

            return int(year) * 12 + int(month)

        elif pattern == patterns[3]:

            year = int(m.group(1))

            return year * 12 + 1

    return None