# Intel Terminal v1.0 🔍

**Personal SIGINT Dashboard + RSS Intelligence Feed**

A retro-styled intelligence terminal for monitoring geopolitical, cybersecurity, AI, and technology news from custom RSS feeds. Real-time WebSocket updates, 9 visual themes, dual layout modes, auto-refresh, and category management.

![Terminal Green Theme](https://img.shields.io/badge/theme-Terminal%20Green-00ff00)
![Matrix Theme](https://img.shields.io/badge/theme-Matrix-00ff41)
![Pip--Boy Theme](https://img.shields.io/badge/theme-Pip--Boy-14fe17)

---

## ✨ Features

### Core
- **Real-time Streaming** - WebSocket live updates as articles arrive
- **34 Pre-configured Sources** - Cybersecurity, OSINT, Geopolitical, AI/ML, Tech news
- **Category Management** - 8 default categories with custom colors
- **Auto-Refresh** - Configurable intervals: 5s, 10s, 30s, 1min, 5min
- **Deduplication** - Hash-based duplicate detection across sources
- **Feed Management** - Add/remove RSS sources via UI

### Visual
- **9 Themes**:
  - 🖥️ Terminal Green (default)
  - 🟠 Amber LCD (classic CRT)
  - 🌈 Neon Rainbow (cyberpunk)
  - 🖖 LCARS (Star Trek)
  - 🔴 HAL 9000 (2001: A Space Odyssey)
  - 🟢 Matrix (with digital rain animation)
  - ☢️ Pip-Boy (Fallout 4)
  - 📺 Commodore 64 (retro 8-bit)
  - ⚠️ Half-Life HEV (Black Mesa)

- **2 Layout Modes**:
  - **Modern Cards** - Rich article cards with descriptions
  - **Classic IRC** - Minimalist chat-room style (`[HH:MM] <Source> Title`)

### Organization
- **Category Filters** - Toggle categories on/off in real-time
- **Color-Coded Sources** - Each source has a unique color
- **Severity Badges** - Visual severity indicators per article

---

## 🏗️ Architecture

```
intel-terminal/
├── backend/
│   ├── app/
│   │   ├── main.py         # FastAPI app, routes, startup
│   │   ├── config.py       # Configuration & defaults
│   │   ├── database.py     # SQLAlchemy setup
│   │   ├── models.py       # DB models (Category, Source, Article)
│   │   ├── rss_engine.py   # RSS fetcher + processor
│   │   ├── websocket.py    # WebSocket broadcast manager
│   │   ├── discord.py      # Discord webhook alerts
│   │   └── utils.py        # Utilities (hash, sanitize)
│   ├── requirements.txt
│   └── run.py              # Development server
├── frontend/
│   ├── index.html          # Main UI
│   ├── styles.css          # All 9 themes + layouts
│   ├── app.js              # WebSocket client + interactivity
│   └── nginx.conf          # Production nginx config
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
├── V2_ROADMAP.md           # Future features (AI triage, heat maps)
└── README.md
```

---

## 🚀 Quick Start

### Option A: Local Development (Recommended for Personal Use)

```powershell
# Clone and navigate
cd intel-terminal/backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Start backend (port 8001)
python run.py
```

Then open `frontend/index.html` in your browser, or serve it:
```powershell
cd ../frontend
python -m http.server 3000
# Open http://localhost:3000
```

### Option B: Docker (Recommended for Deployment)

```bash
# Build and run
docker compose up -d

# Access
# Frontend: http://localhost (port 80)
# Backend API: http://localhost/api
# WebSocket: ws://localhost/ws
```

Stop:
```bash
docker compose down
```

---

## ⚙️ Configuration

### Environment Variables

Create `backend/.env` from `.env.example`:

```env
# Database
DATABASE_URL=sqlite:///./intel.db

# RSS Settings
RSS_CHECK_INTERVAL=5           # Minutes between fetches
MAX_ARTICLES_PER_FEED=10       # Max articles per source per fetch

# Discord Alerts (optional)
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...

# Security
SECRET_KEY=your-secret-key-change-in-production
```

### Adding Custom RSS Sources

Via the UI:
1. Click the **+** button in the header
2. Fill in: Name, URL, Color, Category
3. Click "Add Feed"

Or edit `backend/app/config.py`:
```python
DEFAULT_SOURCES = [
    {
        "name": "Your Feed",
        "url": "https://example.com/rss",
        "color": "#ff5555",
        "category": "Cybersecurity"
    },
]
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/stats` | Source/article counts |
| GET | `/api/sources` | List all RSS sources |
| POST | `/api/sources` | Add new source |
| DELETE | `/api/sources/{id}` | Remove source |
| GET | `/api/categories` | List categories |
| POST | `/api/categories` | Create category |
| DELETE | `/api/categories/{id}` | Remove category |
| GET | `/api/articles` | Get all articles |
| POST | `/api/fetch` | Manually trigger RSS fetch |
| WS | `/ws` | WebSocket for live articles |

### Example: Add a Source
```bash
curl -X POST http://localhost:8001/api/sources \
  -H "Content-Type: application/json" \
  -d '{"name":"HackerNews","url":"https://hnrss.org/frontpage","color":"#ff6600","category":"Technology"}'
```

---

## 🎨 Themes Gallery

| Theme | Style | Special Effects |
|-------|-------|-----------------|
| Terminal Green | Classic hacker terminal | - |
| Amber LCD | Warm CRT monitor | - |
| Neon Rainbow | Cyberpunk gradient | Animated gradients |
| LCARS | Star Trek interface | Curved elements |
| HAL 9000 | 2001 spacecraft | Pulsing red glow |
| Matrix | Digital rain | Canvas rain animation |
| Pip-Boy | Fallout 4 | Scanline overlay |
| Commodore 64 | Retro 8-bit | Blinking cursor |
| Half-Life HEV | Black Mesa suit | Lambda symbol, HEV status |

---

## 🔧 Troubleshooting

### "Disconnected" Status
- Ensure backend is running: `python run.py`
- Check port: default is `8001` for local dev
- Check browser console for WebSocket errors

### Port 8000 Blocked
Windows sometimes reserves port 8000. The backend uses 8001 instead.
```powershell
netstat -ano | findstr 8000  # Check what's using it
```

### Docker Build Fails
Ensure Docker Desktop is running:
```powershell
docker info
```

### RSS Feed Not Loading
- Verify feed URL is valid RSS/Atom
- Some feeds require user-agent headers (not yet implemented)
- Check backend logs for parser errors

---

## 📋 Default Sources (34 feeds)

**Cybersecurity**: BleepingComputer, Krebs on Security, The Hacker News, Dark Reading, Schneier, Ars Technica Security, SecurityWeek, Naked Security

**OSINT**: Bellingcat, OSINT Curious, IntelTechniques

**Geopolitical**: Foreign Affairs, War on the Rocks, Council on Foreign Relations, Lawfare, DefenseOne, RAND

**AI/ML**: MIT Tech Review AI, VentureBeat AI, AI News, Google AI Blog, OpenAI Blog, DeepMind Blog

**Technology**: Ars Technica, Wired, The Verge, TechCrunch, Hacker News

**Privacy**: EFF, Privacy International, Restore Privacy, EPIC

**Science**: Nature News, Science Daily, Phys.org

---

## 🗺️ Roadmap (v2.0)

See [V2_ROADMAP.md](V2_ROADMAP.md) for planned features:

- 🤖 **AI Triage** - Auto-classify severity via:
  - Keyword scoring (built-in, free)
  - Local LLM (Ollama)
  - OpenAI API
  - Claude API
  - Manual triage buttons
- 🗺️ **Event Heat Map** - Geocode locations, visualize on world map
- 🏷️ **Hashtags** - Custom tagging system
- 📊 **Analytics** - Charts and trend detection
- 🔔 **Enhanced Alerts** - Slack, Telegram, email digests

---

## 📜 License

MIT License - Use freely, modify as needed.

---

## 🙏 Credits

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Backend framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - Database ORM
- [feedparser](https://feedparser.readthedocs.io/) - RSS parsing
- [APScheduler](https://apscheduler.readthedocs.io/) - Background job scheduling

Theme inspirations:
- Matrix digital rain
- Fallout Pip-Boy interface
- Star Trek LCARS
- Half-Life HEV suit
- HAL 9000 from 2001: A Space Odyssey

---

**Intel Terminal v1.0** - *Your personal intelligence feed*
