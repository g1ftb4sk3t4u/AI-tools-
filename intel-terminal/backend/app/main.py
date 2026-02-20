import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.database import init_db, SessionLocal
from app.models import Category, Source, Article
from app.websocket import router as websocket_router, broadcast_status
from app.rss_engine import fetch_and_process_feeds
from app.config import RSS_CHECK_INTERVAL, DEFAULT_SOURCES
import os

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Scheduler
scheduler = AsyncIOScheduler()

async def initialize_default_data():
    """Create default categories and sources if they don't exist"""
    db = SessionLocal()
    try:
        # Category colors mapping
        CATEGORY_COLORS = {
            'Cybersecurity': '#ff3333',
            'Geopolitical': '#00ffff',
            'Technology': '#ffff00',
            'OSINT': '#00ff00',
            'AI/ML': '#dd00ff',
            'Privacy': '#ff9900',
            'Science': '#00aaff',
            'Investigation': '#ff1493'
        }
        
        # Create default categories with proper colors
        category_names = set()
        for source in DEFAULT_SOURCES:
            category_names.add(source["category"])
        
        for cat_name in category_names:
            existing = db.query(Category).filter(Category.name == cat_name).first()
            if not existing:
                category = Category(
                    name=cat_name, 
                    color=CATEGORY_COLORS.get(cat_name, "#ffffff")
                )
                db.add(category)
                db.commit()
                logger.info(f"Created category: {cat_name}")
            else:
                # Update color if it was #ffffff
                if existing.color == "#ffffff":
                    existing.color = CATEGORY_COLORS.get(cat_name, "#ffffff")
                    db.commit()
        
        # Create default sources
        for source_config in DEFAULT_SOURCES:
            if not db.query(Source).filter(
                Source.rss_url == source_config["url"]
            ).first():
                category = db.query(Category).filter(
                    Category.name == source_config["category"]
                ).first()
                
                source = Source(
                    name=source_config["name"],
                    rss_url=source_config["url"],
                    color=source_config["color"],
                    category_id=category.id if category else None
                )
                db.add(source)
                db.commit()
                logger.info(f"Created source: {source_config['name']}")
    finally:
        db.close()

async def scheduled_fetch():
    """Scheduled task to fetch RSS feeds"""
    db = SessionLocal()
    try:
        logger.info("Starting RSS fetch...")
        await fetch_and_process_feeds(db)
    except Exception as e:
        logger.error(f"Scheduled fetch error: {e}")
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info("Intel Terminal starting...")
    init_db()
    await initialize_default_data()
    
    scheduler.add_job(
        scheduled_fetch,
        "interval",
        minutes=RSS_CHECK_INTERVAL,
        id="rss_fetch",
        name="RSS Feed Fetch"
    )
    scheduler.start()
    logger.info(f"Scheduler started (interval: {RSS_CHECK_INTERVAL} minutes)")
    
    yield
    
    # Shutdown
    logger.info("Intel Terminal shutting down...")
    scheduler.shutdown()

