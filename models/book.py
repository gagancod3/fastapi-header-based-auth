from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

# Database table class
class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title:str = Field(index=True)
    author:str = Field(index=True)
    price:int
    is_sold:bool = Field(default=False)

    # Foreign key yo user table
    user_id:int = Field(foreign_key="user.id")
    owner: Optional["User"] = Relationship(back_populates="books")


# request body for creating a book
class BookCreate(SQLModel):
    title:str
    author:str
    price:int
    user_id:int

# response body 
class BookRead(SQLModel):
    id:int
    title:str
    author:str
    price:int
    is_sold:bool
    user_id:int

# request body for updating a book
class BookUpdate(SQLModel):
    price: Optional[int] = None
    is_sold: Optional[bool] = None


# avoid circular import
"""avoid circular import - meaning that the book model is dependent on the user model and vice versa,
   so we need to import the user model after the book model is defined"""
from models.user import User
Book.model_rebuild()
