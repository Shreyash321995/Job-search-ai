import sqlite3
from ai.prompts import build_interview_prompt
from ai.ollama_client import generate_response

#prompt = build_interview_prompt(resume)

#analysis["ai_response"] = generate_response(prompt)

DATABASE = "database.db"


def get_connection():
    return sqlite3.connect(DATABASE)


def get_all_resumes():
    """
    Returns all uploaded resumes
    """

    conn = get_connection()
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, filename
        FROM resumes
        ORDER BY id DESC
    """)

    resumes = cursor.fetchall()

    conn.close()

    return resumes


def get_resume_details(resume_id):
    """
    Returns complete resume details
    """

    conn = get_connection()
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM resumes
        WHERE id = ?
    """, (resume_id,))

    resume = cursor.fetchone()

    conn.close()

    return resume

def analyze_resume(resume_id):
    """
    Prepare resume information for Interview Assistant
    """

    resume = get_resume_details(resume_id)

    if not resume:
        return None

    print("=" * 50)
    print(dict(resume))
    print("=" * 50)

    # Build AI prompt
    prompt = build_interview_prompt(resume)
   # print("=" * 80)
   # print(prompt)
   # print("=" * 80)
    #print("Prompt length:", len(prompt))

    # Call Ollama
    ai_response = generate_response(prompt)

    analysis = {
        "id": resume["id"],
        "filename": resume["filename"],
        "candidate_name": resume["candidate_name"],
        "email": resume["email"],
        "mobile": resume["mobile"],
        "skills": resume["skills"],
        "match_score": resume["match_score"],
        "upload_time": resume["upload_time"],
        "experience": "Not Available",
        "ai_response": ai_response
    }

    return analysis
