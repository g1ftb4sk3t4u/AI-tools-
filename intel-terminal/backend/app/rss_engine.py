import feedparser
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Article, Source
from app.websocket import broadcast_article
from app.utils import generate_article_hash, extract_keywords, sanitize_text
from app.config import MAX_ARTICLES_PER_FEED

logger = logging.getLogger(__name__)

async def fetch_and_process_feeds(db: Session):
    """Fetch all enabled sources and process articles"""
    sources = db.query(Source).filter(Source.enabled == True).all()
    
    for source in sources:
        try:
            await fetch_source(source, db)
        except Exception as e:
            logger.error(f"Error fetching {source.name}: {e}")

async def fetch_source(source: Source, db: Session):
    """Fetch a single RSS source"""
    logger.info(f"Fetching: {source.name}")
    
    feed = feedparser.parse(source.rss_url)
    
    if feed.bozo:
        logger.warning(f"Feed error for {source.name}: {feed.bozo_exception}")
    
    # Process latest articles
    for entry in feed.entries[:MAX_ARTICLES_PER_FEED]:
        try:
            title = sanitize_text(entry.get("title", "No title"))
            link = entry.get("link", "")
            description = sanitize_text(entry.get("summary", ""))
            
            if not title or not link:
                continue
            
            # Generate hash for deduplication
            article_hash = generate_article_hash(title, link)
            
            # Check if article already exists
            existing = db.query(Article).filter(
                Article.article_hash == article_hash
            ).first()
            
            if existing:
                logger.debug(f"Duplicate article: {title[:50]}")
                continue
            
            # Extract tags and severity
            tags, severity = extract_keywords(title)
            
            # Create article
            article = Article(
                title=title,
                link=link,
                description=description,
                source_id=source.id,
                source_name=source.name,
                category_id=source.category_id,
                tags=",".join(tags),
                severity=severity,
                article_hash=article_hash,
                timestamp=datetime.utcnow()
            )
            
            db.add(article)
            db.commit()
            
            # Broadcast to WebSocket clients
            await broadcast_article({
                "id": article.id,
                "source": source.name,
                "source_color": source.color,
                "title": title,
                "link": link,
                "tags": tags,
                "severity": severity,
                "timestamp": article.timestamp.isoformat(),
                "category": source.category_id
            })
            
            logger.info(f"New article: {title[:50]}")
            
        except Exception as e:
            logger.error(f"Error processing article from {source.name}: {e}")
