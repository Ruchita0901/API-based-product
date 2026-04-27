from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp, make_playground_handler
import graphene

books = [
    {"id": 1, "title": "1984", "author": "George Orwell"}
]

class BookType(graphene.ObjectType):
    id = graphene.Int()
    title = graphene.String()
    author = graphene.String()

class Query(graphene.ObjectType):
    book = graphene.Field(BookType, id=graphene.Int(required=True))
    books = graphene.List(BookType)

    def resolve_book(self, info, id):
        matched = next((item for item in books if item["id"] == id), None)
        return matched

    def resolve_books(self, info):
        return books

schema = graphene.Schema(query=Query)

app = FastAPI(
    title="Book GraphQL API",
    description="GraphQL API for single book retrieval.",
    version="1.0.0",
)

app.add_route(
    "/graphql",
    GraphQLApp(schema=schema, on_get=make_playground_handler()),
)
app.add_websocket_route("/graphql", GraphQLApp(schema=schema))
