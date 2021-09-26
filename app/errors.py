class FoodNotFoundError(Exception):
    message = "Food not found"


class NegativeAmountError(Exception):
    message = "Serving size and calories amount must be positive numbers"
