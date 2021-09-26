from typing import List
from fastapi import FastAPI, status, HTTPException
from .scheme import *
from . import core
from .errors import *

app = FastAPI()


@app.get("/nutrition/{food_name}", response_model=Nutrition)
def get_nutrition(food_name: str):
    try:
        return core.get_nutrition(food_name)
    except FoodNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=e.message)


@app.post("/nutrition", response_model=Nutrition, status_code=status.HTTP_201_CREATED)
def add_nutrition(nutrition: NutritionBase):
    try:
        return core.add_nutrition(nutrition)
    except NegativeAmountError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=e.message)


@app.get("/nutrition/{food_name}/calories", response_model=CompoundNutrition)
def get_nutrition_by_calories(food_name: str, calories: float):
    try:
        return core.get_compound_nutrition_by_calories(food_name, calories)
    except FoodNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=e.message)


@app.get("/nutrition/{food_name}/weight", response_model=CompoundNutrition)
def get_nutrition_by_weight(food_name: str, weight: float):
    try:
        return core.get_compound_nutrition_by_weight(food_name, weight)
    except FoodNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=e.message)


@app.get("/nutrition/{food_name}/servings", response_model=CompoundNutrition)
def get_nutrition_by_servings(food_name: str, servings: float):
    try:
        return core.get_compound_nutrition_by_servings(food_name, servings)
    except FoodNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=e.message)


@app.get("/compound-nutrition", response_model=CompoundNutrition)
def get_compound_nutrition(food_components: List[CompoundNutrition]):
    return core.get_compound_nutrition(*food_components)
