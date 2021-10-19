from typing import Union
from sqlalchemy.orm import Session
from app.database.models import Nutrition


def get(db: Session, name: str) -> Union[Nutrition, None]:
    return db.query(Nutrition).filter(Nutrition.name == name).first()


def add(db: Session, nutrition: Nutrition) -> None:
    db.add(nutrition)
