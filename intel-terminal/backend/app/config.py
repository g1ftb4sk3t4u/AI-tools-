import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./intel.db")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")
RSS_CHECK_INTERVAL = int(os.getenv("RSS_CHECK_INTERVAL", 5))
MAX_ARTICLES_PER_FEED = int(os.getenv("MAX_ARTICLES_PER_FEED", 10))

# Comprehensive RSS sources organized by category
DEFAULT_SOURCES = [
    # ===== CYBERSECURITY (Red) =====
    {
        "name": "BleepingComputer",
        "url": "https://www.bleepingcomputer.com/feed/",
        "color": "#ff3333",
        "category": "Cybersecurity"
    },
    {
        "name": "Krebs on Security",
        "url": "https://krebsonsecurity.com/feed/",
        "color": "#ff3333",
        "category": "Cybersecurity"
    },
    {
        "name": "Dark Reading",
        "url": "https://www.darkreading.com/feeds/all.rss",
        "color": "#ff3333",
        "category": "Cybersecurity"
    },
    {
        "name": "Securityweek",
        "url": "https://www.securityweek.com/feed/",
        "color": "#ff3333",
        "category": "Cybersecurity"
    },
    {
        "name": "SANS Cyber Aces",
        "url": "https://www.sans.org/cyber-academy/blog/feed.xml",
        "color": "#ff3333",
        "category": "Cybersecurity"
    },
    {
        "name": "Recorded Future Insikt",
        "url": "https://insikt-group.recorded-future.com/rss.xml",
        "color": "#ff3333",
        "category": "Cybersecurity"
    },
    
    # ===== GEOPOLITICAL (Cyan) =====
    {
        "name": "Reuters World",
        "url": "https://feeds.reuters.com/Reuters/worldNews",
        "color": "#00ffff",
        "category": "Geopolitical"
    },
    {
        "name": "BBC News World",
        "url": "http://feeds.bbc.co.uk/news/world/rss.xml",
        "color": "#00ffff",
        "category": "Geopolitical"
    },
    {
        "name": "Al Jazeera English",
        "url": "https://www.aljazeera.com/xml/rss/all.xml",
        "color": "#00ffff",
        "category": "Geopolitical"
    },
    {
        "name": "The Guardian World",
        "url": "https://www.theguardian.com/world/rss",
        "color": "#00ffff",
        "category": "Geopolitical"
    },
    {
        "name": "Associated Press",
        "url": "https://apnews.com/apf-services/v2/homepage.rss",
        "color": "#00ffff",
        "category": "Geopolitical"
    },
    
    # ===== TECHNOLOGY (Yellow) =====
    {
        "name": "Hacker News",
        "url": "https://news.ycombinator.com/rss",
        "color": "#ffff00",
        "category": "Technology"
    },
    {
        "name": "TechCrunch",
        "url": "http://feeds.techcrunch.com/TechCrunch/",
        "color": "#ffff00",
        "category": "Technology"
    },
    {
        "name": "The Verge",
        "url": "https://www.theverge.com/rss/index.xml",
        "color": "#ffff00",
        "category": "Technology"
    },
    {
        "name": "ArXiv CS",
        "url": "http://arxiv.org/rss/cs.all",
        "color": "#ffff00",
        "category": "Technology"
    },
    {
        "name": "InfoQ",
        "url": "https://feed.infoq.com/",
        "color": "#ffff00",
        "category": "Technology"
    },
    {
        "name": "Ars Technica",
        "url": "https://arstechnica.com/feed/",
        "color": "#ffff00",
        "category": "Technology"
    },
    
    # ===== OSINT (Green) =====
    {
        "name": "Bellingcat",
        "url": "https://www.bellingcat.com/feed/",
        "color": "#00ff00",
        "category": "OSINT"
    },
    {
        "name": "First Draft",
        "url": "https://firstdraftnews.org/feed/",
        "color": "#00ff00",
        "category": "OSINT"
    },
    {
        "name": "OSINT Combine",
        "url": "https://www.osintcombine.com/feed",
        "color": "#00ff00",
        "category": "OSINT"
    },
    {
        "name": "MITRE ATT&CK",
        "url": "https://attack.mitre.org/resources/blog/rss.xml",
        "color": "#00ff00",
        "category": "OSINT"
    },
    
    # ===== AI/ML (Purple) =====
    {
        "name": "OpenAI Blog",
        "url": "https://openai.com/feed.xml",
        "color": "#dd00ff",
        "category": "AI/ML"
    },
    {
        "name": "Anthropic News",
        "url": "https://www.anthropic.com/news.rss",
        "color": "#dd00ff",
        "category": "AI/ML"
    },
    {
        "name": "DeepMind Blog",
        "url": "https://www.deepmind.com/blog/feed.xml",
        "color": "#dd00ff",
        "category": "AI/ML"
    },
    {
        "name": "Papers With Code",
        "url": "https://paperswithcode.com/latest/feed",
        "color": "#dd00ff",
        "category": "AI/ML"
    },
    {
        "name": "Hugging Face Blog",
        "url": "https://huggingface.co/blog/feed.xml",
        "color": "#dd00ff",
        "category": "AI/ML"
    },
    
    # ===== PRIVACY/RIGHTS (Orange) =====
    {
        "name": "EFF Blog",
        "url": "https://www.eff.org/feeds/rss",
        "color": "#ff9900",
        "category": "Privacy"
    },
    {
        "name": "Access Now",
        "url": "https://www.accessnow.org/feed/",
        "color": "#ff9900",
        "category": "Privacy"
    },
    {
        "name": "Privacy International",
        "url": "https://www.privacyinternational.org/feed",
        "color": "#ff9900",
        "category": "Privacy"
    },
    
    # ===== INVESTIGATIVE JOURNALISM (Pink) =====
    {
        "name": "ProPublica",
        "url": "https://www.propublica.org/feeds/big-story",
        "color": "#ff1493",
        "category": "Investigation"
    },
    {
        "name": "The Intercept",
        "url": "https://theintercept.com/feed/?lang=en",
        "color": "#ff1493",
        "category": "Investigation"
    },
    
    # ===== HACKING/EXPLOITS (Red) =====
    {
        "name": "EXPLOIT-DB",
        "url": "https://www.exploit-db.com/rss.xml",
        "color": "#ff0000",
        "category": "Cybersecurity"
    },
    {
        "name": "NVD - NIST",
        "url": "https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-recent.json",
        "color": "#ff0000",
        "category": "Cybersecurity"
    },
    {
        "name": "Packet Storm Security",
        "url": "https://packetstormsecurity.com/files/rss/",
        "color": "#ff0000",
        "category": "Cybersecurity"
    },
]

