from starlette_graphene3 import GraphQLApp, make_playground_handler
import graphene
from .data import books

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
graphql_app = GraphQLApp(schema=schema, on_get=make_playground_handler())
