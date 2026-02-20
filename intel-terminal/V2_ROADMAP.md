# Intel Terminal v2.0 Roadmap

## Vision
Transform Intel Terminal from a feed aggregator into an intelligent threat detection and geopolitical awareness platform with AI-powered triage, location extraction, and event visualization.

---

## Planned Features

### 🤖 AI-Powered Triage System

Multiple triage backends will be supported. Users can choose based on their needs:

#### Option 1: Keyword Scoring (Built-in, No Setup)
- **Cost**: Free
- **Speed**: Instant
- **Privacy**: Full (no external calls)
- **How it works**: Pattern matching against curated keyword lists
  - `critical`: breach, zero-day, 0day, ransomware, APT, nation-state, exploit
  - `high`: attack, vulnerability, CVE, malware, backdoor, compromised
  - `medium`: security, threat, risk, warning, advisory
  - `low`: default

```python
# Example implementation
SEVERITY_KEYWORDS = {
    'critical': ['breach', 'zero-day', '0day', 'ransomware', 'APT', 'nation-state'],
    'high': ['attack', 'vulnerability', 'CVE-', 'malware', 'backdoor', 'hack'],
    'medium': ['security', 'threat', 'risk', 'warning', 'patch'],
}
```

#### Option 2: Local LLM (Ollama)
- **Cost**: Free
- **Speed**: 2-5 seconds per article
- **Privacy**: Full (runs locally)
- **Requirements**: 8GB+ RAM, Ollama installed
- **Models**: llama3, mistral, phi3

```bash
# Setup
ollama pull llama3

# Backend will call
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "Classify severity (critical/high/medium/low) and extract location: [article text]"
}'
```

#### Option 3: OpenAI API
- **Cost**: ~$0.001 per article (GPT-3.5-turbo)
- **Speed**: 1-2 seconds
- **Privacy**: Data sent to OpenAI
- **Setup**: Add `OPENAI_API_KEY` to .env

#### Option 4: Claude API (Anthropic)
- **Cost**: ~$0.001 per article (Claude 3 Haiku)
- **Speed**: 1-2 seconds
- **Privacy**: Data sent to Anthropic
- **Setup**: Add `ANTHROPIC_API_KEY` to .env

#### Option 5: Manual Triage
- Click-to-set severity buttons on each article
- Useful for training data collection
- Persists to database

### UI Integration Plan
```
Settings Panel:
┌─────────────────────────────────────┐
│ Triage Method: [Dropdown]           │
│ ○ Disabled                          │
│ ○ Keyword Scoring (Built-in)        │
│ ○ Local LLM (Ollama)                │
│ ○ OpenAI API                        │
│ ○ Claude API                        │
│ ○ Manual Only                       │
├─────────────────────────────────────┤
│ API Key: [••••••••••••]  [Test]     │
│ Model: [llama3 ▼]                   │
└─────────────────────────────────────┘
```

---

### 🗺️ Event Heat Map

Visualize where events are happening globally using extracted location data.

#### Technical Approach
1. **Location Extraction**: Use NLP/AI to extract place names from articles
2. **Geocoding**: Convert place names to lat/long (OpenStreetMap Nominatim - free)
3. **Mapping**: Leaflet.js with heat map overlay

```javascript
// Frontend addition
<div id="map" style="height: 400px;"></div>
<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
<script src="https://unpkg.com/leaflet.heat/dist/leaflet-heat.js"></script>
```

#### Data Flow
```
Article → AI extracts "Moscow", "Ukraine" → Geocode → [55.7558, 37.6173] → Heat map point
```

#### Heat Map Layers
- By category (Cybersecurity events vs Geopolitical)
- By severity (critical = red, high = orange, etc.)
- Time-based decay (older events fade)

---

### 🏷️ Hashtag System

User-defined tags for custom categorization beyond preset categories.

- Auto-suggest based on article content
- Click-to-add common tags
- Filter articles by hashtag
- Export by hashtag

---

### 📊 Analytics Dashboard

- Articles per day/week chart
- Category distribution pie chart
- Severity breakdown
- Source activity ranking
- Trend detection (keyword frequency over time)

---

### 🔔 Enhanced Alerting

- Per-category Discord channels
- Slack integration
- Email digest (daily/weekly)
- Pushover/Telegram notifications
- Custom alert rules (e.g., "any article mentioning 'CVE' AND 'critical'")

---

## Implementation Priority

| Feature | Complexity | Value | Priority |
|---------|------------|-------|----------|
| Keyword Scoring | Low | High | P1 |
| Manual Triage | Low | Medium | P1 |
| Ollama Integration | Medium | High | P2 |
| OpenAI/Claude API | Medium | High | P2 |
| Location Extraction | Medium | High | P2 |
| Heat Map | Medium | High | P2 |
| Hashtags | Low | Medium | P3 |
| Analytics Dashboard | Medium | Medium | P3 |
| Enhanced Alerting | Medium | Medium | P3 |

---

## Environment Variables (v2.0)

```env
# AI Triage
TRIAGE_METHOD=keyword  # keyword | ollama | openai | claude | manual
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3

# Geocoding
GEOCODE_ENABLED=true
NOMINATIM_URL=https://nominatim.openstreetmap.org

# Alerting
DISCORD_WEBHOOK_URL=...
SLACK_WEBHOOK_URL=...
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...
```

---

## Database Schema Additions (v2.0)

```sql
-- Add to articles table
ALTER TABLE articles ADD COLUMN locations JSON;  -- ["Moscow", "Ukraine"]
ALTER TABLE articles ADD COLUMN latitude REAL;
ALTER TABLE articles ADD COLUMN longitude REAL;
ALTER TABLE articles ADD COLUMN ai_summary TEXT;
ALTER TABLE articles ADD COLUMN hashtags JSON;   -- ["#cyber", "#russia"]
ALTER TABLE articles ADD COLUMN manually_triaged BOOLEAN DEFAULT FALSE;

-- New table for hashtags
CREATE TABLE hashtags (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    color TEXT,
    created_at TIMESTAMP
);

-- Article-hashtag relationship
CREATE TABLE article_hashtags (
    article_id INTEGER,
    hashtag_id INTEGER,
    PRIMARY KEY (article_id, hashtag_id)
);
```

---

## Contributing

This roadmap is a living document. Features will be implemented based on community feedback and practical utility.

---

*Intel Terminal v1.0 - Stable Release*  
*v2.0 Development - Coming Soon*
