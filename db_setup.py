from app.database.dictionaries import *
from app.database.database import DB, engine
from app.database.models import *
from app.database.crud import *

Base.metadata.create_all(bind=engine)

db = DB()

for nutrition in nutrition_db.values():
    db_nutrition = Nutrition(**nutrition)
    db.add(db_nutrition)

db.commit()

for recipe in recipe_db.values():
    add_recipe(db, recipe)

db.commit()
