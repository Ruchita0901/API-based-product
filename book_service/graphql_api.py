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
        return next((item for item in books if item["id"] == id), None)

    def resolve_books(self, info):
        return books

class CreateBook(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        author = graphene.String(required=True)

    book = graphene.Field(BookType)

    def mutate(self, info, title, author):
        next_id = max((item["id"] for item in books), default=0) + 1
        book = {"id": next_id, "title": title, "author": author}
        books.append(book)
        return CreateBook(book=book)

class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLApp(schema=schema, on_get=make_playground_handler())
