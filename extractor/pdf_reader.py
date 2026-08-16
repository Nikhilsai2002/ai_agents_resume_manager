from PyPDF2 import PdfReader
print("Working")
def extract_pdf_text(file):

    text = ""

    pdf = PdfReader(file)

    for page in pdf.pages:
        text += page.extract_text()

    return text