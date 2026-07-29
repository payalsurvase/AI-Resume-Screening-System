def calculate_shortlist_status(
    final_score,
    ats_score,
    match_score,
    project_count,
    years_experience,
    github_activity,
    linkedin_activity,
    completeness_score
):

    reasons = []

    # Positive reasons
    if ats_score >= 70:
        reasons.append("✅ Strong ATS score")

    if match_score >= 70:
        reasons.append("✅ Excellent Job Description Match")

    if project_count >= 2:
        reasons.append("✅ Good number of projects")

    if years_experience >= 1:
        reasons.append("✅ Relevant experience")

    if github_activity:
        reasons.append("✅ GitHub profile available")

    if linkedin_activity:
        reasons.append("✅ LinkedIn profile available")

    if completeness_score >= 80:
        reasons.append("✅ Complete resume")

    # Negative reasons
    if ats_score < 40:
        reasons.append("❌ ATS score is too low")

    if match_score < 40:
        reasons.append("❌ Poor JD Match")

    if project_count == 0:
        reasons.append("❌ No projects found")

    if completeness_score < 60:
        reasons.append("❌ Resume is incomplete")

    # Final Status
    if ats_score < 40 or match_score < 40:
        status = "Rejected"
        icon = "❌"

    elif (
        final_score >= 85
        and ats_score >= 70
        and match_score >= 75
        and project_count >= 2
        and completeness_score >= 80
    ):
        status = "Strongly Shortlisted"
        icon = "⭐⭐"

    elif (
        final_score >= 70
        and ats_score >= 60
        and match_score >= 60
    ):
        status = "Shortlisted"
        icon = "✅"

    elif final_score >= 55:
        status = "Needs Manual Review"
        icon = "⚠️"

    else:
        status = "Rejected"
        icon = "❌"

    return status, icon, reasons