from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from resumes.database_service import list_resumes
from analysis.router import create_analysis
from analysis.schemas import AnalysisRequest
from resumes.database_service import get_resume_by_id
from job_descriptions.database_service import get_job_description_by_id, list_job_descriptions

# we will call your existing database/service functions
# from resumes.database_service import get_all_resumes

router = APIRouter(tags=["Web UI"])

# Tell Jinja where templates live
templates = Jinja2Templates(directory="webui/templates")


@router.get("/ui/resumes", response_class=HTMLResponse)
def resumes_page(request: Request, limit=10):
    """
    Human page:
    Shows list of resumes.
    """

    # calling backend service, NOT HTTP API
    resumes = list_resumes(limit=limit)

    return templates.TemplateResponse(
        "resumes.html",
        context={
            "request": request,  # required by Jinja/FastAPI
            "resumes": resumes,
            "current_step": "resume",
        },
    )


@router.get("/ui/job-description/{resume_id}", response_class=HTMLResponse)
def job_descriptions_page(request: Request, resume_id : int, limit=10):
    # calling backend service, NOT HTTP API
    job_descriptions = list_job_descriptions(limit=limit)

    return templates.TemplateResponse(
        "job-descriptions.html",
        context={
            "request": request,  # required by Jinja/FastAPI
            "job_descriptions": job_descriptions,
            "current_step": "job_description",
            "resume_id": resume_id
        },
    )



@router.get("/ui/analysis/{resume_id}/{job_description_id}", response_class=HTMLResponse)
def analysis_page(request: Request, resume_id: int, job_description_id: int):
    """
    Shows analysis based on resume_id and job_description_id
    """
    try: 
        analysis_request = AnalysisRequest(resume_id=resume_id, job_description_id=job_description_id)
        analysis = create_analysis(analysis_request=analysis_request)
        resume = get_resume_by_id(resume_id)
        job_description = get_job_description_by_id(job_description_id)

        analysis_json = analysis.analysis_json_text

        print(analysis)
    
    except Exception as e:
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "message": str(e),
                "status_code": 404
            },
            status_code=404
        )

    return templates.TemplateResponse(
        "analysis.html",
        context={
            "request": request,
            "resume": resume,
            "job_description": job_description, 
            "analysis": analysis,
            "analysis_data": analysis_json,
            "current_step": "analysis"
        }
    )

