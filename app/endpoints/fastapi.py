from typing import List
from fastapi import FastAPI, status, HTTPException, Depends
from sqlalchemy.orm import Session
from app.fastapi.database import SessionLocal, engine
from app.fastapi.scheme import *
from app.fastapi import core, models
from app.errors import *

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/nutrition/{food_name}", response_model=Nutrition)
def get_nutrition(food_name: str, db: Session = Depends(get_db)):
    try:
        return core.get_nutrition(db, food_name)
    except FoodNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=e.message)


@app.post("/nutrition", response_model=Nutrition, status_code=status.HTTP_201_CREATED)
def add_nutrition(nutrition: NutritionBase, db: Session = Depends(get_db)):
    try:
        nutrition = core.add_nutrition(db, nutrition)
        db.commit()
        return nutrition
    except NegativeAmountError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=e.message)


@app.get("/nutrition/{food_name}/calories", response_model=CompoundNutrition)
def get_nutrition_by_calories(food_name: str, calories: float, db: Session = Depends(get_db)):
    try:
        return core.get_compound_nutrition_by_calories(db, food_name, calories)
    except FoodNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=e.message)


@app.get("/nutrition/{food_name}/weight", response_model=CompoundNutrition)
def get_nutrition_by_weight(food_name: str, weight: float, db: Session = Depends(get_db)):
    try:
        return core.get_compound_nutrition_by_weight(db, food_name, weight)
    except FoodNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=e.message)


@app.get("/nutrition/{food_name}/servings", response_model=CompoundNutrition)
def get_nutrition_by_servings(food_name: str, servings: float, db: Session = Depends(get_db)):
    try:
        return core.get_compound_nutrition_by_servings(db, food_name, servings)
    except FoodNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=e.message)


@app.get("/compound-nutrition", response_model=CompoundNutrition)
def get_compound_nutrition(food_components: List[CompoundNutrition]):
    return core.get_compound_nutrition(*food_components)
