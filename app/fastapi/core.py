from typing import List
from app.fastapi.scheme import *
from app.fastapi import models
from app.errors import *
from sqlalchemy.orm import Session


def get_nutrition(db: Session, food_name: str) -> Nutrition:
    nutrition = db.query(models.Nutrition).filter(models.Nutrition.name == food_name).first()
    if nutrition is None:
        raise FoodNotFoundError
    return Nutrition(**nutrition.__dict__)


def add_nutrition(db: Session, nutrition: NutritionBase) -> Nutrition:
    if nutrition.serving_size <= 0 or nutrition.calories_per_100_g <= 0:
        raise NegativeAmountError

    nutrition = Nutrition(**nutrition.dict())
    db_nutrition = models.Nutrition(**nutrition.dict())
    db.add(db_nutrition)
    return nutrition


def get_compound_nutrition_by_calories(db: Session, food_name: str, calories: float) -> CompoundNutrition:
    nutrition = get_nutrition(db, food_name)
    return CompoundNutrition(name=food_name, calories=calories, weight=calories / nutrition.calories_per_100_g * 100)


def get_compound_nutrition_by_weight(db: Session, food_name: str, weight_g: float) -> CompoundNutrition:
    nutrition = get_nutrition(db, food_name)
    return CompoundNutrition(name=food_name, calories=nutrition.calories_per_100_g / 100 * weight_g, weight=weight_g)


def get_compound_nutrition_by_servings(db: Session, food_name: str, servings: float) -> CompoundNutrition:
    nutrition = get_nutrition(db, food_name)
    return CompoundNutrition(name=food_name, calories=nutrition.calories_per_serving * servings, weight=nutrition.serving_size*servings)


def get_compound_nutrition(*food_components: List[CompoundNutrition]) -> CompoundNutrition:
    if not food_components:
        return CompoundNutrition()

    nutrition = food_components[0].copy()
    for food in food_components[1:]:
        nutrition.name += f", {food.name}"
        nutrition.weight += food.weight
        nutrition.calories += food.calories
    return nutrition
