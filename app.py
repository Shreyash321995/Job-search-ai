from fastapi import FastAPI, UploadFile, File
from jobs import jobs
from docx import Document
from pypdf import PdfReader
import sqlite3
import os

app = FastAPI()

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def home():
    return {
        "message": "Welcome to Job Search AI"
    }
@app.get("/resumes")
def get_resumes():

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id,
               filename,
               skills,
               match_score,
               upload_time
        FROM resumes
        """
    )

    rows = cursor.fetchall()

    conn.close()

    resumes = []

    for row in rows:

        resumes.append({
            "id": row[0],
            "filename": row[1],
            "skills": row[2],
            "match_score": row[3],
            "upload_time": row[4]
        })

    return resumes
@app.get("/resume/{id}")
def get_resume(id: int):

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id,
               filename,
               skills,
               match_score,
               upload_time
        FROM resumes
        WHERE id = ?
        """,
        (id,)
    )

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return {
            "error": "Resume not found"
        }

    return {
        "id": row[0],
        "filename": row[1],
        "skills": row[2],
        "match_score": row[3],
        "upload_time": row[4]
    }
@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):

    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = ""

    # DOCX
    if file.filename.lower().endswith(".docx"):

        doc = Document(file_path)

        for para in doc.paragraphs:
            text += para.text + "\n"

    # PDF
    elif file.filename.lower().endswith(".pdf"):

        pdf = PdfReader(file_path)

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    # TXT
    elif file.filename.lower().endswith(".txt"):

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

    else:

        return {
            "error": "Supported formats: .docx, .pdf, .txt"
        }

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
        if skill.lower() in text.lower():
            matched_skills.append(skill)

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

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()
    skills_string = ",".join(matched_skills)

    highest_match_score = max(
    job["match_score"]
    for job in job_matches
    )

    cursor.execute(
       """INSERT INTO resumes (filename,skills,match_score) VALUES (?,?,?)""",
        (file.filename,skills_string,highest_match_score)
    )

    conn.commit()

    conn.close()

    return {
        "filename": file.filename,
        "skills": matched_skills,
        "job_matches": job_matches
    }
