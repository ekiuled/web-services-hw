import pytest
from app.database.database import DB
from app.database.models import Nutrition


@pytest.fixture
def db_session():
    session = DB()
    yield session
    session.rollback()


@pytest.fixture
def db_get(db_session):
    def get(name):
        db_session.flush()
        return db_session.query(Nutrition).filter(Nutrition.name == name).first()

    return get
