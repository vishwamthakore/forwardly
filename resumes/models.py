from typing import Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field

def utc_now():
    return datetime.now(timezone.utc)

class Resume(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    original_filename: str
    saved_filename: str

    extracted_text: Optional[str] = None
    parsed_json_text: Optional[str] = None
    is_parsed: bool = False

    created_at: datetime = Field(default_factory=utc_now)
