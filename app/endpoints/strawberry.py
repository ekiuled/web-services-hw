from strawberry.asgi import GraphQL
from strawberry import Schema

from app.endpoints.fastapi import app
from app.database.database import DB
from app.errors import DuplicateRecipe, FoodsNotFoundError
from app.strawberry.scheme import *
from app.strawberry import core


@strawberry.type
class Query:
    @strawberry.field
    def recipes(self, name: str = None) -> List[Recipe]:
        db = DB()
        if name is None:
            return core.get_all_recipes(db)
        return [core.get_recipe(db, name)]


@strawberry.type
class GenerateRecipeSuccess:
    name: str
    ingredients: List[str]


@strawberry.type
class MissingIngredients:
    ingredients: List[str]


@strawberry.type
class RecipeExists:
    name: str


Response = strawberry.union("GerenateRecipeResponse",
                            (GenerateRecipeSuccess, MissingIngredients, RecipeExists))


@strawberry.type
class Mutation:
    @strawberry.mutation
    def generate_recipe(self, name: str, ingredients: List[str]) -> Response:
        db = DB()
        try:
            core.generate_recipe(db, name, ingredients)
            return GenerateRecipeSuccess(name=name, ingredients=ingredients)
        except FoodsNotFoundError as e:
            return MissingIngredients(ingredients=e.names)
        except DuplicateRecipe as e:
            return RecipeExists(name=e.name)


schema = Schema(query=Query, mutation=Mutation)
graphql_app = GraphQL(schema)
app.add_route("/recipes", graphql_app)
