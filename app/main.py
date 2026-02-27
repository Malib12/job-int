from fastapi import HTTPException
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
from app.schemas.user import UserCreate, Token
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.init_db import init_db
from app.models.application import Application

app = FastAPI(title="Job Intelligence API", version="0.2.0")


@app.on_event("startup")
def on_startup() -> None:
    # Runs once when the API container starts
    init_db()


def get_db():
    """
    FastAPI dependency:
    - open a DB session for this request
    - yield it to the endpoint
    - always close it after the request finishes (even if there's an error)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/applications")
def create_application(
    company: str,
    role: str,
    status: str,
    db: Session = Depends(get_db),
):
    row = Application(company=company, role=role, status=status)
    db.add(row)
    db.commit()        # saves to Postgres
    db.refresh(row)    # pulls generated fields (like id) back from Postgres
    return {"id": row.id, "company": row.company, "role": row.role, "status": row.status}


@app.get("/applications")
def list_applications(db: Session = Depends(get_db)):
    rows = db.query(Application).all()
    return [{"id": r.id, "company": r.company, "role": r.role, "status": r.status} for r in rows]
@app.post("/auth/register")
def register(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == payload.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    user = User(username=payload.username, password_hash=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "username": user.username}


@app.post("/auth/login", response_model=Token)
def login(payload: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token(subject=user.username)
    return {"access_token": token, "token_type": "bearer"}