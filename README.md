# ResumeIQ — AI Resume & Job Matcher

ResumeIQ is a resume analysis web application that helps users compare their resumes against a target job description. It identifies matching skills, potential skill gaps, and relevant keywords to help users improve their job applications.

> **Note:** This is an educational prototype that uses rule-based text and skill matching. It does not use a generative AI model or provide an official ATS score.

## 🚀 Live Demo

**Try the application:** [ResumeIQ — Live Demo](https://resumeiq-job-matcher-lb2kyynepfeqskkg6gnxrp.streamlit.app/)

## ✨ Features

- Upload a resume in PDF format.
- Enter a target job title and paste a job description.
- Calculate an estimated resume-to-job match score.
- Identify matching and potentially missing skills.
- View a side-by-side skill comparison table.
- Extract relevant keywords from the job description.
- Get practical resume improvement suggestions.
- Download a text report containing the analysis.
- Use a clean Streamlit interface with custom CSS styling.
- View results through a structured analysis dashboard.

## 🛠️ Technologies Used

- **Python** — Core application logic.
- **Streamlit** — Interactive web application framework.
- **PyMuPDF** — PDF resume text extraction.
- **Pandas** — Skill comparison tables and data presentation.
- **Regular Expressions** — Text processing and skill detection.
- **HTML and CSS** — Interface layout and styling.

## 📁 Project Structure

```text
resumeiq-job-matcher/
├── app.py
├── requirements.txt
└── README.md
```

## ⏱️ Project Development Timeline — 6-Hour Sprint

The project was organised into a six-hour development sprint, covering application setup, resume processing, skill matching, result generation, interface design, and deployment preparation.

| Time | Development Phase | Work Completed |
|---|---|---|
| Hour 1 | Project Setup | Set up the Python application structure, dependencies, Streamlit configuration, and initial interface. |
| Hour 2 | Resume Processing | Implemented PDF uploading and text extraction using PyMuPDF. |
| Hour 3 | Skill Matching Engine | Created the predefined skill library, skill detection logic, and resume-to-job-description comparison. |
| Hour 4 | Match Scoring and Analysis | Added estimated match scoring, keyword overlap, matching skills, potential skill gaps, and improvement suggestions. |
| Hour 5 | UI Design and Reporting | Developed the results dashboard, skill comparison table, interface styling, and downloadable text report. |
| Hour 6 | Testing and Deployment | Reviewed the main application workflow, refined interface readability, and prepared the application for online deployment through Streamlit Community Cloud. |

### Sprint Deliverables

- A functional Streamlit resume analysis application.
- PDF resume upload and text extraction.
- Rule-based skill matching and job description comparison.
- Estimated match scoring and skill-gap analysis.
- An interactive results dashboard.
- Downloadable text analysis reports.
- An online application demo.

*The timeline represents the planned breakdown of the six-hour sprint. Individual activities should reflect the work actually completed during the project.*

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/resumeiq-job-matcher.git
cd resumeiq-job-matcher
```

Replace `YOUR-USERNAME` with the GitHub username that owns the repository.

### 2. Install dependencies

Run the following command:

```bash
pip install -r requirements.txt
```

If you have not created `requirements.txt`, add the following dependencies to it:

```text
streamlit
pymupdf
pandas
```

### 3. Run the application locally

```bash
streamlit run app.py
```

The application will open in your browser at the local URL displayed in the terminal.

## 🔍 How It Works

1. **Resume Upload:** The user uploads a resume in PDF format.
2. **Text Extraction:** PyMuPDF extracts text from the uploaded PDF.
3. **Job Description Input:** The user enters a target job title and pastes the relevant job description.
4. **Skill Detection:** The application identifies recognised skills using a predefined skill library.
5. **Skill Comparison:** The detected resume skills are compared with those found in the job description.
6. **Match Score Calculation:** A heuristic score is calculated using skill coverage and keyword overlap.
7. **Results Display:** Matching skills, potential skill gaps, comparison tables, and suggestions are displayed.
8. **Report Generation:** The user can download the analysis results as a text file.

## 🌐 Deployment

ResumeIQ is deployed using Streamlit Community Cloud.

To deploy your own version:

1. Push `app.py`, `requirements.txt`, and `README.md` to your GitHub repository.
2. Visit [Streamlit Community Cloud](https://share.streamlit.io/).
3. Sign in and create a new application.
4. Select your GitHub repository.
5. Set the main file path to `app.py`.
6. Deploy the application and open the generated URL.

**Live application:** [https://resumeiq-job-matcher-lb2kyynepfeqskkg6gnxrp.streamlit.app/](https://resumeiq-job-matcher-lb2kyynepfeqskkg6gnxrp.streamlit.app/)

## ⚠️ Limitations

- The application uses predefined skill lists and rule-based matching.
- Scanned image-only PDFs may require OCR before analysis.
- The estimated score may not recognise all synonyms, contextual meanings, or transferable skills.
- The application does not predict hiring outcomes or guarantee ATS compatibility.
- Suggestions should be reviewed for accuracy and relevance.
- A generative AI API is not integrated into the current version.

## 🔒 Privacy

Use test resumes when demonstrating the application. Avoid uploading sensitive personal information unnecessarily. Review the hosting platform's data-handling policies before processing real resumes.

## 🔮 Future Improvements

- Integrate an optional AI-powered resume feedback feature.
- Expand the skill library and improve synonym recognition.
- Add support for DOCX resumes.
- Analyse resume sections, structure, and formatting.
- Enable PDF report generation.
- Add secure user accounts and saved analysis history.
- Improve matching through semantic similarity techniques.

## 📌 Disclaimer

ResumeIQ is intended for educational and career-preparation purposes. The scores and suggestions are informational and should not be treated as official ATS assessments, hiring
