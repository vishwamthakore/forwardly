SYSTEM_PROMPT = """
You are an expert information extraction system.

Extract structured information from a job description text.

Return ONLY valid JSON.
Do not include explanation.
Do not include markdown.
If a field is not present, return null.
Do not hallucinate missing information.
Be precise and conservative.
"""


def build_user_prompt(jd_text: str) -> dict:

    user_prompt = f"""
Extract structured data from the following job description.

Return strictly in this JSON format:

{{
  "company_name": string | null,
  "job_title": string,
  "location": string | null,
  "employment_type": string | null,
  "experience_required": {{
    "min_years": number | null,
    "max_years": number | null
  }},
  "required_skills": string[],
  "preferred_skills": string[],
  "education_requirements": string | null,
  "responsibilities": string[],
  "tools_technologies": string[],
  "soft_skills": string[],
  "domain": string | null,
  "seniority_level": string | null
}}

Job Description:
----------------
{jd_text}
"""
    return user_prompt
