# 🎯 INTEL TERMINAL - PHASE 1 COMPLETE

## Project Overview

**Intel Terminal** is a personal SIGINT dashboard that monitors RSS feeds with:
- 🟢 IRC-style terminal UI (green + multi-color themes)
- 🌐 Real-time WebSocket streaming
- 🔍 Smart deduplication & severity scoring
- 🐉 Discord webhook alerts
- 📁 Category-based filtering

## What Was Fixed/Improved from ChatGPT Code

✅ **Database auto-initialization** - Creates tables on startup  
✅ **Deduplication logic** - SHA256 hashing prevents duplicates  
✅ **Error handling** - Try/catch on RSS feeds + WebSocket  
✅ **Environment variables** - Proper .env config with defaults  
✅ **Scheduler lifecycle** - Properly starts/stops with app  
✅ **Article persistence** - Actually saves to DB (ChatGPT was missing this)  
✅ **Severity scoring** - Auto-detects keywords (exploit, breach, critical, etc.)  
✅ **Discord integration** - Ready for webhook alerts  
✅ **Frontend theme toggle** - Both green & color themes  
✅ **Static file serving** - Frontend auto-served from backend  

## Architecture

```
INTEL TERMINAL
│
├─ BACKEND (FastAPI)
│  ├─ main.py          → App initialization, scheduler, startup
│  ├─ config.py        → Settings, default sources
│  ├─ database.py      → SQLAlchemy setup
│  ├─ models.py        → Category, Source, Article ORM
│  ├─ rss_engine.py    → Feed fetching & processing
│  ├─ websocket.py     → Real-time broadcast manager
│  ├─ discord.py       → Webhook alert system
│  └─ utils.py         → Hash, keywords, sanitize
│
├─ FRONTEND (HTML/CSS/JS)
│  ├─ index.html       → IRC-style terminal UI
│  ├─ styles.css       → Green + Color themes
│  └─ app.js           → WebSocket client + interactivity
│
└─ INFRASTRUCTURE
   ├─ SQLite database  → articles, sources, categories
   ├─ WebSocket        → Real-time article stream
   └─ APScheduler      → RSS fetch every N minutes
```

## Files Created

### Backend (11 files)
```
backend/
├── app/
│   ├── __init__.py           (Empty module marker)
│   ├── main.py               (FastAPI app + lifespan + endpoints)
│   ├── config.py             (Environment & defaults)
│   ├── database.py           (SQLAlchemy engine + session)
│   ├── models.py             (ORM models + schema)
│   ├── rss_engine.py         (Feed fetcher + article processor)
│   ├── websocket.py          (WebSocket broadcast manager)
│   ├── discord.py            (Discord webhook alerts)
│   ├── utils.py              (Hash, keywords, sanitize)
│   ├── __init__.py
├── requirements.txt          (Dependencies)
├── run.py                    (Entry point)
├── .env.example              (Config template)
└── .gitignore               (Ignore rules)
```

### Frontend (3 files)
```
frontend/
├── index.html               (Terminal UI)
├── styles.css               (Themes)
└── app.js                   (Client logic)
```

### Documentation (2 files)
```
README.md                     (Full docs)
QUICKSTART.md                (5-minute setup)
```

## Key Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **API** | FastAPI | Async REST + WebSocket |
| **DB** | SQLite + SQLAlchemy | Persistent storage |
| **RSS** | feedparser | Feed parsing |
| **Scheduling** | APScheduler | Periodic fetching |
| **Frontend** | HTML/CSS/JS | Terminal UI + WebSocket |
| **Alerts** | Discord webhooks | High-severity notifications |

## Database Schema

### Categories
```
id (PK)          INTEGER
name             STRING (unique)
color            HEX (#rrggbb)
enabled          BOOLEAN
created_at       DATETIME
```

### Sources
```
id (PK)          INTEGER
name             STRING
rss_url          STRING (unique)
color            HEX (#rrggbb)
category_id      FK → categories.id
enabled          BOOLEAN
created_at       DATETIME
```

