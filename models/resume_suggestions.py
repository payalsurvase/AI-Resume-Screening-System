# -----------------------------------
# Resume Improvement Suggestions
# -----------------------------------

def generate_resume_suggestions(

    found_skills,
    required_skills,
    project_count,
    years_experience,
    education_level,
    github_activity

):

    suggestions = []

    # -------------------------
    # Missing Skills
    # -------------------------

    found = set(skill.lower() for skill in found_skills)

    for skill in required_skills:

        if skill.lower() not in found:

            suggestions.append(f"Add skill: {skill}")

    # -------------------------
    # Projects
    # -------------------------

    if project_count < 2:

        suggestions.append(
            "Add more real-world projects."
        )

    # -------------------------
    # Experience
    # -------------------------

    if years_experience == 0:

        suggestions.append(
            "Add internship or work experience."
        )

    # -------------------------
    # Education
    # -------------------------

    if education_level == "Unknown":

        suggestions.append(
            "Mention your education details clearly."
        )

    # -------------------------
    # GitHub
    # -------------------------

    if github_activity == 0:

        suggestions.append(
            "Add your GitHub profile."
        )

    return suggestions