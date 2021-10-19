from typing import Union, List
from sqlalchemy.orm import Session
from app.database.models import *


def get_nutrition(db: Session, name: str) -> Union[Nutrition, None]:
    return db.query(Nutrition).filter(Nutrition.name == name).first()


def add_nutrition(db: Session, nutrition: Nutrition) -> None:
    db.add(nutrition)


def get_recipe(db: Session, name: str) -> Union[Recipe, None]:
    return db.query(Recipe).filter(Recipe.name == name).first()


def get_recipes(db: Session) -> List[Recipe]:
    return db.query(Recipe).all()


def add_recipe(db: Session, recipe: dict) -> None:
    db_recipe = Recipe(name=recipe["name"])

    for step in recipe["steps"]:
        db_step = Step(step=step)
        db_recipe.steps.append(db_step)

    for ingredient in recipe["ingredients"]:
        db_ingredient = Ingredient(amount=ingredient["amount"],
                                   nutrition=get_nutrition(db, ingredient["name"]))
        db_recipe.ingredients.append(db_ingredient)

    db.add(db_recipe)
