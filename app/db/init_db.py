from app.db.session import engine
from app.models.base import Base

# Import models so SQLAlchemy "registers" them under Base.metadata
from app.models.application import Application  # noqa: F401
from app.models.user import User  # noqa: F401

def init_db() -> None:
    Base.metadata.create_all(bind=engine)
