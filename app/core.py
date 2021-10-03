from typing import List
from app.database import nutrition_db
from app.scheme import *
from app.errors import *


def get_nutrition(food_name: str) -> dict:
    if food_name not in nutrition_db:
        raise FoodNotFoundError

    return nutrition_db[food_name]


def add_nutrition(nutrition: NutritionBase) -> Nutrition:
    if nutrition.serving_size <= 0 or nutrition.calories_per_100_g <= 0:
        raise NegativeAmountError

    nutrition = Nutrition(**nutrition.dict())
    nutrition_db[nutrition.name] = nutrition.dict()
    return nutrition


def get_compound_nutrition_by_calories(food_name: str, calories: float) -> CompoundNutrition:
    nutrition = get_nutrition(food_name)
    return CompoundNutrition(name=food_name, calories=calories, weight=calories / nutrition["calories_per_100_g"] * 100)


def get_compound_nutrition_by_weight(food_name: str, weight_g: float) -> CompoundNutrition:
    nutrition = get_nutrition(food_name)
    return CompoundNutrition(name=food_name, calories=nutrition["calories_per_100_g"] / 100 * weight_g, weight=weight_g)


def get_compound_nutrition_by_servings(food_name: str, servings: float) -> CompoundNutrition:
    nutrition = get_nutrition(food_name)
    return CompoundNutrition(name=food_name, calories=nutrition["calories_per_serving"] * servings, weight=nutrition["serving_size"]*servings)


def get_compound_nutrition(*food_components: List[CompoundNutrition]) -> CompoundNutrition:
    if not food_components:
        return CompoundNutrition()

    nutrition = food_components[0].copy()
    for food in food_components[1:]:
        nutrition.name += f", {food.name}"
        nutrition.weight += food.weight
        nutrition.calories += food.calories
    return nutrition
