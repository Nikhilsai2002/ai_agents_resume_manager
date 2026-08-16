from docx import Document

def extract_docx_text(file):

    doc = Document(file)

    text = "\n".join(
        para.text
        for para in doc.paragraphs
    )

    return text