# -----------------------------------
# Resume Improvement Suggestions
# -----------------------------------

def generate_resume_suggestions(

    found_skills,
    required_skills,
    project_count,
    experience_months,
    education_level,
    github_activity,
    linkedin_activity,
    resume_sections

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

    if experience_months <= 0 and not resume_sections.get("Experience",False):

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

    if not linkedin_activity:
        suggestions.append("Add your LinkedIn profile.")

    if not github_activity:
        suggestions.append("Add your GitHub profile.")

    return suggestions