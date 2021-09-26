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
