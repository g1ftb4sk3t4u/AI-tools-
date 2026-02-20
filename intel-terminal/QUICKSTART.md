# Intel Terminal - Quick Start Guide

## 🚀 5-Minute Setup

### Prerequisites
- Python 3.8+
- pip
- Git

### Step 1: Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it - Choose based on your shell:

# Windows PowerShell:
venv\Scripts\Activate.ps1

# Windows Command Prompt (cmd.exe):
venv\Scripts\activate.bat

# Git Bash / MinGW on Windows:
source venv/Scripts/activate

# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure (Optional)

Create `.env` file in `backend/` directory:

```bash
cp .env.example .env
```

Edit `.env` if you want Discord alerts:

```env
DISCORD_WEBHOOK_URL=https://discordapp.com/api/webhooks/YOUR_ID/YOUR_TOKEN
RSS_CHECK_INTERVAL=5
```

### Step 3: Run Backend

```bash
# Using the run script (simple):
python run.py

# OR using uvicorn directly (recommended for now):
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```

You should see:
```
INFO:     Intel Terminal starting...
INFO:     Created category: Cybersecurity
INFO:     Created source: BleepingComputer
...
INFO:     Uvicorn running on http://127.0.0.1:8001
```

### Step 4: Open Frontend

Open your browser:
```
http://127.0.0.1:8001
```

You should see:
- **INTEL TERMINAL v1.0** in the title
- "✓ Connected" status indicator
- Green terminal aesthetic
- Left sidebar with feed management
- Populated feed with RSS articles

## 🎮 Using the Terminal

### Feed Management
- **+ Add Feed** - Add custom RSS source with URL
- **✕ Delete Feed** - Remove feed from tracking

### Theme Toggle
- Click **🎨 Color** to switch to multi-color theme
- Click **🟢 Green** to return to classic green

### Category Filters
- Check/uncheck categories in left sidebar
- Only checked categories display in feed

### Quick Commands
- **Clear Feed** - Empty the display
- **Export** - Download all articles as JSON

### Viewing Articles
- Articles show in feed with source, category, and severity
- Color-coded by source and severity level
- Click "Read More →" to open article source link
- Real-time WebSocket streaming from backend

## 📊 What's Happening

### Backend
- ✅ Database initialized (`intel.db`)
- ✅ Default categories created (Cybersecurity, Geopolitical, Tech, OSINT)
- ✅ Default RSS sources added
- ✅ Scheduler fetching feeds every 5 minutes
- ✅ WebSocket streaming articles to frontend

### Frontend
- ✅ Connected to WebSocket
- ✅ Displaying real-time articles
- ✅ Color-coding by source and severity
- ✅ Automatic deduplication
- ✅ Theme toggling

## 🔧 Adding Custom Sources

Edit `backend/app/config.py`:

```python
DEFAULT_SOURCES = [
    # ... existing sources ...
    {
        "name": "My Custom Feed",
        "url": "https://example.com/feed.xml",
        "color": "#ffff00",  # Yellow
        "category": "Tech"   # Must exist or create it
    }
]
```

Restart backend to pick up changes.

## 🚨 Troubleshooting

### "Connecting..." but never connects
1. Check backend is running: `http://localhost:8000/api/health`
2. You should see: `{"status": "online", ...}`
3. If not, check backend console for errors
4. Try stopping and restarting backend

### No articles appearing
1. Check RSS sources are valid
2. Backend logs should show fetch messages
3. Wait up to 5 minutes for first fetch
4. Or lower `RSS_CHECK_INTERVAL` temporarily

### Discord not working
1. Verify `DISCORD_WEBHOOK_URL` in `.env`
2. Test webhook URL in browser (should return 401)
3. Only articles with severity >= 8 send alerts
4. Check backend logs for webhook errors

## 📈 Next Steps (Phase 2)

- User accounts & saved filters
- AI topic clustering
- Advanced search
- Feed reliability monitoring
- Mobile app support

## 📝 Logs

Backend logs to console. View them in the terminal where you ran `python run.py`.

For debug logging, edit `backend/app/main.py`:
```python
logging.basicConfig(level=logging.DEBUG)  # Instead of INFO
```

## 🆘 Getting Help

1. Check backend console for errors
2. Check browser console (F12) for frontend errors
3. Verify `.env` configuration
4. Try clearing browser cache and reloading

---

**Enjoy your Intel Terminal!** 🎉
