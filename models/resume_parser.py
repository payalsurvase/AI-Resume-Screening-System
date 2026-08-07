
import docx
import re
import fitz
import streamlit as st

from models.text_extractor import extract_text

# -----------------------------
# Read PDF using PyMuPDF
# -----------------------------
def read_pdf_fitz(file):

    text = ""

    pdf = fitz.open(stream=file.read(), filetype="pdf")

    for page in pdf:

        text += page.get_text("text") + "\n"

    pdf.close()

    file.seek(0)

    return text

def extract_pdf_links(file):

    links = []

    pdf = fitz.open(stream=file.read(), filetype="pdf")

    for page in pdf:

        page_links = page.get_links()

        for link in page_links:

            if "uri" in link:
                links.append(link["uri"])

    pdf.close()

    file.seek(0)

    return links
# -----------------------------
# Read PDF Resume
# -----------------------------
def read_pdf(file):

    text = ""

    with pdfplumber.open(file) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


# -----------------------------
# Read DOCX Resume
# -----------------------------
def read_docx(file):

    document = docx.Document(file)

    text = ""

    for para in document.paragraphs:

        text += para.text + "\n"

    return text


# -----------------------------
# Extract Email
# -----------------------------
def extract_email(text):

    email = re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    if email:
        return email[0]

    return "Not Found"


# -----------------------------
# Extract Phone Number
# -----------------------------
def extract_phone(text):

    phone = re.findall(
        r"\+?\d[\d\s\-]{8,15}",
        text
    )

    if phone:
        return phone[0]

    return "Not Found"


# -----------------------------
# Extract Name
# -----------------------------
def extract_name(text):

    lines = text.split("\n")

    for line in lines:

        if len(line.strip()) > 2 and len(line.strip()) < 40:

            return line.strip()

    return "Unknown"


# -----------------------------
# Main Parser Function
# -----------------------------
def parse_resume(uploaded_file):


    if uploaded_file is None:
        return{
            "name" : " ",
            "email": " ",
            "phone": " ",
            "text": " "
        }

    if uploaded_file.name.endswith(".pdf"):
        resume_text = extract_text(uploaded_file)
        # st.write(resume_text)
        links = extract_pdf_links(uploaded_file)

        if links:
            resume_text += "\n" + "\n".join(links)

    elif uploaded_file.name.endswith(".docx"):
        resume_text = read_docx(uploaded_file)

    else:
        resume_text = ""

    candidate = {

        "name": extract_name(resume_text),

        "email": extract_email(resume_text),

        "phone": extract_phone(resume_text),

        "text": resume_text

    }

    return candidate