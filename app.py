from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from fastapi import FastAPI, UploadFile, File
from jobs import jobs
from docx import Document
from pypdf import PdfReader
from fastapi.responses import FileResponse
from fastapi.responses import RedirectResponse
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
@app.get("/dashboard")
def dashboard(
    request: Request,
    search: str = ""
):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # -------------------------
    # Dashboard Statistics
    # -------------------------

    cursor.execute("SELECT COUNT(*) FROM resumes")
    total_resumes = cursor.fetchone()[0]

    cursor.execute("SELECT MAX(match_score) FROM resumes")
    highest_score = cursor.fetchone()[0] or 0

    cursor.execute("SELECT AVG(match_score) FROM resumes")
    average_score = cursor.fetchone()[0] or 0

    # -------------------------
    # Chart
    # -------------------------

    cursor.execute("""
        SELECT candidate_name, match_score
        FROM resumes
        ORDER BY upload_time DESC
        LIMIT 5
    """)

    chart_data = cursor.fetchall()

    labels = [row[0] for row in chart_data]
    scores = [row[1] for row in chart_data]

    # -------------------------
    # Top Candidates
    # -------------------------

    cursor.execute("""
        SELECT candidate_name,
               email,
               match_score
        FROM resumes
        ORDER BY match_score DESC
        LIMIT 5
    """)

    top_candidates = cursor.fetchall()

    # -------------------------
    # Resume Search
    # -------------------------

    search_term = f"%{search}%"

    cursor.execute("""
        SELECT
             id,
            candidate_name,
            filename,
            match_score,
            upload_time,
            email,
            mobile
      FROM resumes
     WHERE
        candidate_name LIKE ?
        OR email LIKE ?
        OR mobile LIKE ?
        OR CAST(match_score AS TEXT) LIKE ?
   ORDER BY upload_time DESC
   """,
   (
      search_term,
      search_term,
      search_term,
      search_term
  ))

    recent_uploads = cursor.fetchall()

    conn.close()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "total_resumes": total_resumes,
            "highest_score": highest_score,
            "average_score": round(average_score, 2),
            "labels": labels,
            "scores": scores,
            "top_candidates": top_candidates,
            "recent_uploads": recent_uploads,
            "search": search
        }
    )
@app.get("/history")
def history(request: Request):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            filename,
            candidate_name,
            email,
            match_score,
            upload_time
        FROM resumes
        ORDER BY id DESC
    """)

    resumes = cursor.fetchall()

    conn.close()

    return templates.TemplateResponse(
        "history.html",
        {
            "request": request,
            "resumes": resumes
        }
    )
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
        # Convert skills list into string
    skills_string = ",".join(matched_skills)

    # ---------------------------------
    # Duplicate Resume Detection
    # ---------------------------------

    existing_resume = None

    # Check by Email
    if email:

        cursor.execute("""
            SELECT id, filename
            FROM resumes
            WHERE email = ?
        """, (email,))

        existing_resume = cursor.fetchone()

    # Check by Mobile if Email not available
    elif mobile:

        cursor.execute("""
            SELECT id, filename
            FROM resumes
            WHERE mobile = ?
        """, (mobile,))

        existing_resume = cursor.fetchone()

    # ---------------------------------
    # UPDATE Existing Resume
    # ---------------------------------

    if existing_resume:

        old_resume = os.path.join(UPLOAD_DIR, existing_resume[1])

        if os.path.exists(old_resume):
            os.remove(old_resume)

        cursor.execute("""
            UPDATE resumes
            SET
                filename = ?,
                candidate_name = ?,
                email = ?,
                mobile = ?,
                skills = ?,
                match_score = ?,
                upload_time = CURRENT_TIMESTAMP
            WHERE id = ?
        """,
        (
            file.filename,
            candidate_name,
            email,
            mobile,
            skills_string,
            highest_match_score,
            existing_resume[0]
        ))

    # ---------------------------------
    # INSERT New Resume
    # ---------------------------------

    else:

        cursor.execute("""
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
        ))

    conn.commit()
    conn.close()

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "filename": file.filename,
            "candidate_name": candidate_name,
            "email": email,
            "mobile": mobile,
            "skills": matched_skills,
            "job_matches": job_matches
        }
    )
@app.get("/download/{filename}")
def download_resume(filename: str):

    file_path = f"uploads/{filename}"

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream"
    )
from fastapi.responses import RedirectResponse

@app.get("/delete/{resume_id}")
def delete_resume(resume_id: int):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Find filename
    cursor.execute(
        "SELECT filename FROM resumes WHERE id=?",
        (resume_id,)
    )

    row = cursor.fetchone()

    if row:

        filepath = os.path.join(UPLOAD_DIR, row[0])

        if os.path.exists(filepath):
            os.remove(filepath)

        cursor.execute(
            "DELETE FROM resumes WHERE id=?",
            (resume_id,)
        )

        conn.commit()

    conn.close()

    return RedirectResponse(
        url="/dashboard",
        status_code=303
    )
