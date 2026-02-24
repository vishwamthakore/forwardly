# app/repositories/resume_repository.py
import json
from services.database import get_session
from resumes.models import Resume
from config.exceptions import NotFoundException
from sqlmodel import select


def save_resume(original_filename: str, saved_filename: str) -> Resume:
    session = get_session()

    resume = Resume(
        original_filename=original_filename,
        saved_filename=saved_filename
    )

    session.add(resume)
    session.commit()
    session.refresh(resume)
    session.close()

    return resume


def save_extracted_text(resume_id: int, extracted_text: str, parsed_json: dict):
    session = get_session()

    resume = session.get(Resume, resume_id)
    if not resume:
        session.close()
        return None

    parsed_json_text = json.dumps(parsed_json)

    resume.extracted_text = extracted_text
    resume.parsed_json_text = parsed_json_text
    resume.is_parsed = True

    session.add(resume)
    session.commit()
    session.close()

    return resume

            
def get_resume_by_id(resume_id: int) -> Resume:
    session = get_session()

    resume = session.get(Resume, resume_id)

    if not resume:
        session.close()
        raise NotFoundException(message=f"Resume with id {resume_id} not found")

    # Convert parsed_json_text -> dict
    if resume.parsed_json_text:
        try:
            resume.parsed_json_text = json.loads(resume.parsed_json_text)
        except json.JSONDecodeError:
            resume.parsed_json_text = None

    session.close()
    return resume


def list_resumes(limit=5):
    session = get_session()

    statement = select(
        Resume.id,
        Resume.original_filename,
        Resume.saved_filename,
        Resume.is_parsed,
        Resume.created_at
    ).order_by(Resume.created_at.desc()).limit(limit)

    results = session.exec(statement).mappings().all()

    session.close()

    # Already dict-like → just convert to normal dict
    return [dict(r) for r in results]