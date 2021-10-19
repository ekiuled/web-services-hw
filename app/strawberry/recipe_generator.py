from typing import List
import time
import logging
from celery import Celery
from app.database.database import DB
from app.database.crud import add_recipe
from random import randint

logger = logging.getLogger(__name__)


app = Celery(broker="amqp://localhost:5672")
app.autodiscover_tasks()


@app.task
def generate(name: str, ingredients: List[str]) -> None:
    logger.info(f"Generating recipe {name}...")

    # Clever and heavy recipe generation
    time.sleep(3)
    recipe = {
        "name": name,
        "steps": ["Mix all ingredients"],
        "ingredients": [{"name": ingredient, "amount": randint(1, 1000)}
                        for ingredient in ingredients]
    }

    db = DB()
    add_recipe(db, recipe)
    db.commit()

    logger.info(f"Recipe {name} is generated: {recipe}")
