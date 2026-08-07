import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

from ats_score import calculate_ats_score
from job_descriptions import JOB_DESCRIPTIONS
from models.resume_parser import parse_resume
from models.skills import extract_skills, load_skills
from models.matcher import calculate_match_score
from models.scorer import calculate_resume_score
from models.utils import extract_required_skills, get_missing_skills
from models.resume_completeness import calculate_resume_completeness
from models.resume_sections import detect_resume_sections
from models.experience import extract_experience
from models.education import extract_education
from models.github import extract_github
from models.projects import extract_project_count,extract_projects
from models.linkedin import extract_linkedin
from models.section_parser import extract_sections,clean_sections
from models.nlp_parser import parse_resume_nlp
from models.resume_suggestions import generate_resume_suggestions
from io import BytesIO
from models.shortlist import calculate_shortlist_status
from pdf_report import generate_pdf_report
model = joblib.load("models/resume_shortlist_model.pkl")

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="📄",
    layout="wide"
)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("📋 Menu")

menu = st.sidebar.radio(
    "Select Option",
    [
        "Student Mode",
        "Recruiter Mode",
        "About Project"
    ]
)

# -----------------------------
# About Page
# -----------------------------
if menu == "About Project":

    st.title("📄 AI Resume Screening System")

    st.write("""
This project helps recruiters and students analyze resumes.

### Features
- Resume Upload
- AI Resume Parsing
- Resume & Job Description Matching
- ATS Score
- Missing Skills Detection
- Resume Suggestions
- Dashboard Visualization
- Report Download
    """)

