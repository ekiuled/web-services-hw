from typing import List
import strawberry


@strawberry.type
class Nutrition:
    calories: float
    fats: float
    carbs: float
    protein: float


@strawberry.type
class Ingredient:
    name: str
    amount: float
    nutrition: Nutrition


@strawberry.type
class Recipe:
    name: str
    ingredients: List[Ingredient]
    steps: List[str]
    nutrition: Nutrition