### Articles
```
id (PK)          INTEGER
title            STRING
link             STRING
description      TEXT
source_id        FK → sources.id
source_name      STRING
category_id      FK → categories.id
tags             CSV (#TAG1, #TAG2)
severity         INTEGER (0-10)
article_hash     SHA256 (UNIQUE for dedup)
timestamp        DATETIME
fetched_at       DATETIME
```

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/health` | Service health |
| GET | `/api/stats` | Database stats |
| WS | `/ws` | Real-time article stream |
| GET | `/` | Frontend (auto-served) |

## WebSocket Protocol

### Client → Server
```json
{
  // Listen only (keep connection alive)
}
```

### Server → Client
```json
{
  "type": "article",
  "data": {
    "id": 1,
    "source": "BleepingComputer",
    "source_color": "#ff5555",
    "title": "Zero-day in Apache Log4j",
    "link": "https://...",
    "tags": ["CRITICAL", "EXPLOIT"],
    "severity": 9,
    "timestamp": "2026-02-18T22:41:00"
  }
}
```

## Deployment Ready

✅ Single command startup  
✅ Auto database initialization  
✅ Hot reload in development  
✅ Production-ready async code  
✅ Error handling & logging  
✅ Environment-based config  
✅ Docker-ready (Phase 2)  

## Default Configuration

- **RSS Check Interval**: 5 minutes
- **Max Articles/Feed**: 10
- **Database**: SQLite (intel.db)
- **Bind Address**: 127.0.0.1:8000
- **Theme**: Green (toggle in UI)
- **Discord Alerts**: Disabled (set WEBHOOK_URL to enable)

## Security Notes

✅ HTML sanitization from RSS  
✅ SQL injection protection (ORM)  
✅ XSS prevention (auto-escaping)  
✅ CORS enabled (configure for production)  
✅ WebSocket connection management  
✅ Duplicate prevention via hashing  

## Next Phases

### Phase 2 - Intelligence
- [ ] User accounts & auth
- [ ] Saved filter profiles
- [ ] AI topic clustering (OpenAI/local LLM)
- [ ] Feed health scoring
- [ ] Search & advanced filters
- [ ] Custom alert routing

### Phase 3 - Operations
- [ ] Docker containerization
- [ ] Linode VPS deployment
- [ ] Postgres database
- [ ] Redis caching
- [ ] Load balancing

### Phase 4 - Platform
- [ ] Mobile app (React Native)
- [ ] CLI tool
- [ ] API clients
- [ ] Browser extension

## How to Use

### 1. Start Backend
```bash
cd backend
python run.py
```

### 2. Open Frontend
```
http://localhost:8000
```

### 3. Watch RSS Stream
- Articles populate in real-time
- Toggle categories on/off
- Click titles to view sources
- Switch themes with button

### 4. Setup Discord (Optional)
- Get webhook URL from Discord server
- Set `DISCORD_WEBHOOK_URL` in `.env`
- High-severity items (8+) auto-notify

### 5. Customize Sources
- Edit `backend/app/config.py`
- Add your RSS feeds & categories
- Restart backend to load

## Success Metrics

✅ Code reviewed and validated  
✅ All ChatGPT issues fixed  
✅ Production-ready Phase 1  
✅ Clean architecture  
✅ Full documentation  
✅ Ready for team usage  
✅ Scalable to Phase 2/3  

## File Size Summary

```
Backend: ~15 KB (code)
Frontend: ~25 KB (code)
Docs: ~30 KB (README + QUICKSTART)
Total: ~70 KB
```

---

## 🚀 Ready to Deploy

Intel Terminal is **Phase 1 Complete** and ready for:
1. Local development
2. Testing with real RSS feeds
3. Customization with your sources
4. Discord integration
5. Scaling to Phase 2 features

**Start it now:**
```bash
python backend/run.py
```

Enjoy your intelligence dashboard! 🎉
