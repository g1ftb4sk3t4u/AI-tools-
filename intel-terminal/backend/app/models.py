from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Index, JSON
from sqlalchemy.orm import declarative_base
from datetime import datetime
import hashlib

Base = declarative_base()


class User(Base):
    """User model for Phase 2 authentication and preferences."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    username = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    theme = Column(String(20), default="green")  # green or color
    alerts_enabled = Column(Boolean, default=True)
    keywords = Column(JSON, default=[])  # user's watched keywords

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    color = Column(String(7), default="#ffffff")
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    rss_url = Column(String(500), unique=True)
    color = Column(String(7), default="#ffffff")
    category_id = Column(Integer, ForeignKey("categories.id"))
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Article(Base):
    __tablename__ = "articles"
    __table_args__ = (
        Index('idx_source_timestamp', 'source_id', 'timestamp'),
        Index('idx_article_hash', 'article_hash'),
    )

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), index=True)
    link = Column(String(500))
    description = Column(Text, nullable=True)
    source_id = Column(Integer, ForeignKey("sources.id"))
    source_name = Column(String(255))
    category_id = Column(Integer, nullable=True)
    tags = Column(String(500), default="")  # Comma-separated
    severity = Column(Integer, default=0)  # 0-10 scale
    article_hash = Column(String(64), unique=True, index=True)  # SHA256 for deduplication
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    fetched_at = Column(DateTime, default=datetime.utcnow)

    @staticmethod
    def generate_hash(title: str, link: str) -> str:
        """Generate unique hash for deduplication"""
        content = f"{title}{link}".encode()
        return hashlib.sha256(content).hexdigest()
