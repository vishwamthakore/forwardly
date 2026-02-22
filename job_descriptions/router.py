from fastapi import APIRouter
from fastapi import HTTPException
from job_descriptions.models import JobDescription
from job_descriptions.schemas import JobDescriptionInput
from job_descriptions.llm_service import parse_job_description_with_llm
from job_descriptions.text_service import generate_jd_name
from job_descriptions.database_service import save_job_description, get_job_description_by_id


router = APIRouter(tags=["Job Description"])

@router.post("/job-description/")
def create_job_description(job_description_input: JobDescriptionInput):

    text = job_description_input.text
    try:
        structured = parse_job_description_with_llm(text)
        print(structured)
    except ValueError as e:
        raise HTTPException(500, str(e))
    
    name = generate_jd_name(parsed_json=structured)
    job_description = save_job_description(text, structured, name)
    return job_description
    

@router.get("/job-description/{job_description_id}", response_model=JobDescription)
def get_resume(job_description_id: int) -> JobDescription:    
    job_description = get_job_description_by_id(job_description_id) 
    return job_description   
