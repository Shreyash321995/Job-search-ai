def build_interview_prompt(resume):

    return f"""
You are an expert Senior DevOps interviewer.

Candidate Skills:
{resume["skills"]}

TASK:
Generate EXACTLY 10 interview questions.

RULES:
- Output ONLY the questions.
- Do NOT write headings.
- Do NOT write introductions.
- Do NOT write conclusions.
- Do NOT explain anything.
- Do NOT mention candidate strengths.
- Do NOT mention interview mistakes.
- Do NOT use markdown.
- Do NOT use bullet points.
- Number them from 1 to 10.
- Each question must be one sentence.
- Maximum 15 words per question.
- Stop immediately after question 10.
"""
