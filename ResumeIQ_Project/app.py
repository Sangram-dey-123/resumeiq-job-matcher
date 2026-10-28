
import re
import io
import fitz
import streamlit as st
import pandas as pd
from collections import Counter
from datetime import datetime

st.set_page_config(
    page_title="ResumeIQ | AI Resume & Job Matcher",
    page_icon="🎯",
    layout="wide"
)

# ---------- DESIGN ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f4f7ff 0%, #edf4ff 100%);
    color: #172033 !important;
}

.main .block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Make headings and normal text readable */
.stMarkdown h1,
.stMarkdown h2,
.stMarkdown h3,
.stMarkdown h4,
.stMarkdown p,
.stMarkdown li,
.stMarkdown label {
    color: #172033 !important;
}

/* Header banner */
.hero {
    padding: 28px;
    border-radius: 20px;
    background: linear-gradient(120deg, #14213d, #2457a7);
    color: white !important;
    margin-bottom: 24px;
}

.hero h1 {
    color: #ffffff !important;
    margin-bottom: 8px;
}

.hero p {
    color: #edf3ff !important;
    font-size: 17px;
}

/* Dashboard metric cards */
.metric-card {
    background: #ffffff;
    border: 1px solid #d6e2f3;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
}

.metric-value {
    font-size: 30px;
    font-weight: 750;
    color: #1d4ed8 !important;
}

.metric-label {
    color: #475569 !important;
}

/* Matching skills: dark green text */
.skill-match {
    background: #dcfce7;
    color: #166534 !important;
    border-left: 5px solid #16a34a;
    padding: 13px 16px;
    border-radius: 9px;
    margin: 8px 0;
    font-weight: 600;
}

/* Missing skills: dark red text */
.skill-gap {
    background: #fee2e2;
    color: #991b1b !important;
    border-left: 5px solid #dc2626;
    padding: 13px 16px;
    border-radius: 9px;
    margin: 8px 0;
    font-weight: 600;
}

/* Information cards */
.section-card {
    background: #ffffff;
    color: #172033 !important;
    padding: 20px;
    border: 1px solid #d6e2f3;
    border-radius: 15px;
    margin-bottom: 14px;
}

.small-note {
    color: #475569 !important;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# ---------- SKILL LIBRARY ----------
SKILL_LIBRARY = {
    "Python": ["python", "pandas", "numpy", "scipy", "flask", "django"],
    "Machine Learning": [
        "machine learning", "scikit-learn", "sklearn",
        "supervised learning", "unsupervised learning",
        "model training", "model evaluation"
    ],
    "AI & Deep Learning": [
        "artificial intelligence", "deep learning",
        "neural networks", "tensorflow", "pytorch",
        "natural language processing", "nlp", "computer vision",
        "generative ai", "large language models", "llm"
    ],
    "Data Analysis": [
        "data analysis", "data analytics", "excel",
        "power bi", "tableau", "statistics", "data visualization",
        "data cleaning", "data wrangling"
    ],
    "Programming": [
        "java", "c++", "c#", "javascript", "typescript",
        "sql", "html", "css", "git", "github", "rest api"
    ],
    "Cloud & Tools": [
        "aws", "azure", "google cloud", "docker",
        "kubernetes", "linux", "streamlit", "fastapi"
    ],
    "Professional Skills": [
        "communication", "teamwork", "leadership",
        "problem solving", "project management", "critical thinking"
    ]
}

def normalize(text):
    """Normalize text while preserving useful technical terms."""
    text = text.lower()
    text = text.replace("c++", "cplusplus")
    text = text.replace("c#", "csharp")
    text = re.sub(r"[^a-z0-9+#.\s-]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def extract_pdf(uploaded_file):
    """Extract text from an uploaded PDF."""
    data = uploaded_file.getvalue()
    document = fitz.open(stream=data, filetype="pdf")
    pages = [page.get_text() for page in document]
    document.close()
    return "\n".join(pages).strip()

def detect_skills(text):
    normalized = normalize(text)
    found = []

    for category, skills in SKILL_LIBRARY.items():
        for skill in skills:
            term = normalize(skill)
            if re.search(
                r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])",
                normalized
            ):
                found.append((skill, category))

    # Keep each skill only once.
    unique = {}
    for skill, category in found:
        unique[skill] = category

    return unique

def find_keywords(text, limit=12):
    """Find frequent non-generic words as additional job keywords."""
    stop_words = set("""
        the and for with that this from have has will are was were our
        you your they their them about into using use used required
        requirements responsibilities candidate role work working team
        experience skills ability strong good excellent preferred plus
        must should would can may all any per etc who what when where
        job description position looking ideal across within support
        including such ensure develop developing build building
    """.split())

    words = re.findall(r"\b[a-zA-Z][a-zA-Z0-9+#.-]{2,}\b", text.lower())
    counts = Counter(
        word for word in words
        if word not in stop_words and not word.isdigit()
    )
    return [word for word, _ in counts.most_common(limit)]

def analyse_resume(resume_text, job_text):
    resume_skills = detect_skills(resume_text)
    job_skills = detect_skills(job_text)

    resume_set = set(resume_skills)
    job_set = set(job_skills)

    matched = sorted(resume_set & job_set)
    missing = sorted(job_set - resume_set)

    if job_set:
        skill_score = round(100 * len(matched) / len(job_set))
    else:
        skill_score = 0

    # Additional keyword overlap, clearly separated from skill matching.
    resume_words = set(normalize(resume_text).split())
    job_words = set(normalize(job_text).split())

    keywords = [
        word for word in find_keywords(job_text, 15)
        if word not in {"years", "year", "knowledge"}
    ]
    keyword_matches = [word for word in keywords if word in resume_words]

    if keywords:
        keyword_score = round(100 * len(keyword_matches) / len(keywords))
    else:
        keyword_score = 0

    # Transparent heuristic, not a real ATS score.
    overall_score = round(0.8 * skill_score + 0.2 * keyword_score)

    return {
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched": matched,
        "missing": missing,
        "skill_score": skill_score,
        "keyword_score": keyword_score,
        "overall_score": overall_score,
        "keywords": keywords,
        "keyword_matches": keyword_matches,
    }

def make_report(results, job_title):
    lines = [
        "RESUMEIQ — RESUME AND JOB MATCH REPORT",
        "=" * 45,
        f"Job title: {job_title or 'Not specified'}",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        f"Estimated match score: {results['overall_score']}%",
        f"Skill coverage: {results['skill_score']}%",
        f"Keyword overlap: {results['keyword_score']}%",
        "",
        "MATCHING SKILLS",
        *([f"- {x}" for x in results["matched"]] or ["- None detected"]),
        "",
        "SKILLS TO CONSIDER DEVELOPING",
        *([f"- {x}" for x in results["missing"]] or ["- No missing listed skills detected"]),
        "",
        "SUGGESTED JOB KEYWORDS",
        *([f"- {x}" for x in results["keywords"]] or ["- None detected"]),
        "",
        "IMPORTANT DISCLAIMER",
        "This report uses rule-based text and skill matching. It is not",
        "a genuine ATS score, hiring prediction, or guarantee of selection.",
        "Review every suggestion and include only truthful qualifications."
    ]
    return "\n".join(lines)

# ---------- HEADER ----------
st.markdown("""
<div class="hero">
    <h1>🎯 ResumeIQ</h1>
    <p>Understand your resume's alignment with a job description.</p>
    <p>Discover matching skills, identify gaps, and improve your application.</p>
</div>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.title("ResumeIQ")
    st.caption("Your job application companion")
    st.markdown("---")
    st.markdown("### How it works")
    st.write("1. Upload your resume in PDF format.")
    st.write("2. Paste the target job description.")
    st.write("3. Review the match and skill gaps.")
    st.write("4. Download your report.")
    st.markdown("---")
    st.caption("Your resume is processed in this app session. Avoid uploading sensitive information you do not need to analyse.")

# ---------- INPUTS ----------
st.subheader("1. Add your resume and target role")

left, right = st.columns(2)

with left:
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF)",
        type=["pdf"],
        help="Text-based PDFs work best. Scanned image-only PDFs may need OCR."
    )
    job_title = st.text_input(
        "Target job title",
        placeholder="e.g. Junior Data Scientist"
    )

with right:
    job_description = st.text_area(
        "Paste the full job description",
        height=190,
        placeholder="Paste the responsibilities, qualifications and required skills here..."
    )

analyse_button = st.button(
    "🔍 Analyse Resume",
    type="primary",
    use_container_width=True
)

if analyse_button:
    if uploaded_file is None:
        st.error("Please upload a PDF resume first.")
    elif not job_description.strip():
        st.error("Please paste a job description first.")
    else:
        try:
            with st.spinner("Extracting text and comparing skills..."):
                resume_text = extract_pdf(uploaded_file)

                if len(resume_text) < 30:
                    st.error(
                        "Very little text was extracted. This may be a scanned PDF. "
                        "Try a text-based PDF or run OCR first."
                    )
                    st.stop()

                results = analyse_resume(resume_text, job_description)

                st.session_state["results"] = results
                st.session_state["job_title"] = job_title
                st.session_state["report"] = make_report(results, job_title)

        except Exception as error:
            st.error(
                "The PDF could not be processed. Please try another text-based PDF."
            )
            st.caption(f"Technical detail: {error}")

# ---------- RESULTS ----------
if "results" in st.session_state:
    results = st.session_state["results"]

    st.markdown("---")
    st.subheader("2. Your analysis results")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{results['overall_score']}%</div>
            <div class="metric-label">Estimated match</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(results['matched'])}</div>
            <div class="metric-label">Matching skills</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(results['missing'])}</div>
            <div class="metric-label">Potential skill gaps</div>
        </div>
        """, unsafe_allow_html=True)

    st.progress(results["overall_score"] / 100)

    st.info(
        "The estimated match is a rule-based comparison, not an official ATS score. "
        "It measures the skills and keywords this prototype can recognise."
    )

    st.markdown("### Skill coverage")
    st.write(f"**Recognised skill coverage:** {results['skill_score']}%")
    st.progress(results["skill_score"] / 100)
    st.write(f"**Keyword overlap:** {results['keyword_score']}%")
    st.progress(results["keyword_score"] / 100)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ✅ Matching skills")
        if results["matched"]:
        for skill in results["matched"]:
        st.markdown(
        f'<div class="skill-match">✓ {skill.title()}</div>',
        unsafe_allow_html=True
        )
        else:
        st.info("No matching skills were recognised.")

    with col2:
        st.markdown("### 📌 Potential skill gaps")
        if results["missing"]:
        for skill in results["missing"]:
        st.markdown(
        f'<div class="skill-gap">! {skill.title()}</div>',
        unsafe_allow_html=True
        )
        else:
        st.success("No gaps detected in the recognised skill list.")

    st.markdown("### 🧩 Skill comparison table")

    all_skills = sorted(set(results["job_skills"]) | set(results["resume_skills"]))

    if all_skills:
        table_rows = []
        for skill in all_skills:
            table_rows.append({
                "Skill": skill,
                "Category": results["job_skills"].get(
                    skill, results["resume_skills"].get(skill, "Other")
                ),
                "In resume": "Yes" if skill in results["resume_skills"] else "No",
                "In job description": "Yes" if skill in results["job_skills"] else "No",
                "Status": (
                    "Match" if skill in results["matched"]
                    else "Potential gap" if skill in results["missing"]
                    else "Resume-only skill"
                )
            })

        st.dataframe(
            pd.DataFrame(table_rows),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.write("No recognised skills found. Try a more detailed job description.")

    st.markdown("### 💡 Improvement suggestions")

    if results["missing"]:
        st.write(
            "Review these skills and learn or practise the ones that are genuinely "
            "relevant to your career goals:"
        )
        st.write(", ".join(results["missing"]))

        st.write(
            "If you already have one of these skills, consider making your relevant "
            "experience easier to find in your resume. Do not add skills you do not have."
        )
    else:
        st.write(
            "Check whether your resume provides clear evidence of the relevant skills "
            "through projects, experience, or achievements."
        )

    if results["keywords"]:
        st.markdown("### 🔑 Job description keywords")
        st.write(", ".join(results["keywords"]))

    st.markdown("### 📥 Download your report")

    st.download_button(
        label="Download analysis report (.txt)",
        data=st.session_state["report"],
        file_name="resume_match_report.txt",
        mime="text/plain",
        use_container_width=True
    )

    st.markdown("---")
    st.caption(
        "Privacy note: this prototype does not intentionally save resumes to a database. "
        "The hosting environment may still process session data. Use a test resume when demonstrating."
    )

else:
    st.markdown("""
    <div class="section-card">
        <h3>✨ What you'll get</h3>
        <p>✔ An estimated resume-to-job match score</p>
        <p>✔ Matching and missing skills</p>
        <p>✔ A side-by-side skills comparison</p>
        <p>✔ Practical improvement suggestions</p>
        <p>✔ A downloadable report</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("ResumeIQ · Educational prototype · Match scores are estimates, not hiring predictions.")
