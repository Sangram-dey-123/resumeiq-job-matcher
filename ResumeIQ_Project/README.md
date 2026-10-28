
# ResumeIQ — AI Resume & Job Matcher

ResumeIQ is a resume analysis web application that helps users compare their resumes against a target job description. It identifies matching skills, potential skill gaps, and keywords that may help users improve their job applications.

> **Note:** This is an educational prototype that uses rule-based text and skill matching. It does not use a generative AI model or provide an official ATS score.

## Features

- Upload a resume in PDF format.
- Enter a target job title and paste a job description.
- Calculate an estimated resume-to-job match score.
- Identify matching and potentially missing skills.
- View a side-by-side skill comparison table.
- Review job description keywords.
- Get practical resume improvement suggestions.
- Download a text report of the analysis.
- Use a clean, interactive Streamlit interface.

## Technologies Used

- Python
- Streamlit
- PyMuPDF
- Pandas
- Regular expressions

## Project Structure

```text
resumeiq-job-matcher/
├── app.py
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/resumeiq-job-matcher.git
cd resumeiq-job-matcher
```

Replace `YOUR-USERNAME` with the GitHub account username that owns the repository.

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
streamlit run app.py
```

The application will open in your browser at the local URL shown in the terminal.

## Deployment

The application can be deployed using Streamlit Community Cloud.

1. Push `app.py`, `requirements.txt`, and `README.md` to GitHub.
2. Sign in to Streamlit Community Cloud.
3. Create an app and select the GitHub repository.
4. Set the main file path to `app.py`.
5. Deploy and open the generated application URL.

## How It Works

1. The user uploads a text-based PDF resume.
2. Resume text is extracted using PyMuPDF.
3. The user provides a job description.
4. The application detects recognised skills and compares them.
5. A heuristic match score is calculated using skill coverage and keyword overlap.
6. The results and recommendations are displayed and can be downloaded.

## Limitations

- The current version uses predefined skill lists and rule-based matching.
- Scanned image-only PDFs may require OCR before analysis.
- The match score is an estimate and may miss synonyms, context, or transferable skills.
- The application does not predict hiring outcomes or guarantee ATS compatibility.
- Resume suggestions should be reviewed by the user for accuracy.
- No generative AI API is integrated in this version.

## Privacy

Use test resumes when demonstrating the application. Avoid uploading sensitive personal information unnecessarily. Review the hosting platform's data-handling policies before processing real resumes.

## Future Improvements

- Add an optional AI-powered feedback feature.
- Expand the skill library and recognise synonyms.
- Support DOCX resumes.
- Add resume section analysis and formatting checks.
- Export reports as PDF.
- Add secure user accounts and saved analysis history.

## Disclaimer

ResumeIQ is intended for educational and career-preparation purposes. Its scores and suggestions are informational and should not be treated as official ATS assessments or hiring decisions.
