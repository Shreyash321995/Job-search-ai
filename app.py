from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from fastapi import FastAPI, UploadFile, File
from jobs import jobs
from docx import Document
from pypdf import PdfReader
import sqlite3
import os
import re

from resume_parser import extract_resume_details

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def home(request: Request):

    #return {"message": "Frontend Test"}
    return templates.TemplateResponse(
 #       request=request,
  #      name="index.html"
          "index.html",
          {
        "request": request,
#        "candidate_name": candidate_name,
#        "email": email,
#        "mobile": mobile,
#        "skills": matched_skills,
#        "job_matches": job_matches
    }
    )


@app.get("/resumes")
def get_resumes():

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id,
               filename,
               candidate_name,
               email,
               mobile,
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
            "candidate_Name": row[2],
            "email": row[3],
            "mobile": row[4],
            "skills": row[5],
            "match_score": row[6],
            "upload_time": row[7]
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
               candidate_name,
               email,
               mobile,
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
        "candidate_name": row[2],
        "email": row[3],
        "mobile": row[4],
        "skills": row[5],
        "matched_score": row[6],
        "upload_time": row[7]
    }
@app.post("/upload")
async def upload_resume( #file: UploadFile = File(...)):
            request:Request,
            file: UploadFile = File(...)
):

    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    details = extract_resume_details(file_path)

    text = details["text"]

    candidate_name = details["candidate_name"]

    email = details["email"]

    mobile = details["mobile"]

    matched_skills = details["matched_skills"]

    job_matches = details["job_matches"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    skills_string = ",".join(matched_skills)

    highest_match_score = max(
        job["match_score"]
        for job in job_matches
    )

    cursor.execute(
        """
        INSERT INTO resumes
        (
            filename,
            candidate_name,
            email,
            mobile,
            skills,
            match_score
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            file.filename,
            candidate_name,
            email,
            mobile,
            skills_string,
            highest_match_score
        )
    )

    conn.commit()
    conn.close()

    return templates.TemplateResponse(
    "result.html",
{
         "request":request,
        "filename": file.filename,
        "candidate_name": candidate_name,
        "email": email,
        "mobile": mobile,
        "skills": matched_skills,
        "job_matches": job_matches
    }
)
