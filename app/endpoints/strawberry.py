from strawberry.asgi import GraphQL
from strawberry import Schema

from app.endpoints.fastapi import app
from app.database.database import get_db
from app.strawberry.scheme import *
from app.strawberry.core import *


@strawberry.type
class Query:
    @strawberry.field
    def recipes(self, name: str = None) -> List[Recipe]:
        if name is None:
            return get_all_recipes(next(get_db()))
        return [get_recipe(next(get_db()), name)]


schema = Schema(Query)
graphql_app = GraphQL(schema)
app.add_route("/recipes", graphql_app)
