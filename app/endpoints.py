from fastapi import FastAPI, status, HTTPException
from .scheme import NutritionBase, Nutrition
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
