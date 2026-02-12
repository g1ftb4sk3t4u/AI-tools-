# MikroTik Master Scraper - Headless Edition

**Now with both GUI and Headless (CLI) modes!**

Run the MikroTik scraper:
- 🖥️ **GUI Mode** - Interactive desktop application (original)
- 🖤 **Headless Mode** - Terminal/SSH server application (NEW!)

---

## Quick Start (Choose Your Path)

### 🖥️ GUI Mode (Desktop)
```bash
python3 mikrotik_master.py
```
See the original tkinter GUI with live monitoring.

### 🖤 Headless Mode (Server/SSH)
```bash
# Start daemon
python3 mikrotik_headless.py --daemon start

# Check status
python3 mikrotik_headless.py --daemon status

# View stats
python3 mikrotik_headless.py --stats
```

Manage entirely from terminal/SSH.

---

## What's New: Headless Features

✅ **Daemon Mode** - Run as background service  
✅ **SSH Control** - Manage from your local machine  
✅ **Terminal Interface** - Full CLI with options  
✅ **Systemd Compatible** - Auto-restart on reboot  
✅ **Flexible Configuration** - Control workers, retries, output paths  
✅ **Logging** - Full audit trail to file and console  
✅ **Statistics** - Track downloads and versions  

---

## Files Overview

```
Core Files:
├── mikrotik_master.py           (Original GUI - unchanged)
├── mikrotik_headless.py         (NEW - CLI/headless mode)
└── setup-mikrotik-headless.sh   (Setup script)

Documentation (Start Here!):
├── MIKROTIK_DOCS_INDEX.md       (Navigation guide - READ THIS FIRST)
├── MIKROTIK_HEADLESS_SUMMARY.md (Quick overview - 5 min read)
├── MIKROTIK_DEPLOYMENT_GUIDE.md (How to deploy - 15 min read)
├── MIKROTIK_HEADLESS_README.md  (Complete reference - detailed)
├── MIKROTIK_QUICK_REFERENCE.md  (Copy-paste commands - handy)
└── MIKROTIK_TROUBLESHOOTING.md  (Problem solving guide)
```

---

## Choose Your Documentation

### 🚀 I Want to Get Started (5 min)
→ Read: **MIKROTIK_DOCS_INDEX.md** then **MIKROTIK_HEADLESS_SUMMARY.md**

### 📖 I Want to Deploy to Server (15 min)
→ Read: **MIKROTIK_DEPLOYMENT_GUIDE.md**

### ⚡ I Want Quick Commands (Copy-Paste)
→ Use: **MIKROTIK_QUICK_REFERENCE.md**

### 🔍 I Want All Details (Reference)
→ Check: **MIKROTIK_HEADLESS_README.md**

### 🐛 I'm Having Issues
→ Go to: **MIKROTIK_TROUBLESHOOTING.md**

---

## Headless Mode Commands

```bash
# Daemon Control
python3 mikrotik_headless.py --daemon start      # Start
python3 mikrotik_headless.py --daemon stop       # Stop
python3 mikrotik_headless.py --daemon status     # Check status

# Manual Operations
python3 mikrotik_headless.py --check-rss         # Check once
python3 mikrotik_headless.py --scan-version 6.51 # Get specific version

# Information
python3 mikrotik_headless.py --stats             # View statistics
python3 mikrotik_headless.py --list-versions     # List all versions

# Configuration
python3 mikrotik_headless.py --output /path      # Custom output dir
python3 mikrotik_headless.py --workers 8         # Number of workers
python3 mikrotik_headless.py --retries 3         # Retry count
```

---

## Remote SSH Control (From Your Computer)

```bash
# Check if it's running
ssh user@server "python3 /opt/mikrotik/mikrotik_headless.py --daemon status"

# View stats
ssh user@server "python3 /opt/mikrotik/mikrotik_headless.py --stats"

# Get all versions
ssh user@server "python3 /opt/mikrotik/mikrotik_headless.py --list-versions"

# Stop it
ssh user@server "python3 /opt/mikrotik/mikrotik_headless.py --daemon stop"
```

---

## System Requirements

### For GUI Mode
- Python 3.6+
- `requests` library: `pip install requests`
- `tkinter` (usually included with Python)
- Display (X11, Windows, macOS)

### For Headless Mode
- Python 3.6+
- `requests` library: `pip install requests`
- SSH access (optional, for remote control)
- Terminal/shell

---

## Installation

### Quick Install (Headless)
```bash
# 1. Install Python and pip
sudo apt-get install python3 python3-pip

# 2. Install dependencies
pip3 install requests

# 3. Copy files to server
scp mikrotik_master.py user@server:/opt/mikrotik/
scp mikrotik_headless.py user@server:/opt/mikrotik/

# 4. Make executable
chmod +x /opt/mikrotik/mikrotik_headless.py

# 5. Start
python3 /opt/mikrotik/mikrotik_headless.py --daemon start
```

