import json
from services.database import get_session
from job_descriptions.models import JobDescription
from config.exceptions import NotFoundException
from sqlmodel import select

def save_job_description(text: str, structured: dict, name: str) -> JobDescription:
    session = get_session()
    parsed_json_text = json.dumps(structured)

    job_description = JobDescription(
        name=name,
        raw_text=text,
        parsed_json_text=parsed_json_text
    )

    session.add(job_description)
    session.commit()
    session.refresh(job_description)
    session.close()
    return job_description



def get_job_description_by_id(id: int) -> JobDescription:
    session = get_session()

    job_description = session.get(JobDescription, id)

    if not job_description:
        session.close()
        raise NotFoundException(message=f"Resume with id {id} not found")

    # Convert parsed_json_text -> dict
    if job_description.parsed_json_text:
        try:
            job_description.parsed_json_text = json.loads(job_description.parsed_json_text)
        except json.JSONDecodeError:
            job_description.parsed_json_text = None

    session.close()
    return job_description 


def list_job_descriptions(limit=5):
    session = get_session()

    statement = select(
        JobDescription.id,
        JobDescription.name,
        JobDescription.created_at
    ).order_by(JobDescription.created_at.desc()).limit(limit)

    results = session.exec(statement).mappings().all()

    session.close()

    # Already dict-like → just convert to normal dict
    return [dict(r) for r in results]