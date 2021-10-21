import pytest
from app.fastapi.core import *
from app.errors import *
from app.fastapi.scheme import NutritionBase


class TestGetNutrition:
    def test_get_nutrition_successfull(self, db_session):
        nutrition = get_nutrition(db_session, "avocado")
        assert nutrition.name == "avocado"

    def test_get_different_nutrition_successfull(self, db_session):
        nutrition = get_nutrition(db_session, "coffee")
        assert nutrition.name == "coffee"

    def test_get_invalid_food(self, db_session):
        with pytest.raises(FoodNotFoundError):
            get_nutrition(db_session, "bad food")


class TestAddNutrition:
    def test_add_nutrition_successfull(self, db_session, db_get):
        name = "ok"
        serving_size = 1
        calories_per_100_g = 100
        calories_per_serving = 1

        nutrition = NutritionBase(name=name, serving_size=serving_size, calories_per_100_g=calories_per_100_g)
        add_nutrition(db_session, nutrition)
        db_nutrition = db_get(name)

        assert db_nutrition is not None
        assert db_nutrition.serving_size == serving_size
        assert db_nutrition.calories_per_100_g == calories_per_100_g
        assert db_nutrition.calories_per_serving == calories_per_serving

    def test_add_nutrition_negative_serving_size(self, db_session, db_get):
        name = "bad food"
        with pytest.raises(NegativeAmountError):
            nutrition = NutritionBase(name=name, serving_size=-1, calories_per_100_g=10)
            add_nutrition(db_session, nutrition)
        assert db_get(name) is None

    def test_add_nutrition_zero_calories(self, db_session, db_get):
        name = "bad food"
        with pytest.raises(NegativeAmountError):
            nutrition = NutritionBase(name=name, serving_size=1, calories_per_100_g=0)
            add_nutrition(db_session, nutrition)
        assert db_get(name) is None


class TestGetCompoundNutritionSingleFood:
    def test_compound_nutrition_by_calories(self, db_session):
        nutrition = get_compound_nutrition_by_calories(db_session, "toast", 450)
        assert nutrition.name == "toast"
        assert nutrition.calories == 450
        assert nutrition.weight == 150

    def test_compound_nutrition_by_weight(self, db_session):
        nutrition = get_compound_nutrition_by_weight(db_session, "toast", 150)
        assert nutrition.name == "toast"
        assert nutrition.calories == 450
        assert nutrition.weight == 150

    def test_compound_nutrition_by_servings(self, db_session):
        nutrition = get_compound_nutrition_by_servings(db_session, "toast", 3)
        assert nutrition.name == "toast"
        assert nutrition.calories == 450
        assert nutrition.weight == 150

    def test_invalid_food_by_calories(self, db_session):
        with pytest.raises(FoodNotFoundError):
            get_compound_nutrition_by_calories(db_session, "bad food", 123)

    def test_invalid_food_by_weight(self, db_session):
        with pytest.raises(FoodNotFoundError):
            get_compound_nutrition_by_weight(db_session, "bad food", 123)

    def test_invalid_food_by_servings(self, db_session):
        with pytest.raises(FoodNotFoundError):
            get_compound_nutrition_by_servings(db_session, "bad food", 1.5)


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
