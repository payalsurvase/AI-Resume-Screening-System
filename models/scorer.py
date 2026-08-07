# -----------------------------------
# Resume Score Calculator
# -----------------------------------

def calculate_resume_score(
    match_score,
    ats_score,
    project_count,
    experience_months,
    education_level,
    github_activity,
    resume_sections,
    linkedin_activity
):

    # -------------------------
    # Project Score
    # -------------------------
    project_score = min(project_count * 4, 20)

    # -------------------------
    # Experience Score
    # -------------------------
    if experience_months >= 24:
        experience_score = 15

    elif experience_months >= 12:
        experience_score = 12

    elif experience_months >= 6:
        experience_score = 8

    elif experience_months >= 3:
        experience_score = 5

    elif experience_months > 0:
        experience_score = 3

    # Experience section exists but dates couldn't be extracted
    elif resume_sections.get("Experience", False):
        experience_score = 2

    # No experience section at all
    else:
        experience_score = 0

    # -------------------------
    # Education Score
    # -------------------------
    education_scores = {
        "High School": 2,
        "Unknown": 2,
        "Bachelors": 10,
        "Masters": 13,
        "PhD": 15
    }

    education_score = education_scores.get(education_level, 2)

    # -------------------------
    # GitHub Score
    # -------------------------
    github_score = 5 if github_activity else 0
    linkedin_score = 5 if linkedin_activity else 0
    # -------------------------
    # Final Score
    # -------------------------
    final_score = (
        ats_score * 0.40 +
        match_score * 0.30 +
        project_score +
        experience_score +
        education_score +
        github_score +
        linkedin_score
    )

    final_score = min(round(final_score, 2), 100)

    return {

        "match_score": round(match_score, 2),

        "skill_score": round(ats_score, 2),

        "project_score": project_score,

        "experience_score": experience_score,

        "education_score": education_score,

        "github_score": github_score,

        "linkedin_score": linkedin_score,

        "final_score": final_score
    }