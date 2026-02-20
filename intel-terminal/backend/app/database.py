from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.config import DATABASE_URL
from app.models import Base

# For SQLite, use StaticPool for in-memory or file-based
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool if "sqlite" in DATABASE_URL else None
)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency for getting DB session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
