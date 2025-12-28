from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Create SQLite database
DATABASE_URL = "sqlite:///pizza_store.db"
engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize the database by creating all tables"""
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

def get_session():
    """Get a database session"""
    return SessionLocal()
