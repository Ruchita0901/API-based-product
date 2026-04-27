from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="Book REST API",
    description="REST API for book information.",
    version="1.0.0",
)

class Book(BaseModel):
    id: int
    title: str
    author: str

books = [
    {"id": 1, "title": "1984", "author": "George Orwell"}
]

@app.get("/books", response_model=List[Book])
def list_books():
    return books

@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    book = next((item for item in books if item["id"] == book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
