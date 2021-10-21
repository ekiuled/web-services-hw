nutrition_db = {
    "avocado": {
        "name": "avocado",
        "serving_size": 201,
        "calories_per_serving": 426.12,
        "calories_per_100_g": 212,
        "fats_per_100_g": 20,
        "carbs_per_100_g": 6,
        "protein_per_100_g": 2
    },
    "coffee": {
        "name": "coffee",
        "serving_size": 237,
        "calories_per_serving": 2,
        "calories_per_100_g": 0.84,
        "fats_per_100_g": 0.02,
        "carbs_per_100_g": 0.04,
        "protein_per_100_g": 0.12
    },
    "toast": {
        "name": "toast",
        "serving_size": 50,
        "calories_per_serving": 150,
        "calories_per_100_g": 300,
        "fats_per_100_g": 3.5,
        "carbs_per_100_g": 50,
        "protein_per_100_g": 8
    },
    "cream": {
        "name": "cream",
        "serving_size": 50,
        "calories_per_serving": 59,
        "calories_per_100_g": 118,
        "fats_per_100_g": 10,
        "carbs_per_100_g": 4.5,
        "protein_per_100_g": 2.6
    }
}

recipe_db = {
    "Avocado Toast": {
        "name": "Avocado Toast",
        "steps": ["Mash avocado", "Put avocado on toast"],
        "ingredients": [{
            "name": "avocado",
            "amount": 201,
        }, {
            "name": "toast",
            "amount": 50,
        }]
    },
    "Coffee & Cream": {
        "name": "Coffee & Cream",
        "steps": ["Whip the cream", "Pour coffee into whipped cream"],
        "ingredients": [{
            "name": "cream",
            "amount": 50,
        }, {
            "name": "coffee",
            "amount": 200,
        }]
    }
}