app = FastAPI(
    title="Intel Terminal",
    description="RSS Intelligence Dashboard with Discord Alerts",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket router
app.include_router(websocket_router)

# Static files path - check multiple locations for different deployment scenarios
# Local dev: ../frontend, Docker/Railway: /app/static or ./static
possible_frontend_paths = [
    os.path.join(os.path.dirname(__file__), "..", "..", "frontend"),  # Local dev
    "/app/static",  # Railway/Docker
    os.path.join(os.path.dirname(__file__), "..", "static"),  # Alternative
    "./static",  # Current directory
]
frontend_path = None
for path in possible_frontend_paths:
    if os.path.exists(path):
        frontend_path = path
        break


@app.get("/api/sources")
def get_sources():
    """Get all RSS sources"""
    db = SessionLocal()
    try:
        sources = db.query(Source).all()
        return [
            {
                "id": s.id,
                "name": s.name,
                "url": s.rss_url,
                "category": s.category_id,
                "color": s.color,
                "last_fetch": s.created_at.isoformat() if s.created_at else None
            }
            for s in sources
        ]
    finally:
        db.close()

@app.post("/api/sources")
def add_source(data: dict):
    """Add a new RSS source"""
    db = SessionLocal()
    try:
        # Look up category by name to get ID
        category_name = data.get("category", "Technology")
        category = db.query(Category).filter(Category.name == category_name).first()
        category_id = category.id if category else None
        
        source = Source(
            name=data.get("name"),
            rss_url=data.get("url"),
            category_id=category_id,
            color=data.get("color", "#55ff55")
        )
        db.add(source)
        db.commit()
        return {"status": "created", "id": source.id}
    except Exception as e:
        db.rollback()
        return {"status": "error", "detail": str(e)}
    finally:
        db.close()

@app.delete("/api/sources/{source_id}")
def delete_source(source_id: int):
    """Delete a source"""
    db = SessionLocal()
    try:
        source = db.query(Source).filter(Source.id == source_id).first()
        if source:
            db.delete(source)
            db.commit()
        return {"status": "deleted"}
    except Exception as e:
        db.rollback()
        return {"status": "error", "detail": str(e)}
    finally:
        db.close()

@app.get("/api/categories")
def get_categories():
    """Get all categories"""
    db = SessionLocal()
    try:
        cats = db.query(Category).all()
        return [
            {
                "id": c.id,
                "name": c.name,
                "color": c.color,
                "enabled": c.enabled
            }
            for c in cats
        ]
    finally:
        db.close()

@app.post("/api/categories")
def add_category(data: dict):
    """Add a new category"""
    db = SessionLocal()
    try:
        category = Category(
            name=data.get("name"),
            color=data.get("color", "#00ffff")
        )
        db.add(category)
        db.commit()
        return {"status": "created", "id": category.id, "name": category.name}
    except Exception as e:
        db.rollback()
        return {"status": "error", "detail": str(e)}
    finally:
        db.close()

@app.delete("/api/categories/{category_id}")
def delete_category(category_id: int):
    """Delete a category"""
    db = SessionLocal()
    try:
        cat = db.query(Category).filter(Category.id == category_id).first()
        if cat:
            db.delete(cat)
            db.commit()
        return {"status": "deleted"}
    except Exception as e:
        db.rollback()
        return {"status": "error", "detail": str(e)}
    finally:
        db.close()

@app.post("/api/fetch")
async def fetch_feeds():
    """Manually trigger RSS feed fetch"""
    db = SessionLocal()
    try:
        await fetch_and_process_feeds(db)
        return {"status": "success", "message": "RSS feeds fetched"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    finally:
        db.close()

@app.get("/api/articles")
def get_articles(category: str = None, limit: int = 50):
    """Get articles with optional filtering"""
    db = SessionLocal()
    try:
        # Build category name lookup
        cats = {c.id: c.name for c in db.query(Category).all()}
        # Build source color lookup
        source_colors = {s.id: s.color for s in db.query(Source).all()}
        
        query = db.query(Article).order_by(Article.timestamp.desc()).limit(limit)
        if category:
            query = query.filter(Article.category_id == category)
        articles = query.all()
        return [
            {
                "id": a.id,
                "title": a.title,
                "url": a.link,
                "summary": a.description or "No summary",
                "source": a.source_name,
                "source_color": source_colors.get(a.source_id, "#55ff55"),
                "category": cats.get(a.category_id, "Unknown"),
                "category_id": a.category_id,
                "published_at": a.timestamp.isoformat() if a.timestamp else None,
                "severity": "high" if a.severity >= 7 else "medium" if a.severity >= 4 else "low"
            }
            for a in articles
        ]
    finally:
        db.close()

@app.get("/api/dashboard-stats")
def get_dashboard_stats():
    """Get dashboard statistics"""
    db = SessionLocal()
    try:
        total_articles = db.query(Article).count()
        total_sources = db.query(Source).count()
        return {
            "total_articles": total_articles or 0,
            "total_sources": total_sources or 0
        }
    finally:
        db.close()

@app.get("/api/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Intel Terminal",
        "scheduler": scheduler.running
    }

@app.get("/api/stats")
async def stats():
    """Get basic stats"""
    db = SessionLocal()
    try:
        categories = db.query(Category).count()
        sources = db.query(Source).count()
        articles = db.query(Article).count()
        
        return {
            "categories": categories,
            "sources": sources,
            "articles": articles
        }
    finally:
        db.close()

# Mount static files LAST so API routes take precedence
if frontend_path and os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
