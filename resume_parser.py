from docx import Document
from pypdf import PdfReader
from jobs import jobs
import re


def extract_resume_details(file_path):

    text = ""

    # DOCX
    if file_path.lower().endswith(".docx"):

        doc = Document(file_path)

        for para in doc.paragraphs:
            text += para.text + "\n"

    # PDF
    elif file_path.lower().endswith(".pdf"):

        pdf = PdfReader(file_path)

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    # TXT
    elif file_path.lower().endswith(".txt"):

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

    # Extract Email
    email_match = re.search(
        r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',
        text
    )

    email = ""

    if email_match:
        email = email_match.group()

    # Extract Mobile
    clean_text = text.replace(" ", "").replace("-", "")

    mobile_match = re.search(
        r'(\+91)?[6-9]\d{9}',
        clean_text
    )

    mobile = ""

    if mobile_match:
        mobile = mobile_match.group()

    # Extract Candidate Name
    candidate_name = ""

    lines = text.split("\n")

    for line in lines:

        line = line.strip()

        if line.lower().startswith("name:"):

            candidate_name = (
                line.replace("Name:", "")
                    .replace("name:", "")
                    .strip()
            )

            break

        if (
            line
            and "@" not in line
            and "/" not in line
            and "\\" not in line
            and "--" not in line
            and len(line.split()) <= 5
        ):

            candidate_name = line

            break

    # Skills Database
    skills_db = [
        "AWS",
        "Docker",
        "Kubernetes",
        "Terraform",
        "Jenkins",
        "Git",
        "Linux",
        "Python",
        "Ansible",
        "Prometheus",
        "Grafana",
        "MySQL",
        "Oracle",
        "Bash"
    ]

    matched_skills = []

    for skill in skills_db:
        pattern = r"\b" + re.escape(skill) + r"\b"

        if skill.lower() in text.lower():
            matched_skills.append(skill)
         
    print("=" * 50)
    print("Matched Skills:", matched_skills)
    print("=" * 50)

    # Job Matching
        # Job Matching
    job_matches = []

    for job in jobs:

        common_skills = list(
            set(matched_skills) &
            set(job["skills"])
        )

        score = int(
            len(common_skills) /
            len(job["skills"]) * 100
        )

        job_matches.append({
            "job_title": job["title"],
            "match_score": score,
            "matched_skills": common_skills
        })

    # Sort jobs by highest score
    job_matches.sort(
        key=lambda job: job["match_score"],
        reverse=True
    )

    return {
        "candidate_name": candidate_name,
        "email": email,
        "mobile": mobile,
        "text": text,
        "matched_skills": matched_skills,
        "job_matches": job_matches
    }
