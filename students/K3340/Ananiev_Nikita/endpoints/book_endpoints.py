from fastapi import APIRouter, Depends
from models.models import Book, BookDefault, BookInfo, BookInfoDefault
from models.public_models import BookPublic, BookPatch
from connection import get_session
from helpers import upd_model, get_object_by_id
from typing_extensions import TypedDict

book_router = APIRouter()

@book_router.get("/book_instance/{id}", response_model=BookPublic)
def get_book_instance(book_id: int, session=Depends(get_session)):
    return get_object_by_id(book_id, Book, session)


@book_router.post("/book_instance")
def create_book_instance(new_book: BookDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "created": Book}):
    new_book = Book.model_validate(new_book)
    session.add(new_book)
    session.commit()
    session.refresh(new_book)
    return {"status": 201, "created": new_book}


@book_router.patch("/book_instance/{id}")
def update_book_instance(book_id: int, upd_book: BookPatch, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "updated": Book}):
    book = get_object_by_id(book_id, Book, session)
    upd_data = upd_book.model_dump(exclude_unset=True)
    book = upd_model(book, upd_data, session)
    return {"status": 202, "updated": book}


@book_router.post("/book_info")
def create_book_instance(book: BookInfoDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "created": BookInfo}):
    book = BookInfo.model_validate(book)
    session.add(book)
    session.commit()
    session.refresh(book)
    return {"status": 201, "created": book}
