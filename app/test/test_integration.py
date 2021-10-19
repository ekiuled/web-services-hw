import pytest
from app.fastapi.core import *


def test_get_after_add(db_session):
    name = "new food"
    calories_per_100_g = 100
    nutrition_in = NutritionBase(name=name, calories_per_100_g=calories_per_100_g)

    add_nutrition(db_session, nutrition_in)
    db_session.flush()
    nutrition_out = get_nutrition(db_session, name)

    assert nutrition_in.name == nutrition_out.name
    assert nutrition_in.serving_size == nutrition_out.serving_size
    assert nutrition_in.calories_per_100_g == nutrition_out.calories_per_100_g


def test_get_after_unsuccessfull_add(db_session):
    name = "bad food"
    nutrition_in = NutritionBase(name="bad food", calories_per_100_g=-5)

    with pytest.raises(NegativeAmountError):
        add_nutrition(db_session, nutrition_in)
    db_session.flush()
    with pytest.raises(FoodNotFoundError):
        get_nutrition(db_session, name)


def test_compound_nutrition(db_session):
    avocado = get_compound_nutrition_by_weight(db_session, "avocado", 100)
    toast = get_compound_nutrition_by_calories(db_session, "toast", 100)
    coffee = get_compound_nutrition_by_calories(db_session, "coffee", 2)
    compound = get_compound_nutrition(avocado, toast, coffee)

    assert compound.name == f"{avocado.name}, {toast.name}, {coffee.name}"
    assert compound.calories == avocado.calories + toast.calories + coffee.calories
    assert compound.weight == avocado.weight + toast.weight + coffee.weight
