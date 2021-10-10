import pytest
from app.core import *


def test_get_after_add():
    name = "new food"
    calories_per_100_g = 100
    nutrition_in = NutritionBase(name=name, calories_per_100_g=calories_per_100_g)

    add_nutrition(nutrition_in)
    nutrition_out = get_nutrition(name)

    assert nutrition_in.name == nutrition_out["name"]
    assert nutrition_in.serving_size == nutrition_out["serving_size"]
    assert nutrition_in.calories_per_100_g == nutrition_out["calories_per_100_g"]


def test_get_after_unsuccessfull_add():
    name = "bad food"
    nutrition_in = NutritionBase(name="bad food", calories_per_100_g=-5)

    with pytest.raises(NegativeAmountError):
        add_nutrition(nutrition_in)
    with pytest.raises(FoodNotFoundError):
        get_nutrition(name)


def test_compound_nutrition():
    avocado = get_compound_nutrition_by_weight("avocado", 100)
    toast = get_compound_nutrition_by_calories("toast", 100)
    coffee = get_compound_nutrition_by_calories("coffee", 2)
    compound = get_compound_nutrition(avocado, toast, coffee)

    assert compound.name == f"{avocado.name}, {toast.name}, {coffee.name}"
    assert compound.calories == avocado.calories + toast.calories + coffee.calories
    assert compound.weight == avocado.weight + toast.weight + coffee.weight
