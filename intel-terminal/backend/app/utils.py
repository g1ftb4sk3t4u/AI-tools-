import hashlib
from datetime import datetime

def generate_article_hash(title: str, link: str) -> str:
    """Generate SHA256 hash for deduplication"""
    content = f"{title}{link}".encode()
    return hashlib.sha256(content).hexdigest()

def extract_keywords(title: str) -> list:
    """Simple keyword extraction for tagging"""
    # Keywords that indicate severity
    severity_words = {
        "critical": 10,
        "exploit": 9,
        "ransomware": 9,
        "breach": 8,
        "vulnerability": 8,
        "attack": 7,
        "alert": 6,
        "warning": 5,
    }

    title_lower = title.lower()
    severity = 0
    tags = []

    for word, score in severity_words.items():
        if word in title_lower:
            severity = max(severity, score)
            tags.append(word.upper())

    return tags, severity

def format_timestamp(dt: datetime) -> str:
    """Format datetime for IRC-style display"""
    if not dt:
        return "[??:??]"
    return f"[{dt.strftime('%H:%M')}]"

def sanitize_text(text: str) -> str:
    """Remove HTML and dangerous characters from RSS content"""
    if not text:
        return ""
    
    # Remove HTML tags
    import re
    text = re.sub(r'<[^>]+>', '', text)
    
    # Escape special characters
    text = text.replace("&lt;", "<").replace("&gt;", ">")
    text = text.replace("&quot;", '"').replace("&#39;", "'")
    text = text.replace("&amp;", "&")
    
    return text.strip()
