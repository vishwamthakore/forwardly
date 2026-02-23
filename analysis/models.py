from typing import Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field

def utc_now():
    return datetime.now(timezone.utc)

class Analysis(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    resume_id: int
    job_description_id: int

    analysis_json_text: str
    
    created_at: datetime = Field(default_factory=utc_now)