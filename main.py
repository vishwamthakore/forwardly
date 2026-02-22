from fastapi import FastAPI
from datetime import datetime, timezone
from items.schemas import HealthStatus
from items.router import router as item_router
from resumes.router import router as resume_router
from config.handlers import add_all_exception_handlers
from services.database import init_db
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # create tables once
    yield


app = FastAPI(lifespan=lifespan)
add_all_exception_handlers(app=app)


@app.get("/health", response_model=HealthStatus)
def health():
    return HealthStatus(status="healthy", timestamp=datetime.now(tz=timezone.utc))


app.include_router(item_router)
app.include_router(resume_router)
