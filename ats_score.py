import math


def calculate_ats_score(found_skills, required_skills):

    if len(required_skills) == 0:
        return 0

    found = set(skill.lower() for skill in found_skills)
    required = set(skill.lower() for skill in required_skills)

    matched = found.intersection(required)

    score = (len(matched) / len(required)) * 100

    return round(score, 2)