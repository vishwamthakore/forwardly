from datetime import datetime
from pydantic import BaseModel

class ResumeUploadResponse(BaseModel):
    message: str
    original_filename: str
    clean_filename: str

class ResumeListItem(BaseModel):
    id: int
    original_filename: str
    saved_filename: str
    is_parsed: bool
    created_at: datetime