from .database import nutrition_db
from .scheme import NutritionBase, Nutrition
from .errors import *


def get_nutrition(food_name: str):
    if food_name not in nutrition_db:
        raise FoodNotFoundError

    return nutrition_db[food_name]


def add_nutrition(nutrition: NutritionBase):
    if nutrition.serving_size <= 0 or nutrition.calories_per_100_g <= 0:
        raise NegativeAmountError

    nutrition = Nutrition(**nutrition.dict())
    nutrition_db[nutrition.name] = nutrition
    return nutrition
