from fastapi import FastAPI, status, HTTPException
from .scheme import NutritionBase, Nutrition, nutrition_db

app = FastAPI()


@app.get("/nutrition/{food_name}", response_model=Nutrition)
def get_nutrition(food_name: str):
    if food_name not in nutrition_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Food not found")

    return nutrition_db[food_name]


@app.post("/nutrition", response_model=Nutrition, status_code=status.HTTP_201_CREATED)
def add_nutrition(nutrition: NutritionBase):
    if nutrition.serving_size <= 0 or nutrition.calories_per_100_g <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Serving size and calories amount must be positive numbers")

    nutrition = Nutrition(**nutrition.dict())
    nutrition_db[nutrition.name] = nutrition
    return nutrition
