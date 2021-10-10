# REST API application

Simple REST API application for getting food nutrition value. 

## REST API

### Get nutrition value 

```
GET /nutrition/{food_name}
```

### Add new nutrition information

```
POST /nutrition
```

Request body must contain name, serving size (in grams, optional) and calories per 100 grams in the following format: 

```python
name: str
serving_size: Optional[float] = 100
calories_per_100_g: float
```

### Get weight and calories

Get information about food weight and calories given calories amount, weight or a number of servings.

```
GET /nutrition/{food_name}/calories?calories=...
GET /nutrition/{food_name}/weight?weight=...
GET /nutrition/{food_name}/servings?servings=...
```

### Get nutrition value of a mixture of foods

Get information about food weight and calories given a list of food items with weight and calories. Information about each item can be obtained using the previous request.

```
GET /compound-nutrition
```

Request body must contain a list of item in the following format:

```python
name: str
weight: float
calories: float
```

### Get recipes (GraphQL)
Get either all available recipes or some recipe by its name. Access GraphiQL at `/recipes` and enter your query.

#### Schema
```python
type Nutrition {
    calories: Float
    fats: Float
    carbs: Float
    protein: Float
}

type Ingredient {
    name: String
    amount: Float
    nutrition: Nutrition
}

type Recipe {
    name: String
    ingredients: [Ingredient]
    steps: [String]
    nutrition: Nutrition
}
```

#### Query
```python
type Query {
    recipes(name: String): [Recipe]
}
```

#### Examples
```python
query {
  recipes {
    name
    steps
    ingredients {
      amount
      name
    }
  }
}
```

```python
query {
  recipes(name: "Avocado Toast") {
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
```

## Usage

Run the server locally and access it at `localhost:8000`:

```
uvicorn app.main:app --reload
```

Or run the server in a Docker container and access it at `localhost`:
```
docker run -d -p 80:80 myimage
```

## Testing

Unit and integration tests can be run with pytest:

```
pytest
```