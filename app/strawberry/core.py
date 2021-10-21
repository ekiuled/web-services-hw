from typing import List
from sqlalchemy.orm import Session
from app.strawberry.scheme import *
from app.strawberry.recipe_generator import generate
from app.database import crud
from app.database.models import Recipe as DBRecipe
from app.errors import *


def get_all_recipes(db: Session) -> List[Recipe]:
    return [_db_to_recipe(db, recipe) for recipe in crud.get_recipes(db)]


def get_recipe(db: Session, name: str) -> Recipe:
    recipe = crud.get_recipe(db, name)
    if recipe is None:
        raise FoodNotFoundError(name)

    return _db_to_recipe(db, recipe)


def generate_recipe(db: Session, name: str, ingredients: List[str]) -> None:
    if crud.get_recipe(db, name) is not None:
        raise DuplicateRecipe(name)
    missing_ingredients = [ingredient
                           for ingredient in ingredients
                           if crud.get_nutrition(db, ingredient) is None]
    if missing_ingredients:
        raise FoodsNotFoundError(missing_ingredients)

    generate.delay(name, ingredients)


def _db_to_recipe(db: Session, recipe: DBRecipe) -> Recipe:
    ingredients = []
    recipe_nutrition = Nutrition(calories=0, fats=0, carbs=0, protein=0)

    for ingredient in recipe.ingredients:
        amount = ingredient.amount
        if amount <= 0:
            raise NegativeAmountError

        info = ingredient.nutrition

        def scale(x, amount): return x / 100 * amount

        nutrition = Nutrition(calories=scale(info.calories_per_100_g, amount),
                              fats=scale(info.fats_per_100_g, amount),
                              carbs=scale(info.carbs_per_100_g, amount),
                              protein=scale(info.protein_per_100_g, amount))

        recipe_nutrition.calories += nutrition.calories
        recipe_nutrition.fats += nutrition.fats
        recipe_nutrition.carbs += nutrition.carbs
        recipe_nutrition.protein += nutrition.protein

        ingredients.append(Ingredient(info.name, amount, nutrition))

    steps = list(map(lambda step: step.step, recipe.steps))

    return Recipe(name=recipe.name,
                  ingredients=ingredients,
                  steps=steps,
                  nutrition=recipe_nutrition)
