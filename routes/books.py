from fastapi import Depends, HTTPException, APIRouter, Query
from sqlmodel import Session, select
from typing import Optional
from database import get_session

from models.book import Book, BookCreate, BookRead, BookUpdate

from auth import verify_api_key


router=APIRouter(
    prefix="/books",tags=["books"])

@router.get("/", response_model=list[BookRead])
def list_books(
    title: Optional[str] = Query(None, description="Filter books by title"),
    author: Optional[str] = Query(None, description="Filter books by author"),
    session: Session = Depends(get_session),
    # api_key: str = Depends(verify_api_key)
    ):

    query = select(Book).where(Book.is_sold == False)

    if title:
        query = query.where(Book.title.contains(title))
    if author:
        query = query.where(Book.author.contains(author))

    books = session.exec(query).all()
    return books


@router.post("/", response_model=BookRead)
def create_book(
    book_data: BookCreate,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key),
):
    # matching api key (Authentication)
    if api_key != "my_secret_key":
        raise HTTPException(status_code=401, detail="Invalid API key")

    
    book = Book.model_validate(book_data)
    print(f"Book data: {book_data}, Book object: {book}")
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@router.patch("/{book_id}", response_model=BookRead)
def update_book(
    book_id: int,
    update: BookUpdate,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key),
):
    # matching api key (Authentication)
    if api_key != "my_secret_key":
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    book = session.get(Book, book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    book_data_dict = update.model_dump(exclude_unset=True)

    # update the book object with the provided data
    for key, value in book_data_dict.items():
        # update the attribute of the book object with the new value
        setattr(book, key, value)

    session.add(book)
    session.commit()
    session.refresh(book)
    return book

@router.patch("/{book_id}/mark_sold", response_model=BookRead)
def mark_book_as_sold(
    book_id: int,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key),
):
    # matching api key (Authentication)
    if api_key != "my_secret_key":
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    book = session.get(Book, book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    book.is_sold = True

    session.add(book)
    session.commit()
    session.refresh(book)
    return book