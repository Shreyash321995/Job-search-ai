from fastapi import APIRouter
from fastapi import Request
from fastapi import Form
from fastapi.templating import Jinja2Templates

from ai.resume_analysis import (
    get_all_resumes,
    analyze_resume
)

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/interview")
async def interview_page(request: Request):

    resumes = get_all_resumes()

    return templates.TemplateResponse(
        "interview.html",
        {
            "request": request,
            "resumes": resumes,
            "analysis": None
        }
    )


@router.post("/interview")
async def analyze_resume_page(
    request: Request,
    resume_id: int = Form(...)
):

    resumes = get_all_resumes()

    try:
        analysis = analyze_resume(resume_id)

        print("=" * 50)
        print("Resume ID =", resume_id)
        print("Analysis =", analysis)
        print("=" * 50)

    except Exception as e:
        print("Interview Analysis Error:", e)

        analysis = {
            "error": str(e)
        }

        print("AI Response Length:", len(analysis.get("ai_response", "")))

    return templates.TemplateResponse(
        "interview.html",
        {
            "request": request,
            "resumes": resumes,
            "analysis": analysis
        }
    )
