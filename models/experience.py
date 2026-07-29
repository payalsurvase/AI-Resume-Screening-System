import re
from datetime import datetime

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

    date_pattern = re.compile(
        r'((?:\d{1,2}\s+)?(?:jan|january|feb|february|mar|march|apr|april|may|jun|june|jul|july|aug|august|sep|sept|september|oct|october|nov|november|dec|december)\s+\d{4}|\d{1,2}/\d{4}|\d{4}|present|current)\s*(?:-|–|—|to)\s*((?:\d{1,2}\s+)?(?:jan|january|feb|february|mar|march|apr|april|may|jun|june|jul|july|aug|august|sep|sept|september|oct|october|nov|november|dec|december)\s+\d{4}|\d{1,2}/\d{4}|\d{4}|present|current)',
        re.IGNORECASE
    )

    intervals = []

    for start_text, end_text in date_pattern.findall(text):

        start = parse_date(start_text)

        end = parse_date(end_text)

        if start is not None and end is not None and end >= start:
            intervals.append((start, end))

    merged = merge_intervals(intervals)

    total_months = sum(end - start for start, end in merged)

    years = total_months // 12

    months = total_months % 12

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
        "experience",
        "work experience",
        "employment",
        "internships"
    ]

    end_headings = [
        "projects",
        "skills",
        "education",
        "certifications",
        "achievements",
        "languages"
    ]

    start = -1

    for heading in headings:
        pos = text.find(heading)
        if pos != -1:
            start = pos
            break

    if start == -1:
        return text

    end = len(text)

    for heading in end_headings:
        pos = text.find(heading, start + 20)

        if pos != -1 and pos < end:
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

        m = re.match(pattern, date_str)

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