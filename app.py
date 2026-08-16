import streamlit as st
 

from services.recommendation import (
    get_recommendation
)
from extractor.pdf_reader import extract_pdf_text
from extractor.docx_reader import extract_docx_text
from extractor.txt_reader import extract_txt_text

 
from services.jd_matcher import (
    load_jd,
    compare_skills
)

st.title("AI Resume & Job Application Manager")
 
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

    # Extract text based on file type
    if uploaded_file.name.endswith(".pdf"):
        text = extract_pdf_text(uploaded_file)

    elif uploaded_file.name.endswith(".docx"):
        text = extract_docx_text(uploaded_file)

    else:
        text = extract_txt_text(uploaded_file)

    # Parse resume
    parsed_data = parse_resume_json(text)

    jd = load_jd(selected_role)

    matching_result = compare_skills(
        parsed_data["skills"],
        jd["mandatory_skills"],
        jd["good_to_have_skills"]
    )

    ats_score = matching_result["match_percentage"]

    if ats_score >= 70:
        recommendation = "✅ Eligible"

    elif ats_score >= 50:
        recommendation = "⚠ Needs Review"

    else:
        recommendation = "❌ Not Eligible"

    st.subheader("Resume Details")
    st.write("### Name")
    st.write(parsed_data["name"])
    st.write("### Email")
    st.write(parsed_data["email"])

    st.write("### Phone")
    st.write(parsed_data["phone"])

    st.write("### Skills Found")

    for skill in parsed_data["skills"]:
        st.write(f"✅ {skill}")

    st.subheader("Skill Matching Report")

    st.write(
        f"Match Percentage: {matching_result['match_percentage']}%"
    )

    st.write("### Mandatory Skills Matched")

    for skill in matching_result["matched_mandatory"]:
        st.write(f"✅ {skill}")

    st.write("### Mandatory Skills Missing")

    for skill in matching_result["missing_mandatory"]:
        st.write(f"❌ {skill}")

    st.write("### Good To Have Skills Matched")

    for skill in matching_result["matched_good"]:
        st.write(f"⭐ {skill}")

    st.subheader("ATS Evaluation")

    st.metric(
        "ATS Score",
        f"{ats_score}/100"
    )

    st.write(
        f"### Recommendation: {recommendation}"
    )

    st.subheader("Extracted Resume Text")

    st.text_area(
        "",
        text,
        height=300
    )

    st.subheader("AI Agent Evaluation")

    st.info(
        """
        Resume Parser Agent and ATS Evaluator Agent
        are ready for integration.
        
        Current version uses rule-based ATS scoring.
        """
    )