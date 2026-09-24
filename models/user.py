from sqlmodel import SQLModel, Field, Relationship
from typing import Optional


# Database table
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(unique=True)
    college: str
    # one user can have many books
    books: list["Book"] = Relationship(back_populates="owner")

# request body for creating a user
class UserCreate(SQLModel):
    name:str
    email:str
    college:str

# response body 
class UserRead(SQLModel):
    id:int
    name:str
    email:str
    college:str


# avoid circular import
"""avoid circular import - meaning that the book model is dependent on the user model and vice versa,
   so we need to import the user model after the book model is defined"""
from models.book import Book
User.model_rebuild()

