import pytest
from app.fastapi.database import SessionLocal
from app.fastapi.models import Nutrition


@pytest.fixture
def db_session():
    session = SessionLocal()
    yield session
    session.rollback()
    session.close()


@pytest.fixture
def db_get(db_session):
    def get(name):
        db_session.flush()
        return db_session.query(Nutrition).filter(Nutrition.name == name).first()

    return get
