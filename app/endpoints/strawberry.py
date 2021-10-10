from strawberry.asgi import GraphQL
from strawberry import Schema

from app.endpoints.fastapi import app
from app.strawberry.scheme import *
from app.strawberry.core import *


@strawberry.type
class Query:
    @strawberry.field
    def recipes(self, name: str = None) -> List[Recipe]:
        if name is None:
            return get_all_recipes()
        return [get_recipe(name)]


schema = Schema(Query)
graphql_app = GraphQL(schema)
app.add_route("/recipes", graphql_app)
