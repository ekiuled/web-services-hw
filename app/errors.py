class FoodNotFoundError(Exception):
    def __init__(self, name):
        self.name = name

    @property
    def message(self):
        return f"Food {self.name} not found"


class FoodsNotFoundError(Exception):
    def __init__(self, names):
        self.names = names

    @property
    def message(self):
        return f"Foods {', '.join(self.names)} not found"


class DuplicateRecipe(Exception):
    def __init__(self, name):
        self.name = name

    @property
    def message(self):
        return f"Recipe {self.name} already exists"


class NegativeAmountError(Exception):
    message = "Serving size and calories amount must be positive numbers"
