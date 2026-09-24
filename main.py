from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_tables
from routes import books, users

from models.book import Book
from models.user import User


# deprecated way

# @app.on_event("startup")
# def on_startup():
#     create_tables()


# new way - to create tables on startup and cleanup on shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    print("Database tables created")
    yield
    # shutdown: cleanup here
    print("Shutting down the app")

app = FastAPI(
    title="Bookstore API",
    description="A simple API for managing books and users",
    version="1.0.0",
    lifespan=lifespan  # lifespan key passed to call lifespan function 
)

app.include_router(books.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Bookstore API!"}