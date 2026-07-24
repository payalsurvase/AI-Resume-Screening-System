# -----------------------------------
# Resume Score Calculator
# -----------------------------------

# -----------------------------------
# Resume Score Calculator
# -----------------------------------

def calculate_resume_score(
    match_score,
    ats_score,
    project_count,
    years_experience,
    education_level,
    github_activity
):

    # -------------------------
    # Project Score
    # -------------------------
    project_score = min(project_count * 4, 20)

    # -------------------------
    # Experience Score
    # -------------------------
    experience_score = min(years_experience * 3, 15)

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

    # -------------------------
    # Final Score
    # -------------------------
    final_score = (
        ats_score * 0.40 +
        match_score * 0.30 +
        project_score +
        experience_score +
        education_score +
        github_score
    )

    final_score = min(round(final_score, 2), 100)

    return {

        "match_score": round(match_score, 2),

        "skill_score": round(ats_score, 2),

        "project_score": project_score,

        "experience_score": experience_score,

        "education_score": education_score,

        "github_score": github_score,

        "final_score": final_score
    }