from sqlalchemy import Column, ForeignKey, String, Float, Integer
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Nutrition(Base):
    __tablename__ = "nutrition"

    name = Column(String, primary_key=True, index=True)
    serving_size = Column(Float, default=100)
    calories_per_100_g = Column(Float)
    calories_per_serving = Column(Float)

    fats_per_100_g = Column(Float, default=0)
    carbs_per_100_g = Column(Float, default=0)
    protein_per_100_g = Column(Float, default=0)


class Recipe(Base):
    __tablename__ = "recipes"

    name = Column(String, primary_key=True, index=True)
    steps = relationship("Step")
    ingredients = relationship("Ingredient")


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True)
    recipe_name = Column(String, ForeignKey("recipes.name"))
    nutrition_name = Column(String, ForeignKey("nutrition.name"))
    amount = Column(Float)

    nutrition = relationship("Nutrition")


class Step(Base):
    __tablename__ = "steps"

    id = Column(Integer, primary_key=True)
    recipe_name = Column(String, ForeignKey("recipes.name"))
    step = Column(String)
