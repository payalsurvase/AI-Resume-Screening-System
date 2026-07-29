import fitz
import pdfplumber
import docx

from models. layout_detector import detect_layout

def extract_with_fitz(file):

    text = ""

    pdf = fitz.open(stream=file.read(), filetype="pdf")

    for page in pdf:

        text += page.get_text("text") + "\n"

    pdf.close()

    file.seek(0)

    return text

def extract_blocks(file):

    text = ""

    pdf = fitz.open(stream=file.read(), filetype="pdf")

    for page in pdf:

        blocks = page.get_text("blocks")

        blocks = sorted(blocks, key=lambda b: (b[1], b[0]))

        for block in blocks:

            text += block[4] + "\n"

    pdf.close()

    file.seek(0)

    return text

def extract_with_pdfplumber(file):

    text = ""

    with pdfplumber.open(file) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:

                text += page_text + "\n"

    file.seek(0)

    return text

def extract_tables(file):

    text = ""

    with pdfplumber.open(file) as pdf:

        for page in pdf.pages:

            tables = page.extract_tables()

            if tables:

                for table in tables:

                    for row in table:

                        row = [cell for cell in row if cell]

                        if row:

                            text += " | ".join(row) + "\n"

    file.seek(0)

    return text


def extract_text(file):

    layout = detect_layout(file)
    texts = []

    # PyMuPDF
    if layout == "single_column":

            try:
                texts.append(extract_with_fitz(file))
            except:
                pass

            try:
                texts.append(extract_blocks(file))
            except:
                pass

    else:

            try:
                texts.append(extract_blocks(file))
            except:
                pass

            try:
                texts.append(extract_with_fitz(file))
            except:
                pass
    # pdfplumber
    try:
        texts.append(extract_with_pdfplumber(file))
    except:
        pass

    # Table Extraction
    try:
        texts.append(extract_tables(file))
    except:
        pass

    # Remove empty outputs
    texts = [t.strip() for t in texts if t.strip()]

    if not texts:
        return ""

    # Select the richest extraction
    
    return extract_with_pdfplumber(file)