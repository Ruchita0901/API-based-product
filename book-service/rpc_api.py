from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Book RPC API",
    description="RPC-style API for book information.",
    version="1.0.0",
)

class Book(BaseModel):
    id: int
    title: str
    author: str

class GetBookRequest(BaseModel):
    id: int

class CreateBookRequest(BaseModel):
    title: str
    author: str

books = [
    {"id": 1, "title": "1984", "author": "George Orwell"}
]

@app.post("/getBook", response_model=Book)
def get_book(request: GetBookRequest):
    book = next((item for item in books if item["id"] == request.id), None)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.post("/createBook", response_model=Book, status_code=201)
def create_book(request: CreateBookRequest):
    next_id = max((item["id"] for item in books), default=0) + 1
    book = {"id": next_id, "title": request.title, "author": request.author}
    books.append(book)
    return book
