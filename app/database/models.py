from sqlalchemy import Column, String, Float
from sqlalchemy.orm import declarative_base

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
