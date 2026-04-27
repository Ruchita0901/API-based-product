from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from .data import books

router = APIRouter(tags=["REST"])

class Book(BaseModel):
    id: int
    title: str
    author: str

@router.get("/books", response_model=List[Book])
def list_books():
    return books

@router.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    book = next((item for item in books if item["id"] == book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
