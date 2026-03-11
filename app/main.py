from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.applications import router as applications_router
from app.db.init_db import init_db

app = FastAPI(title="Job Intelligence API", version="0.4.0")


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(auth_router)
app.include_router(applications_router)