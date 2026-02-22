from pydantic import BaseModel
from datetime import datetime


class HealthStatus(BaseModel):
    status: str = "healthy"
    timestamp: datetime | None = None


class ItemCreateRequest(BaseModel):
    name: str
    quantity: int = 0
    price: float = 0


class ItemResponse(BaseModel):
    id: int
    name: str
    quantity: int = 0
    price: float = 0
