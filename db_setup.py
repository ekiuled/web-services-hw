from app.database.dictionaries import nutrition_db
from app.database.database import SessionLocal, engine
from app.database import models

models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

for nutrition in nutrition_db.values():
    db_nutrition = models.Nutrition(**nutrition)
    db.add(db_nutrition)

db.commit()
db.close()
