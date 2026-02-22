from pydantic import BaseModel

class ResumeUploadResponse(BaseModel):
    message: str
    original_filename: str
    clean_filename: str