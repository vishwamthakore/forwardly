from typing import Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field

def utc_now():
    return datetime.now(timezone.utc)

class JobDescription(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = None
    raw_text: str
    parsed_json_text: Optional[str] = None

    created_at: datetime = Field(default_factory=utc_now)