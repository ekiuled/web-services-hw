from app.endpoints.strawberry import schema


def test_get_all_recipes_names():
    query = """
        query {
            recipes {
                name
            }
        }
    """

    result = schema.execute_sync(query)

    assert result.errors is None
    assert result.data["recipes"] == [{"name": "Avocado Toast"},
                                      {"name": "Coffee & Cream"}]


def test_get_full_recipe():
    query = """
        query Test($name: String!) {
            recipes(name: $name) {
                name
                ingredients {
                    name
                    nutrition {
                        calories
                        fats
                        protein
                        carbs
                    }
                    amount
                }
                nutrition {
                    calories
                    carbs
                    fats
                    protein
                }
                steps
            }
        }
    """

    result = schema.execute_sync(query,
                                 variable_values={"name": "Avocado Toast"})

    assert result.errors is None
    assert result.data["recipes"] == [{
        "name": "Avocado Toast",
        "ingredients": [
            {
                "name": "avocado",
                "nutrition": {
                    "calories": 426.12,
                    "fats": 40.2,
                    "protein": 4.0200000000000005,
                    "carbs": 12.059999999999999
                },
                "amount": 201
            },
            {
                "name": "toast",
                "nutrition": {
                    "calories": 150,
                    "fats": 1.7500000000000002,
                    "protein": 4,
                    "carbs": 25
                },
                "amount": 50
            }
        ],
        "nutrition": {
            "calories": 576.12,
            "carbs": 37.06,
            "fats": 41.95,
            "protein": 8.02
        },
        "steps": [
            "Mash avocado",
            "Put avocado on toast"
        ]
    }]


def test_get_invalid_recipe():
    query = """
        query {
            recipes(name: "Bad Recipe") {
                name
            }
        }
    """

    result = schema.execute_sync(query)
    assert result.errors is not None
