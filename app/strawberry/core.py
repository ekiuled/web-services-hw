from typing import List
from app.strawberry.scheme import *
from app.database import *
from app.errors import *


def get_all_recipes() -> List[Recipe]:
    return [_dict_to_recipe(recipe) for recipe in recipe_db.values()]


def get_recipe(name: str) -> Recipe:
    if name not in recipe_db:
        raise FoodNotFoundError

    return _dict_to_recipe(recipe_db[name])


def _dict_to_recipe(recipe: dict) -> Recipe:
    ingredients = []
    recipe_nutrition = Nutrition(calories=0, fats=0, carbs=0, protein=0)

    for ingredient in recipe["ingredients"]:
        name = ingredient["name"]
        amount = ingredient["amount"]

        if amount <= 0:
            raise NegativeAmountError
        if name not in nutrition_db:
            raise FoodNotFoundError

        def scale(x, amount): return x / 100 * amount

        info = nutrition_db[name]
        nutrition = Nutrition(calories=scale(info["calories_per_100_g"], amount),
                              fats=scale(info["fats_per_100_g"], amount),
                              carbs=scale(info["carbs_per_100_g"], amount),
                              protein=scale(info["protein_per_100_g"], amount))

        recipe_nutrition.calories += nutrition.calories
        recipe_nutrition.fats += nutrition.fats
        recipe_nutrition.carbs += nutrition.carbs
        recipe_nutrition.protein += nutrition.protein

        ingredients.append(Ingredient(name, amount, nutrition))

    return Recipe(name=recipe["name"],
                  ingredients=ingredients,
                  steps=recipe["steps"],
                  nutrition=recipe_nutrition)
