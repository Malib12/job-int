from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.application import Application
from app.models.user import User
from app.schemas.application import ApplicationCreate, ApplicationRead

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("", response_model=ApplicationRead)
def create_application(
    payload: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    row = Application(
        user_id=current_user.id,
        company=payload.company,
        role=payload.role,
        status=payload.status,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.get("", response_model=list[ApplicationRead])
def list_applications(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Application)
        .filter(Application.user_id == current_user.id)
        .order_by(Application.id)
        .offset(offset)
        .limit(limit)
        .all()
    )