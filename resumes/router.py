from fastapi import APIRouter
from fastapi import UploadFile, File, HTTPException

from resumes.schemas import ResumeUploadResponse
from resumes.text_service import get_clean_text_from_pdf
from resumes.llm_service import parse_resume_with_llm
from resumes.utils import upload_pdf_file
from resumes.utils import UPLOAD_DIR
from resumes.database_service import save_resume, get_resume_by_id, save_extracted_text
from resumes.models import Resume

router = APIRouter(tags=["Resumes"])


@router.post("/resume", response_model=Resume)
def create_resume(file: UploadFile = File()):
    saved_filename = upload_pdf_file(file=file)
    resume: Resume = save_resume(
        original_filename=file.filename, saved_filename=saved_filename
    )
    return resume


@router.get("/resume/{resume_id}", response_model=Resume)
def get_resume(resume_id: int, parse_again: bool = False) -> Resume:    
    resume: Resume = get_resume_by_id(resume_id)

    if resume.is_parsed and parse_again==False:
        return resume

    try:
        text = get_clean_text_from_pdf(filename=resume.saved_filename)
    except ValueError as e:
        raise HTTPException(422, str(e))

    try:
        structured = parse_resume_with_llm(text)
    except ValueError as e:
        raise HTTPException(500, str(e))
    
    save_extracted_text(resume_id=resume_id, extracted_text=text, parsed_json=structured)
    resume: Resume = get_resume_by_id(resume_id)
    return resume