### Automated Setup
```bash
bash setup-mikrotik-headless.sh
```

For detailed instructions, see **MIKROTIK_DEPLOYMENT_GUIDE.md**

---

## Real-World Usage

### Scenario 1: "I Want to Archive MikroTik Versions on a Server"
```bash
# Deploy headless version
scp mikrotik_headless.py user@myserver:/opt/mikrotik/

# SSH to server and start
ssh user@myserver "python3 /opt/mikrotik/mikrotik_headless.py --daemon start"

# Later, check from your machine
ssh user@myserver "python3 /opt/mikrotik/mikrotik_headless.py --stats"
```

### Scenario 2: "I Want to Monitor Downloads from My Desktop"
```bash
# Start GUI locally
python3 mikrotik_master.py

# Or check headless server from terminal
watch -n 30 'ssh user@server "python3 /opt/mikrotik/mikrotik_headless.py --stats"'
```

### Scenario 3: "I Want Automated Daily Backups"
```bash
# Add to crontab (checks every 6 hours)
0 */6 * * * ssh user@server "python3 /opt/mikrotik/mikrotik_headless.py --check-rss"

# Monitor locally
0 * * * * python3 /path/to/monitor.py >> ~/mikrotik-monitor.log
```

---

## Comparison: GUI vs Headless

| Aspect | GUI | Headless |
|--------|-----|----------|
| **Interface** | Graphical | Terminal |
| **Remote Access** | Need tunneling | Direct SSH |
| **Server Friendly** | No | Yes ✓ |
| **Background Running** | Window must stay open | True daemon |
| **Automation** | Manual only | Fully scriptable |
| **Resource Usage** | ~100MB | ~20MB |
| **Use Case** | Interactive | Production servers |

**Both work perfectly.** Choose based on your use case.

---

## Next Steps

1. **Start Here**: Read [MIKROTIK_DOCS_INDEX.md](MIKROTIK_DOCS_INDEX.md)
2. **Then Read**: [MIKROTIK_HEADLESS_SUMMARY.md](MIKROTIK_HEADLESS_SUMMARY.md)
3. **Deploy**: Follow [MIKROTIK_DEPLOYMENT_GUIDE.md](MIKROTIK_DEPLOYMENT_GUIDE.md)
4. **Use Daily**: Reference [MIKROTIK_QUICK_REFERENCE.md](MIKROTIK_QUICK_REFERENCE.md)
5. **Troubleshoot**: Check [MIKROTIK_TROUBLESHOOTING.md](MIKROTIK_TROUBLESHOOTING.md) if needed

---

## Features Comparison

### Both Modes Include:
✅ MikroTik CDN crawling  
✅ RSS feed polling  
✅ Automatic version detection  
✅ Parallel downloads  
✅ Retry logic  
✅ Version/architecture filtering  
✅ Persistent statistics  
✅ Concurrent operations  

### GUI Only:
- Real-time visual monitoring
- Interactive controls
- Settings dialogs

### Headless Only:
- No GUI overhead
- SSH control
- Daemon mode
- Systemd integration
- Scriptable automation

---

## Getting Help

**Can't find what you need?**

1. Check the **MIKROTIK_DOCS_INDEX.md** for navigation
2. Search **MIKROTIK_QUICK_REFERENCE.md** for commands
3. Look up your issue in **MIKROTIK_TROUBLESHOOTING.md**
4. See detailed info in **MIKROTIK_HEADLESS_README.md**

---

## Example: Complete Deployment

```bash
# On server
mkdir -p /opt/mikrotik
cd /opt/mikrotik

# Get files (via scp from your machine)
# scp *.py user@server:/opt/mikrotik/

# Install
pip3 install requests

# Start daemon
python3 mikrotik_headless.py \
  --output /opt/mikrotik/archive \
  --workers 8 \
  --log-file /var/log/mikrotik.log \
  --daemon start

# From your machine, check status anytime
ssh user@server "python3 /opt/mikrotik/mikrotik_headless.py --stats"
```

**That's it!** You now have a production-ready MikroTik scraper.

---

## Version Info

- **GUI Version**: Unchanged (tkinter-based)
- **Headless Version**: New CLI-based interface
- **Engine**: Shared between both modes
- **Python**: 3.6+
- **Dependencies**: requests

---

## License & Attribution

Original concept and implementation for GUI version.
Headless enhancement maintains full compatibility while adding server capabilities.

---

**Start with**: [MIKROTIK_DOCS_INDEX.md](MIKROTIK_DOCS_INDEX.md)
