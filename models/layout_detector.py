import fitz

def detect_layout(file):

    file.seek(0)

    pdf = fitz.open(stream=file.read(), filetype="pdf")

    if len(pdf) == 0:
        pdf.close()
        file.seek(0)
        return "unknown"

    page = pdf[0]

    page_middle = page.rect.width / 2

    blocks = page.get_text("blocks")

    left = 0
    right = 0

    for block in blocks:
        x0 = block[0]

        if x0 < page_middle:
            left += 1
        else:
            right += 1

    pdf.close()
    file.seek(0)

    if left > 5 and right > 5:
        return "two_column"

    return "single_column"