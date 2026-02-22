from pydantic import BaseModel

class JobDescriptionInput(BaseModel):
    text: str