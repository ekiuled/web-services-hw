from typing import Optional
from pydantic import BaseModel, validator


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
