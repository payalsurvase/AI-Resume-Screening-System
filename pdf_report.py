from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderPDF
# from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib.colors import blue
from datetime import datetime

def generate_pdf_report(
        filename,
        candidate_name,
        ats_score,
        match_score,
        resume_score,
        completeness_score,
        ai_prediction,
        recruiter_decision,
        matched_skills,
        missing_skills,
        suggestions,
        strengths,
        weaknesses

):
    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4
    )

    elements = []

    title = Paragraph(
    "<b><font size=20>AI Resume Screening Report</font></b>",
    styles["Title"]
)

    elements.append(title)
    elements.append(Spacer(1, 0.3 * inch))


    candidate = Paragraph(
    f"<b>Candidate:</b> {candidate_name}",
    styles["Normal"]
)

    elements.append(candidate)
    elements.append(Spacer(1, 0.2 * inch))

    summary_heading = Paragraph(
    "<b><font size=16>Executive Summary</font></b>",
    styles["Heading2"]
)

    elements.append(summary_heading)
    elements.append(Spacer(1,0.1*inch))

    summary = f"""
    This resume achieved an ATS Score of <b>{ats_score}%</b>,
    a Job Match Score of <b>{match_score}%</b>,
    and an Overall Resume Score of <b>{resume_score}%</b>.
    The AI model predicted the candidate as <b>{ai_prediction}</b>,
    while the final recruiter decision is
    <b>{recruiter_decision}</b>.
    """

    elements.append(
        Paragraph(summary, styles["Normal"])
    )

    elements.append(Spacer(1,0.25*inch))

    heading = Paragraph(
    "<b><font size=16>Overall Analysis</font></b>",
    styles["Heading2"]
)

    elements.append(heading)
    elements.append(Spacer(1, 0.15 * inch))


    table_data = [

    ["ATS Score", f"{ats_score}%"],

    ["JD Match Score", f"{match_score}%"],

    ["Resume Score", f"{resume_score}%"],

    ["Resume Completeness", f"{completeness_score}%"],

    ["AI Prediction", ai_prediction],

    ["Recruiter Decision", recruiter_decision]

]

    table = Table(
        table_data,
        colWidths=[200,200]
    )

    table.setStyle(

    TableStyle([

        ("BACKGROUND", (0,0), (-1,0), colors.lightblue),

        ("GRID", (0,0), (-1,-1), 1, colors.black),

        ("BACKGROUND", (0,0), (0,-1), colors.whitesmoke),

        ("TEXTCOLOR", (0,0), (-1,-1), colors.black),

        ("FONTNAME", (0,0), (-1,-1), "Helvetica-Bold"),

        ("BOTTOMPADDING", (0,0), (-1,-1), 8),

        ("TOPPADDING", (0,0), (-1,-1), 8),

        ("ALIGN", (1,0), (1,-1), "CENTER")

    ])

)

    elements.append(table)
    elements.append(Spacer(1,0.3*inch))


    heading = Paragraph(
    "<b><font size=16>Score Comparison</font></b>",
    styles["Heading2"]
)

    elements.append(heading)
    elements.append(Spacer(1,0.1*inch))

    drawing = Drawing(400,220)

    chart = VerticalBarChart()

    chart.x = 50
    chart.y = 30

    chart.width = 250
    chart.height = 150

    chart.data = [[
        ats_score,
        match_score,
        resume_score
    ]]

    chart.categoryAxis.categoryNames = [
        "ATS",
        "JD Match",
        "Resume"
    ]

    chart.valueAxis.valueMin = 0
    chart.valueAxis.valueMax = 100
    chart.valueAxis.valueStep = 20

    chart.bars[0].fillColor = blue

    drawing.add(chart)

    elements.append(drawing)

    elements.append(Spacer(1,0.3*inch))


    heading = Paragraph(
    "<b><font size=16>Skills Distribution</font></b>",
    styles["Heading2"]
)

    elements.append(heading)
    elements.append(Spacer(1,0.15*inch))

    drawing = Drawing(300,220)

    pie = Pie()

    pie.x = 65
    pie.y = 15

    pie.width = 150
    pie.height = 150

    pie.data = [
        len(matched_skills),
        len(missing_skills)
    ]

    pie.labels = [
        "Matched",
        "Missing"
    ]

    pie.slices[0].fillColor = colors.green
    pie.slices[1].fillColor = colors.red
    pie.slices[0].strokeColor = colors.white
    pie.slices[1].strokeColor = colors.white

    pie.sideLabels = True

    drawing.add(pie)

    elements.append(drawing)

    elements.append(Spacer(1,0.25*inch))

    heading = Paragraph(
    "<b><font size=16>Final Verdict</font></b>",
    styles["Heading2"]
)

    elements.append(heading)
    elements.append(Spacer(1,0.1*inch))

    if recruiter_decision == "Strongly Shortlisted":

        verdict = "<font color='green'><b>★★★★★ Strongly Shortlisted</b></font>"

    elif recruiter_decision == "Shortlisted":

        verdict = "<font color='green'><b>★★★★ Shortlisted</b></font>"

    elif recruiter_decision == "Needs Manual Review":

        verdict = "<font color='orange'><b>★★★ Needs Manual Review</b></font>"

    else:

        verdict = "<font color='red'><b>★★ Rejected</b></font>"

    verdict_table = Table([[Paragraph(verdict, styles["BodyText"])]], colWidths=[400])

    verdict_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.whitesmoke),
        ("BOX", (0,0), (-1,-1), 1, colors.black),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("TOPPADDING", (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
    ]))

    elements.append(verdict_table)

    elements.append(Spacer(1,0.25*inch))

    heading = Paragraph(
    "<b><font size=16>Matched Skills</font></b>",
    styles["Heading2"]
)

    elements.append(heading)
    elements.append(Spacer(1,0.1*inch))

    for skill in matched_skills:

        elements.append(

            Paragraph(
                f"<font color='green'>✓</font> {skill}",
                styles["Normal"]
            )

        )

    elements.append(Spacer(1,0.25*inch))

    heading = Paragraph(
    "<b><font size=16>Missing Skills</font></b>",
    styles["Heading2"]
)

    elements.append(heading)
    elements.append(Spacer(1,0.1*inch))

    if len(missing_skills)==0:

        elements.append(

            Paragraph(
                "No missing skills found.",
                styles["Normal"]
            )

        )

    else:

        for skill in missing_skills:

            elements.append(

                Paragraph(f"<font color='red'>✗</font> {skill}", styles["Normal"])

            )
    elements.append(Spacer(1,0.25*inch))


    heading = Paragraph(
    "<b><font size=16>Strengths</font></b>",
    styles["Heading2"]
)

    elements.append(heading)
    elements.append(Spacer(1,0.1*inch))

    if strengths:

        for item in strengths:

            elements.append(
                Paragraph(
                    f"✓ {item}",
                    styles["Normal"]
                )
            )

    else:

        elements.append(
            Paragraph(
                "No major strengths identified.",
                styles["Normal"]
            )
        )

    elements.append(Spacer(1,0.25*inch))

    heading = Paragraph(
    "<b><font size=16>Areas to Improve</font></b>",
    styles["Heading2"]
)

    elements.append(heading)
    elements.append(Spacer(1,0.1*inch))

    if weaknesses:

        for item in weaknesses:

            elements.append(
                Paragraph(
                    f"✗ {item}",
                    styles["Normal"]
                )
            )

    else:

        elements.append(
            Paragraph(
                "No major weaknesses found.",
                styles["Normal"]
            )
        )

    elements.append(Spacer(1,0.25*inch))

    heading = Paragraph(
    "<b><font size=16>Resume Improvement Suggestions</font></b>",
    styles["Heading2"]
)

    elements.append(heading)
    elements.append(Spacer(1, 0.1 * inch))

    if suggestions:

        for suggestion in suggestions:

            elements.append(
                Paragraph(
                    f"• {suggestion}",
                    styles["Normal"]
                )
            )

    else:

        elements.append(
            Paragraph(
                "Excellent! No major suggestions found.",
                styles["Normal"]
            )
        )

    elements.append(Spacer(1,0.3*inch))



    def add_footer(canvas, doc):
        canvas.saveState()

        canvas.setFont("Helvetica", 9)

        canvas.drawString(
            40,
            20,
            f"Generated on: {datetime.now().strftime('%d-%m-%Y %I:%M %p')}"
        )

        canvas.drawRightString(
            550,
            20,
            f"Page {doc.page}"
        )

        canvas.restoreState()

    doc.build(
        elements,
        onFirstPage=add_footer,
        onLaterPages=add_footer
    )

