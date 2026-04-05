from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import os

# Use absolute path so SQLite always writes to the project folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if os.environ.get('RAILWAY_ENVIRONMENT'):
    DATABASE_URL = "sqlite:////tmp/pizza_store.db"
else:
    DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'pizza_store.db')}"

engine = create_engine(
    DATABASE_URL, 
    echo=True,
    connect_args={"check_same_thread": False},
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize the database by creating all tables"""
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

def get_session():
    """Get a database session"""
    return SessionLocal()