# -----------------------------
# Main Dashboard
# -----------------------------
elif menu == "Student Mode":

    st.title("📄 AI Resume Screening System")

    st.markdown("### Upload Resume and Compare with Job Description")

    st.divider()

    # Resume Upload

    uploaded_resume = st.file_uploader(
        "📂 Upload Resume",
        type=["pdf", "docx"],
    )

    st.divider()

    # Job Description

    st.subheader("💼 Select Job Domain")

    selected_domain = st.selectbox(
        "Choose a Job Role",
        list(JOB_DESCRIPTIONS.keys())
    )

    job_description = JOB_DESCRIPTIONS[selected_domain]

    st.text_area(
        "📋 Job Description",
        value=job_description,
        height=220,
        disabled=True
    )

    
    # Analyze Button

    analyze = st.button(
        "🚀 Analyze Resume",
        use_container_width=True
    )


    # ------------------------------------------
    # Dashboard Result
    # ------------------------------------------

    if analyze:

        

        if uploaded_resume is None:
            st.warning("Please upload a resume.")
            st.stop()

        if job_description.strip() == "":
            st.warning("Please enter Job Description.")
            st.stop()

        # -----------------------------
        # Parse Resume
        # -----------------------------

        # st.write(uploaded_resume)
        # st.write(type(uploaded_resume))

        candidate = parse_resume(uploaded_resume)
        resume_text = candidate["text"]
        # st.write("resume length:",len(resume_text))
        # st.write(repr(resume_text[-1000]))
        # st.text(resume_text)
        sections = extract_sections(candidate["text"])
        sections = clean_sections(sections)

        skills_text = ""

        if "skills" in sections and sections["skills"]:
            skills_text = "\n".join(sections["skills"])

        else:
            skills_text = resume_text

        resume_sections = detect_resume_sections(resume_text) 
        # st.write(resume_sections)
        completeness_score = calculate_resume_completeness(resume_text)

        candidate_name = candidate["name"]

        email = candidate["email"]

        phone = candidate["phone"]


        # -----------------------------
        # Extract Skills
        # -----------------------------

        all_skills = load_skills()

        resume_skills = extract_skills(
            skills_text,
            all_skills
            )

        normalized_resume_skills = []

        for skill in resume_skills:
            s = skill.lower().strip()

            if s in ["llm", "llms"]:
                normalized_resume_skills.append("Large Language Models")

            else:
                normalized_resume_skills.append(skill)

        resume_skills = list(set(normalized_resume_skills))

        # Remove unwanted skills
        UNWANTED_SKILLS = {
            "Artificial Intelligence",
            "HTTPS",
            "HTTP",
            "Stack"
        }

        resume_skills = [
            skill for skill in resume_skills
            if skill not in UNWANTED_SKILLS
        ]


        required_skills = extract_required_skills(
            job_description,
            all_skills
        )
        
        missing_skills = get_missing_skills(
            resume_skills,
            required_skills
        )

        matched_skills = sorted(
              list(set(resume_skills).intersection(set(required_skills)))
        )


        recommended_courses = []

        for skill in missing_skills:
            recommended_courses.append(
                    f"Learn {skill} using Coursera , Udemy or YouTube"
            )


        # -----------------------------
        # AI Match Score
        # -----------------------------
        
        ats_score = calculate_ats_score(
              resume_skills,
              required_skills
        )
        match_score = calculate_match_score(
            resume_text,
            job_description
        )

        
        # -----------------------------
        # AI Resume Shortlist Prediction
        # -----------------------------

        experience = extract_experience(resume_text)
        experience_months = experience["total_months"]
        experience_text = experience["experience"] 

        # st.write("Experience:",experience_months)   
               # Change later if you extract experience automatically
        education_level = extract_education(resume_text) 
        # Change later if you extract education automatically
        # st.subheader("Resume Text Debug")
        # st.text(resume_text[:3000])

        project_count = extract_project_count(resume_text)
        projects = extract_projects(resume_text)
        if projects is None:
            projects = []
        project_count = len(projects)
        # st.write("projects:",projects)
        # st.write("project count:",project_count)
        resume_length = len(resume_text)
        github_activity = extract_github(resume_text)           # Change later if GitHub link is found
        linkedin_activity = extract_linkedin(resume_text)
        
        st.subheader("📊 Resume Summary")

        col1, col2 = st.columns(2)

        with col1:

            st.metric("👤 Candidate", candidate_name)

            st.metric("🎓 Education", education_level)

            st.metric("👨‍💼 Experience", experience_text)

            st.metric("📂 Projects", project_count)

        with col2:

            st.metric("📧 Email", email)

            st.metric("📱 Phone", phone)

            st.metric("💻 GitHub", "Yes ✅" if github_activity else "No ❌")

            st.metric("🔗 LinkedIn", "Yes ✅" if linkedin_activity else "No ❌")

        education_map = {
            "High School": 0,
            "Bachelors": 1,
            "Masters": 2,
            "PhD": 3
        }

        model_input = pd.DataFrame([{
            "years_experience": experience_months,
            "skills_match_score": match_score,
            "education_level": education_map.get(education_level, 1),
            "project_count": project_count,
            "resume_length": resume_length,
            "github_activity": github_activity
        }])

        prediction = model.predict(model_input)[0]

        if prediction == 1:
            ai_prediction = "Shortlisted"
        else:
            ai_prediction = "Rejected"

        
        # -----------------------------
        # Final Resume Score
        # -----------------------------
        

        result = calculate_resume_score(
            match_score,
            ats_score,
            project_count,
            experience_months,
            education_level,
            github_activity,
            resume_sections,
            linkedin_activity
        )

        suggestions = generate_resume_suggestions(

            resume_skills,

            required_skills,

            project_count,

            experience_months,

            education_level,

            github_activity,

            linkedin_activity,
            
            resume_sections

)

        resume_score = result["final_score"]

        # -----------------------------
        # AI Prediction
        # -----------------------------

        st.subheader("🤖 AI Prediction")

        if ai_prediction == "Shortlisted":
            st.success("✅ AI Model predicts this resume is likely to be shortlisted.")
        else:
            st.error("❌ AI Model predicts this resume is likely to be rejected.")

        # -----------------------------
        # Final Recruiter Decision
        # -----------------------------

        status, icon , reasons = calculate_shortlist_status(
            resume_score,
            ats_score,
            match_score,
            project_count,
            experience_months,
            github_activity,
            linkedin_activity,
            completeness_score
        )

        st.subheader("🏆 Final Recruiter Decision")

        if status == "Strongly Shortlisted":
            st.success(f"{icon} {status}")

        elif status == "Shortlisted":
            st.success(f"{icon} {status}")

        elif status == "Needs Manual Review":
            st.warning(f"{icon} {status}")

        else:
            st.error(f"{icon} {status}")

        st.subheader("decision reason")
        for reason in reasons:
            st.write(reason)
        

        st.subheader("🎯 ATS Score")

        st.progress(ats_score / 100)

        st.metric(
            label="Overall ATS Score",
            value=f"{ats_score}%"
        )

        st.subheader("📊 Score Breakdown")

        st.write("🎯 JD Match Score:", result["match_score"])

        st.write("🛠 ATS Skill Score:", result["skill_score"])

        st.write("📂 Project Score:", result["project_score"])

        st.write("💼 Experience Score:", result["experience_score"])

        st.write("🎓 Education Score:", result["education_score"])

        st.write("🐙 GitHub Score:", result["github_score"])

        st.write("🐙 Linkedin Score:", result["linkedin_score"])

        st.write("⭐ Final Resume Score:", result["final_score"])

        st.subheader("📄 Resume Completeness Score")

        st.progress(completeness_score / 100)

        st.metric(
            label="Resume Completeness",
            value=f"{completeness_score}%"
        )

        st.subheader("💡 Resume Improvement Suggestions")

        if len(suggestions) == 0:

            st.success("Excellent! No major suggestions found.")

        else:

            for suggestion in suggestions:

                st.warning(suggestion)

        st.subheader("📑 Resume Section Analysis")

        left, right = st.columns(2)

        items = list(resume_sections.items())

        mid = len(items) // 2

        with left:
            for section, present in items[:mid]:
                if present:
                    st.success(f"✅ {section}")
                else:
                    st.error(f"❌ {section}")

        with right:
            for section, present in items[mid:]:
                if present:
                    st.success(f"✅ {section}")
                else:
                    st.error(f"❌ {section}")

        if completeness_score >= 90:
            st.success("✅ Excellent Resume Structure")

        elif completeness_score >= 75:
            st.info("👍 Good Resume Structure")

        elif completeness_score >= 50:
            st.warning("⚠ Resume is missing some important sections")

        else:
            st.error("❌ Resume needs major improvements")

        
            
        st.divider()

        st.header("📊 Resume Analysis Dashboard")

        st.subheader("🏆 Overall Resume Rating")

        if resume_score >= 85:
            st.success("⭐⭐⭐⭐⭐ Excellent Resume")

        elif resume_score >= 70:
            st.info("⭐⭐⭐⭐ Good Resume")

        elif resume_score >= 50:
            st.warning("⭐⭐⭐ Average Resume")

        else:
            st.error("⭐⭐ Needs Improvement")


        st.subheader("📈 Resume Score Breakdown")

        st.write(f"✅ JD Match Score : {match_score}%")
        st.write(f"✅ ATS Score : {ats_score}%")

        st.info(f"""
        Resume Score Formula

        70% × JD Match ({match_score}%)
        +
        30% × ATS Score ({ats_score}%)

        = Resume Score ({resume_score}%)
        """)



        # -------------------------------
        # Candidate Details
        # -------------------------------

        col1, col2, col3 = st.columns(3)

        col1.metric("Candidate", candidate_name)
        col2.metric("Email", email)
        col3.metric("Phone", phone)

        st.divider()

        # -------------------------------
        # Score Cards
        # -------------------------------

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Resume Score", f"{resume_score}%")
        c2.metric("ATS Score", f"{ats_score}%")
        c3.metric("JD Match", f"{match_score}%")
        skill_match = ats_score
        c4.metric("🎯 Skill Match", f"{skill_match}%")

        # -------------------------------
        # Skills
        # -------------------------------

        left, center, right = st.columns(3)

        with left:

                    st.subheader("✅ Skills Found")

                    for skill in resume_skills:
                        st.success(skill)
        
        with center:

                st.subheader("🎯 Matched Skills")

                if matched_skills:
                    for skill in matched_skills:
                        st.success(skill)
                else:
                    st.warning("No matching skills found.")

        with right:

                    st.subheader("❌ Missing Skills")

                    for skill in missing_skills:
                        st.error(skill)


        st.subheader("📋 Resume Analysis")

        strengths = []
        weaknesses = []

        # Strengths
        if skill_match >= 80:
            strengths.append("Excellent skill match with the selected job role.")
        elif skill_match >= 60:
            strengths.append("Good skill match with the selected job role.")

        if match_score >= 70:
            strengths.append("Resume content closely matches the job description.")

        if len(resume_skills) >= 10:
            strengths.append("Resume contains a good number of technical skills.")

        # Weaknesses
        if missing_skills:
            weaknesses.append(f"Missing {len(missing_skills)} important job-related skills.")

        if ats_score < 60:
            weaknesses.append("Improve ATS score by adding more relevant skills and keywords.")

        if match_score < 50:
            weaknesses.append("Resume content does not closely match the selected job description.")

        
        left, right = st.columns(2)

        with left:
            st.subheader("⭐ Strengths")

            if strengths:
                for item in strengths:
                    st.success(item)
            else:
                st.info("No major strengths identified.")

        with right:
            st.subheader("⚠ Areas to Improve")

            if weaknesses:
                for item in weaknesses:
                    st.warning(item)
            else:
                st.success("No major weaknesses found.")


        st.divider()

        # -------------------------------
        # Suggestions
        # -------------------------------

        st.subheader("💡 Resume Suggestions")

        for tip in recommended_courses:
                    st.info(tip)

                    st.divider()

        # ---------------------------------
        # Score Visualization
        # ---------------------------------


        chart_data = pd.DataFrame({
                    "Category": [
                        "Resume Score",
                        "ATS Score",
                        "JD Match",
                        "Skill Match"
                        
                    ],
                    "Score": [
                        resume_score,
                        ats_score,
                        match_score,
                        skill_match
                    ]
                })

        fig = px.bar(
                    chart_data,
                    x="Category",
                    y="Score",
                    text="Score",
                    color="Category",
                    title="Resume Performance"
                )

        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # ---------------------------------
        # Generate PDF Report
        # ---------------------------------

        pdf_file = "Resume_Report.pdf"

        generate_pdf_report(
            pdf_file,
            candidate_name,
            ats_score,
            match_score,
            resume_score,
            completeness_score,
            ai_prediction,
            status,
            matched_skills,
            missing_skills,
            suggestions,
            strengths,
            weaknesses
        )

        # ---------------------------------
        # Download PDF
        # ---------------------------------

        with open(pdf_file, "rb") as file:

            st.download_button(
                label="📄 Download PDF Report",
                data=file,
                file_name="Resume_Report.pdf",
                mime="application/pdf"
            )
        
