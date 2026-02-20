"""Pydantic schemas for request/response validation."""

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# ===== USER SCHEMAS =====
class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    theme: Optional[str] = None
    alerts_enabled: Optional[bool] = None
    keywords: Optional[List[str]] = None


class UserResponse(UserBase):
    id: int
    created_at: datetime
    theme: str
    alerts_enabled: bool
    keywords: List[str]

    class Config:
        from_attributes = True


# ===== AUTH SCHEMAS =====
class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


# ===== ARTICLE SCHEMAS =====
class ArticleResponse(BaseModel):
    id: int
    title: str
    url: str
    summary: str
    source: str
    category: str
    published_at: Optional[datetime]
    severity: str
    keywords: List[str]
    color: str

    class Config:
        from_attributes = True


class ArticleSearchRequest(BaseModel):
    query: str
    category: Optional[str] = None
    severity: Optional[str] = None
    limit: int = 20


# ===== SOURCE SCHEMAS =====
class SourceResponse(BaseModel):
    id: int
    name: str
    url: str
    category: str
    color: str
    last_fetch: Optional[datetime]
    article_count: int

    class Config:
        from_attributes = True


# ===== ANALYTICS SCHEMAS =====
class CategoryStats(BaseModel):
    category: str
    article_count: int
    recent_articles: int


class DashboardStats(BaseModel):
    total_articles: int
    total_sources: int
    categories: List[CategoryStats]
    last_update: datetime
