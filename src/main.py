from typing import Optional

from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, validator

app = FastAPI()


class NutritionBase(BaseModel):
    name: str
    serving_size: Optional[float] = 100
    calories_per_100_g: float


class Nutrition(NutritionBase):
    calories_per_serving: float = None

    @validator('calories_per_serving', always=True)
    def set_calories_per_serving(cls, v, values) -> float:
        return values["calories_per_100_g"] / 100 * values["serving_size"]


nutrition_db = {
    "avocado": {"name": "avocado", "serving_size": 201, "calories_per_100_g": 160.2, "calories_per_serving": 322},
    "coffee": {"name": "coffee", "serving_size": 237, "calories_per_100_g": 0.84, "calories_per_serving": 2},
    "toast": {"name": "toast", "serving_size": 50, "calories_per_100_g": 300, "calories_per_serving": 150}
}


@app.get("/nutrition/food/{food_name}", response_model=Nutrition)
def get_nutrition(food_name: str):
    if food_name not in nutrition_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Food not found")

    return nutrition_db[food_name]


@app.post("/nutrition/add", response_model=Nutrition, status_code=status.HTTP_201_CREATED)
def add_nutrition(nutrition: NutritionBase):
    if nutrition.serving_size <= 0 or nutrition.calories_per_100_g <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Serving size and calories amount must be positive numbers")

    nutrition = Nutrition(**nutrition.dict())
    nutrition_db[nutrition.name] = nutrition
    return nutrition
