import json
from services.database import get_session
from analysis.models import Analysis
from config.exceptions import NotFoundException
from analysis.schemas import AnalysisResult
from sqlmodel import select

def save_analysis(resume_id: int, job_description_id: int, analysis_result: AnalysisResult) -> Analysis:
    session = get_session()

    analysis_json_text = json.dumps(analysis_result.model_dump())
    analysis = Analysis(
        resume_id=resume_id,
        job_description_id=job_description_id,
        analysis_json_text=analysis_json_text
    )

    session.add(analysis)
    session.commit()
    session.refresh(analysis)
    session.close()

    return analysis


def get_analysis_by_id(analysis_id: int):
    session = get_session()

    analysis = session.get(Analysis, analysis_id)

    if not analysis:
        session.close()
        raise NotFoundException(message=f"Analysis with id {analysis} not found")

    # Convert parsed_json_text -> dict
    if analysis.analysis_json_text:
        try:
            analysis.analysis_json_text = json.loads(analysis.analysis_json_text)
        except json.JSONDecodeError:
            analysis.analysis_json_text = None

    session.close()
    return analysis


def get_existing_analysis(resume_id: int, jd_id: int) -> Analysis | None:
    session = get_session()

    statement = (
        select(Analysis)
        .where(Analysis.resume_id == resume_id)
        .where(Analysis.job_description_id == jd_id)
        .limit(1)
    )

    result = session.exec(statement).first()

    session.close()
    return result