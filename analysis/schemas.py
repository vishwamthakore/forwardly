from pydantic import BaseModel
from typing import List, Literal


class AnalysisRequest(BaseModel):
    resume_id: int
    job_description_id: int


class AnalysisResult(BaseModel):
    # Objective scoring
    matching_score: int
    required_skill_coverage: float

    strong_matching_skills: List[str]
    missing_required_skills: List[str]

    experience_match: Literal["underqualified", "good", "overqualified"]
    seniority_match: Literal["below", "good", "above"]
    education_match: Literal["yes", "no", "unknown"]

    # Explanation
    gap_summary: str

    # Actionable guidance
    priority_skills_to_learn: List[str]
    estimated_preparation_time: str  # e.g. "5-10 days"

    # Encouragement + realism
    overall_assessment: str
