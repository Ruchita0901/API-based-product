from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from .data import books

router = APIRouter(tags=["REST"])

class Book(BaseModel):
    id: int
    title: str
    author: str

class BookCreate(BaseModel):
    title: str
    author: str

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None

@router.get("/books", response_model=List[Book])
def list_books():
    return books

@router.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    book = next((item for item in books if item["id"] == book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/books", response_model=Book, status_code=201)
def create_book(payload: BookCreate):
    next_id = max((item["id"] for item in books), default=0) + 1
    book = {"id": next_id, "title": payload.title, "author": payload.author}
    books.append(book)
    return book

@router.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, payload: BookUpdate):
    book = next((item for item in books if item["id"] == book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if payload.title is not None:
        book["title"] = payload.title
    if payload.author is not None:
        book["author"] = payload.author
    return book

@router.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int):
    index = next((idx for idx, item in enumerate(books) if item["id"] == book_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Book not found")
    books.pop(index)
    return None
