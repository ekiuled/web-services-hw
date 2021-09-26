import pytest
from ..core import *
from ..errors import *
from ..scheme import NutritionBase
from ..database import nutrition_db


class TestGetNutrition:
    def test_get_nutrition_successfull(self):
        nutrition = get_nutrition("avocado")
        assert "name" in nutrition
        assert "serving_size" in nutrition
        assert "calories_per_100_g" in nutrition
        assert "calories_per_serving" in nutrition
        assert nutrition["name"] == "avocado"

    def test_get_different_nutrition_successfull(self):
        nutrition = get_nutrition("coffee")
        assert nutrition["name"] == "coffee"

    def test_get_invalid_food(self):
        with pytest.raises(FoodNotFoundError):
            get_nutrition("bad food")


class TestAddNutrition:
    def test_add_nutrition_successfull(self):
        name = "ok"
        serving_size = 1
        calories_per_100_g = 100
        calories_per_serving = 1

        nutrition = NutritionBase(name=name, serving_size=serving_size, calories_per_100_g=calories_per_100_g)
        add_nutrition(nutrition)

        assert name in nutrition_db
        assert nutrition_db[name]["serving_size"] == serving_size
        assert nutrition_db[name]["calories_per_100_g"] == calories_per_100_g
        assert nutrition_db[name]["calories_per_serving"] == calories_per_serving

    def test_add_nutrition_negative_serving_size(self):
        with pytest.raises(NegativeAmountError):
            nutrition = NutritionBase(name="bad food", serving_size=-1, calories_per_100_g=10)
            add_nutrition(nutrition)
        assert "bad food" not in nutrition_db

    def test_add_nutrition_zero_calories(self):
        with pytest.raises(NegativeAmountError):
            nutrition = NutritionBase(name="bad food", serving_size=1, calories_per_100_g=0)
            add_nutrition(nutrition)
        assert "bad food" not in nutrition_db


class TestGetCompoundNutritionSingleFood:
    def test_compound_nutrition_by_calories(self):
        nutrition = get_compound_nutrition_by_calories("toast", 450)
        assert nutrition.name == "toast"
        assert nutrition.calories == 450
        assert nutrition.weight == 150

    def test_compound_nutrition_by_weight(self):
        nutrition = get_compound_nutrition_by_weight("toast", 150)
        assert nutrition.name == "toast"
        assert nutrition.calories == 450
        assert nutrition.weight == 150

    def test_compound_nutrition_by_servings(self):
        nutrition = get_compound_nutrition_by_servings("toast", 3)
        assert nutrition.name == "toast"
        assert nutrition.calories == 450
        assert nutrition.weight == 150

    def test_invalid_food_by_calories(self):
        with pytest.raises(FoodNotFoundError):
            get_compound_nutrition_by_calories("bad food", 123)

    def test_invalid_food_by_weight(self):
        with pytest.raises(FoodNotFoundError):
            get_compound_nutrition_by_weight("bad food", 123)

    def test_invalid_food_by_servings(self):
        with pytest.raises(FoodNotFoundError):
            get_compound_nutrition_by_servings("bad food", 1.5)


class TestGetCompoundNutrition:
    def test_empty_food(self):
        nutrition = get_compound_nutrition()
        assert nutrition.name == ""
        assert nutrition.weight == 0
        assert nutrition.calories == 0

    def test_single_food(self):
        nutrition_in = CompoundNutrition(name="example", weight=100, calories=10)
        nutrition_out = get_compound_nutrition(nutrition_in)
        assert nutrition_in == nutrition_out

    def test_several_items(self):
        nutrition = get_compound_nutrition(CompoundNutrition(name="one", weight=100, calories=10),
                                           CompoundNutrition(
            name="two", weight=1000, calories=1000),
            CompoundNutrition(name="three", weight=300, calories=123))
        assert nutrition.name == "one, two, three"
        assert nutrition.weight == 1400
        assert nutrition.calories == 1133
