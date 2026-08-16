import json
import streamlit as st

from extractor.pdf_reader import extract_pdf_text
from extractor.docx_reader import extract_docx_text
from extractor.txt_reader import extract_txt_text


st.set_page_config(
    page_title="Agentic ATS",
    layout="wide"
)

st.title("AI Resume & Job Application Manager (V2)")

selected_role = st.selectbox(
    "Select Job Role",
    [
        "AI Engineer",
        "Data Engineer",
        "Python Developer"
    ]
)

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx", "txt"]
)

if uploaded_file:

    # Extract Text

    if uploaded_file.name.endswith(".pdf"):
        resume_text = extract_pdf_text(uploaded_file)

    elif uploaded_file.name.endswith(".docx"):
        resume_text = extract_docx_text(uploaded_file)

    else:
        resume_text = extract_txt_text(uploaded_file)

    st.success("Resume Text Extracted Successfully")

    st.subheader("Resume Text")

    st.text_area(
        "Extracted Text",
        resume_text,
        height=300
    )

    # Load JD

    role_map = {
        "AI Engineer":
            "jd/ai_engineer.json",

        "Data Engineer":
            "jd/data_engineer.json",

        "Python Developer":
            "jd/python_developer.json"
    }

    with open(
        role_map[selected_role],
        "r"
    ) as file:

        jd = json.load(file)

    st.subheader("Selected JD")

    st.json(jd)