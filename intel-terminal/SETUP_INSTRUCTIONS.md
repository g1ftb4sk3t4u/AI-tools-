# Setup Instructions - Feed Management & RSS Fetching

## What We've Added

1. **Feed Management UI** - Add/Delete RSS feeds in the frontend
2. **API Endpoints** - Backend endpoints for feed management
3. **CSS Styling** - Terminal-style UI for feeds
4. **Auto-fetching** - Automatic RSS fetching every 5 minutes

## Implementation Steps

### Step 1: Update frontend/styles.css

Copy all content from `FRONTEND_STYLES.md` and add to the end of your `frontend/styles.css` file.

### Step 2: Update frontend/app.js

Replace your entire `frontend/app.js` with the code provided in this update. Key features:
- WebSocket connection with auto-reconnect
- Feed management (+ to add, ✕ to delete)
- Article filtering by category
- Real-time feed display
- Theme toggle
- Export functionality

### Step 3: Update backend/app/main.py

Add the following imports at the top:
```python
from sqlalchemy import delete, func
import asyncio
```

Then add these endpoints to your FastAPI app (before the last line):

**GET /api/sources** - List all RSS sources
**POST /api/sources** - Add new source
**DELETE /api/sources/{id}** - Delete source
**POST /api/fetch** - Manually trigger RSS fetch
**GET /api/articles** - Get articles with filtering
**GET /api/stats** - Dashboard statistics

See `API_ENDPOINTS.md` for complete endpoint code.

### Step 4: Test the Setup

1. Backend should be running: `python -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload`
2. Open frontend: http://127.0.0.1:8001
3. You should see "✓ Connected" status
4. Click "+ Add Feed" to test adding a custom source
5. Articles should populate from the 32 default sources

## Troubleshooting

### WebSocket shows "Disconnected"
- Backend must be running on port 8001
- Check browser console for connection errors
- Server might not have `/ws` endpoint - we'll need to add that

### No Articles Showing
- Check backend logs for RSS fetch errors
- Verify sources are being created (you saw the logs)
- Try clicking "Add Feed" manually to test API

### API Endpoints Not Working
- Make sure you added the new routes to main.py
- Restart the backend after changes
- Check FastAPI docs at http://127.0.0.1:8001/docs

## Files That Need Updating

- `frontend/app.js` - Replace entirely
- `frontend/styles.css` - Add new CSS at end
- `backend/app/main.py` - Add new endpoints

## Next: WebSocket Integration

For real-time feed updates, we need to:
1. Add `/ws` WebSocket endpoint to backend
2. Ensure articles are broadcast to connected clients
3. Test live feed population

This guide covers the UI infrastructure. The WebSocket connection will complete the real-time functionality.
