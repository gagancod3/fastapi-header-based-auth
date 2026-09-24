from pathlib import Path

from sqlmodel import SQLModel, create_engine, Session

# Database configuration

BASE_DIR = Path(__file__).resolve().parent
DATABASE_FILE = BASE_DIR / "books.db"
DATABASE_URL = f"sqlite:///{DATABASE_FILE.as_posix()}"

print(f"Database URL: {DATABASE_URL}")  # Debugging line to check the database URL

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)

# Create the database tables
def create_tables():
    SQLModel.metadata.create_all(engine)

# Get a database session
def get_session():
    with Session(engine) as session:
        yield session

