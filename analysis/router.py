from fastapi import APIRouter
from resumes.database_service import get_resume_by_id
from job_descriptions.database_service import get_job_description_by_id
from resumes.models import Resume
from job_descriptions.models import JobDescription
from analysis.llm_service import analyse_resume_and_jd
from analysis.models import Analysis
from analysis.schemas import AnalysisRequest
from analysis.database_service import save_analysis, get_analysis_by_id, get_existing_analysis


router = APIRouter(tags=["Analysis"])


@router.post("/analysis", response_model=Analysis)
def create_analysis(analysis_request: AnalysisRequest, analyse_again=False) -> Analysis:
    resume_id = analysis_request.resume_id
    job_description_id = analysis_request.job_description_id

    existing_analysis = get_existing_analysis(resume_id, job_description_id)
    if existing_analysis and analyse_again == False:
        return get_analysis_by_id(analysis_id=existing_analysis.id)

    resume: Resume = get_resume_by_id(resume_id)
    jd: JobDescription = get_job_description_by_id(job_description_id)

    analysis_result = analyse_resume_and_jd(
        resume_dict=resume.parsed_json_text, jd_dict=jd.parsed_json_text
    )

    analysis = save_analysis(resume_id=resume_id, job_description_id=job_description_id, analysis_result=analysis_result)
    analysis = get_analysis_by_id(analysis_id=analysis.id)
    return analysis


@router.get("/analysis/{analysis_id}", response_model=Analysis)
def get_analysis(analysis_id: int) -> Analysis:
    analysis = get_analysis_by_id(analysis_id)
    return analysis