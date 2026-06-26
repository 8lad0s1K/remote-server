from fastapi import FastAPI

from database import Base, engine
from api.auth import router as auth_router
from api.request import router as request_router
from api.programs import router as programs_router
from api.admin import router as admin_router  # <-- МИ ДОДАЛИ ЦЕЙ ІМПОРТ

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="REMOTE SERVER",
    version="1.0"
)

app.include_router(auth_router)
app.include_router(request_router)
app.include_router(programs_router)
app.include_router(admin_router)  # <-- ПІДКЛЮЧЕННЯ АДМІНКИ


@app.get("/")
def root():
    return {
        "status": "online",
        "project": "REMOTE SERVER"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }