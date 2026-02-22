
SYSTEM_PROMPT = """
You are an expert resume parsing engine.

Your task:
Extract structured information from resume text and return ONLY valid JSON.

Rules:
- Output MUST be valid JSON.
- Do NOT include explanations.
- Do NOT wrap in markdown.
- If a field is missing, return null.
- Keep arrays even if empty.
"""


def build_user_prompt(resume_text: str) -> str:
    return f"""
Extract the following fields from the resume below:

Return JSON in this exact format:

{{
  "full_name": string | null,
  "email": string | null,
  "phone": string | null,
  "linkedin": string | null,
  "skills": string[],
  "education": [
    {{
      "degree": string | null,
      "institution": string | null,
      "start_year": string | null,
      "end_year": string | null
    }}
  ],
  "experience": [
    {{
      "job_title": string | null,
      "company": string | null,
      "start_date": string | null,
      "end_date": string | null,
      "description": string | null
    }}
  ]
}}

Resume Text:
----------------
{resume_text}
"""