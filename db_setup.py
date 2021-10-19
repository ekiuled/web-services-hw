from app.strawberry.database import nutrition_db
from app.fastapi.database import SessionLocal, engine
from app.fastapi import models

models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

for nutrition in nutrition_db.values():
    name = nutrition["name"]
    serving_size = nutrition["serving_size"]
    calories_per_100_g = nutrition["calories_per_100_g"]
    calories_per_serving = nutrition["calories_per_serving"]

    db_nutrition = models.Nutrition(name=name,
                                    serving_size=serving_size,
                                    calories_per_100_g=calories_per_100_g,
                                    calories_per_serving=calories_per_serving)
    db.add(db_nutrition)

db.commit()
db.close()
