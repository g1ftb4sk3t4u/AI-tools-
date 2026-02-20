"""
Extended API endpoints for feed management
Add these to your backend/app/main.py
"""

# Add these imports at the top of main.py
from fastapi import HTTPException, status
from sqlalchemy import delete

# Add these endpoints to the FastAPI app

@app.get("/api/sources")
async def get_sources():
    """Get all RSS sources"""
    stmt = select(Source)
    result = await db.execute(stmt)
    sources = result.scalars().all()
    return [
        {
            "id": s.id,
            "name": s.name,
            "url": s.rss_url,
            "category": s.category_id,
            "color": s.color,
            "last_fetch": s.created_at
        }
        for s in sources
    ]

@app.post("/api/sources")
async def add_source(data: dict):
    """Add a new RSS source"""
    try:
        source = Source(
            name=data.get("name"),
            rss_url=data.get("url"),
            category_id=data.get("category", "Technology"),
            color=data.get("color", "#55ff55")
        )
        db.add(source)
        await db.commit()
        return {"status": "created", "id": source.id}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/sources/{source_id}")
async def delete_source(source_id: int):
    """Delete a source"""
    try:
        stmt = delete(Source).where(Source.id == source_id)
        await db.execute(stmt)
        await db.commit()
        return {"status": "deleted"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/fetch")
async def fetch_feeds():
    """Manually trigger RSS feed fetch"""
    asyncio.create_task(fetch_rss_feeds_task())
    return {"status": "fetching", "message": "RSS feeds are being fetched"}

@app.get("/api/articles")
async def get_articles(category: str = None, limit: int = 50):
    """Get articles with optional filtering"""
    stmt = select(Article).order_by(Article.timestamp.desc()).limit(limit)
    if category:
        stmt = stmt.where(Article.category_id == category)
    result = await db.execute(stmt)
    articles = result.scalars().all()
    return [article_to_dict(a) for a in articles]

@app.get("/api/stats")
async def get_stats():
    """Get dashboard statistics"""
    total_articles = await db.scalar(select(func.count()).select_from(Article))
    total_sources = await db.scalar(select(func.count()).select_from(Source))
    return {
        "total_articles": total_articles,
        "total_sources": total_sources,
        "categories": list(selectedCategories)
    }

def article_to_dict(article):
    """Convert article to dict"""
    return {
        "id": article.id,
        "title": article.title,
        "url": article.link,
        "summary": article.description or "No summary",
        "source": article.source_name,
        "category": article.category_id,
        "published_at": article.timestamp,
        "severity": "high" if article.severity >= 7 else "medium" if article.severity >= 4 else "low"
    }