elif menu == "Recruiter Mode":

    st.title("🏢 Recruiter Dashboard")

    st.info("Upload multiple resumes to rank candidates.")

    st.subheader("💼 Select Job Role for Screening")

    selected_domain = st.selectbox(
        "Choose a Job Role",
        list(JOB_DESCRIPTIONS.keys()),
        key="recruiter_domain"
    )

    job_description = JOB_DESCRIPTIONS[selected_domain]

    st.text_area(
        "📋 Job Description",
        value=job_description,
        height=220,
        disabled=True,
        key="recruiter_jd"
    )

    uploaded_resumes = st.file_uploader(
        "📂 Upload Multiple Resumes",
        type=["pdf", "docx"],
        accept_multiple_files=True
    )

    analyze_all = st.button(
        "🚀 Analyze All Resumes",
        use_container_width=True
    )

    if analyze_all:

        if not uploaded_resumes:
          st.warning("Please upload at least one resume.")
          st.stop()

        st.success(f"✅ {len(uploaded_resumes)} resumes uploaded successfully.")

        results = []

        all_skills = load_skills()

        required_skills = extract_required_skills(
            job_description,
            all_skills
        )

        for resume in uploaded_resumes:

            candidate = parse_resume(resume)

            resume_text = candidate["text"]

            resume_skills = extract_skills(
                resume_text,
                all_skills
            )

            ats_score = calculate_ats_score(
                resume_skills,
                required_skills
            )

            match_score = calculate_match_score(
                resume_text,
                job_description
            )

            
            
            project_count = len(extract_projects(resume_text))

            experience_months = extract_experience(resume_text)

            education_level = extract_education(resume_text)

            github_activity = extract_github(resume_text)

            linkedin_activity = extract_linkedin(resume_text)

            education_map = {
                "High School": 0,
                "Bachelors": 1,
                "Masters": 2,
                "PhD": 3
            }

            resume_length = len(resume_text)

            model_input = pd.DataFrame([{
                "years_experience": experience_months,
                "skills_match_score": match_score,
                "education_level": education_map.get(education_level, 1),
                "project_count": project_count,
                "resume_length": resume_length,
                "github_activity": github_activity
            }])

            prediction = model.predict(model_input)[0]

            prediction_text = "Shortlisted ✅" if prediction == 1 else "Rejected ❌"

            result = calculate_resume_score(
                match_score,
                ats_score,
                project_count,
                experience_months,
                education_level,
                github_activity
            )

            results.append({

                "Candidate": candidate["name"],

                "Email": candidate["email"],

                "Phone": candidate["phone"],

                "Experience": experience_months,

                "Education": education_level,

                "Projects": project_count,

                "GitHub": "Yes" if github_activity else "No",

                "LinkedIn": "Yes" if linkedin_activity else "No",

                "ATS Score": ats_score,

                "JD Match": match_score,

                "Resume Score": result["final_score"],

                "AI Prediction": prediction_text

        })

        ranking = pd.DataFrame(results)

        ranking = ranking.sort_values(
            by="Resume Score",
            ascending=False
        ).reset_index(drop=True)

        ranking.index = ranking.index + 1

        st.subheader("🏆 Candidate Ranking")

        st.dataframe(
            ranking,
            use_container_width=True
        )


        st.divider()

        st.subheader("📊 Recruitment Summary")

        total_candidates = len(ranking)

        shortlisted = len(
            ranking[ranking["AI Prediction"] == "Shortlisted ✅"]
        )

        rejected = len(
            ranking[ranking["AI Prediction"] == "Rejected ❌"]
        )

        average_score = round(
            ranking["Resume Score"].mean(),
            2
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "👥 Total Resumes",
            total_candidates
        )

        col2.metric(
            "✅ Shortlisted",
            shortlisted
        )

        col3.metric(
            "❌ Rejected",
            rejected
        )

        col4.metric(
            "⭐ Average Score",
            f"{average_score}%"
        )

        st.subheader("📈 Candidate Resume Scores")

        chart = px.bar(
            ranking,
            x="Candidate",
            y="Resume Score",
            color="AI Prediction",
            text="Resume Score",
            title="Candidate Ranking"
        )

        st.plotly_chart(
            chart,
            use_container_width=True
        )

        buffer = BytesIO()

        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            ranking.to_excel(
                writer,
                index=False,
                sheet_name="Recruiter Report"
            )

        buffer.seek(0)

        st.download_button(
            label="📥 Download Recruiter Report (Excel)",
            data=buffer,
            file_name="Recruiter_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


                                