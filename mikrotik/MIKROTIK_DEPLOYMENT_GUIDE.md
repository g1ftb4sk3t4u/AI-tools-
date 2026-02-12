# MikroTik Headless Scraper - Deployment Guide

Complete guide for deploying the MikroTik scraper on a headless server with SSH access.

## Architecture

```
Your Local Machine (SSH Client)
         ↓
  SSH Connection
         ↓
Headless Server (with scraper daemon)
    ├── mikrotik_headless.py (CLI interface)
    ├── mikrotik_master.py (engine)
    ├── mikrotik_archive/ (downloads)
    │   ├── found_versions.json
    │   ├── download_stats.json
    │   ├── headless.log
    │   └── versions/
    └── Daemon (background process)
```

## Step 1: Prepare Your Server

```bash
# SSH into your server
ssh user@your-server.com

# Update system
sudo apt-get update
sudo apt-get install -y python3 python3-pip

# Create a dedicated directory for the scraper
mkdir -p /opt/mikrotik
cd /opt/mikrotik
```

## Step 2: Copy Files to Server

**From your local machine:**

```bash
# Copy the scripts to the server
scp mikrotik_master.py user@your-server.com:/opt/mikrotik/
scp mikrotik_headless.py user@your-server.com:/opt/mikrotik/
scp setup-mikrotik-headless.sh user@your-server.com:/opt/mikrotik/
```

## Step 3: Run Setup Script

```bash
# SSH back to server
ssh user@your-server.com

# Make setup script executable
chmod +x /opt/mikrotik/setup-mikrotik-headless.sh

# Run setup
cd /opt/mikrotik
bash setup-mikrotik-headless.sh

# Follow prompts to set up systemd service (recommended)
```

## Step 4: Configure and Start

### Option A: Direct Start (Not Recommended - Dies with SSH)
```bash
python3 mikrotik_headless.py \
  --output /opt/mikrotik/archive \
  --workers 8 \
  --log-file /var/log/mikrotik.log \
  --daemon start
```

### Option B: Using nohup (Better)
```bash
nohup python3 /opt/mikrotik/mikrotik_headless.py \
  --output /opt/mikrotik/archive \
  --workers 8 \
  --log-file /var/log/mikrotik.log \
  --daemon start > /opt/mikrotik/startup.log 2>&1 &
```

### Option C: Using systemd (BEST - Persistent)

If you chose to setup systemd during installation:

```bash
# Enable and start
sudo systemctl enable mikrotik-scraper
sudo systemctl start mikrotik-scraper

# Check status
sudo systemctl status mikrotik-scraper

# View logs
sudo journalctl -u mikrotik-scraper -f
```

## Step 5: Manage from Your Local Machine

All commands executed via SSH from your local machine:

```bash
# Check if daemon is running
ssh user@your-server.com "python3 /opt/mikrotik/mikrotik_headless.py --daemon status"

# View statistics
ssh user@your-server.com "python3 /opt/mikrotik/mikrotik_headless.py --stats"

# List all versions
ssh user@your-server.com "python3 /opt/mikrotik/mikrotik_headless.py --list-versions"

# Download a specific version
ssh user@your-server.com "python3 /opt/mikrotik/mikrotik_headless.py --scan-version 6.51"

# Manually check RSS
ssh user@your-server.com "python3 /opt/mikrotik/mikrotik_headless.py --check-rss"

# View logs
ssh user@your-server.com "tail -f /var/log/mikrotik.log"

# Stop daemon
ssh user@your-server.com "python3 /opt/mikrotik/mikrotik_headless.py --daemon stop"
```

## Step 6: Automated Local Management Script

Create a script on your local machine for easy management:

**File: `manage-mikrotik.sh`**

```bash
#!/bin/bash

# Configuration
SERVER="user@your-server.com"
SCRAPER="/opt/mikrotik/mikrotik_headless.py"

if [ $# -eq 0 ]; then
    echo "Usage: ./manage-mikrotik.sh {start|stop|status|stats|versions|rss|scan VERSION}"
    exit 1
fi

case "$1" in
    start)
        echo "Starting daemon..."
        ssh $SERVER "python3 $SCRAPER --daemon start"
        ;;
    stop)
        echo "Stopping daemon..."
        ssh $SERVER "python3 $SCRAPER --daemon stop"
        ;;
    status)
        echo "Checking status..."
        ssh $SERVER "python3 $SCRAPER --daemon status"
        ;;
    stats)
        echo "=== Statistics ==="
        ssh $SERVER "python3 $SCRAPER --stats"
        ;;
    versions)
        echo "=== Downloaded Versions ==="
        ssh $SERVER "python3 $SCRAPER --list-versions"
        ;;
    rss)
        echo "Checking RSS..."
        ssh $SERVER "python3 $SCRAPER --check-rss"
        ;;
    scan)
        if [ -z "$2" ]; then
            echo "Usage: ./manage-mikrotik.sh scan VERSION"
            exit 1
        fi
        echo "Scanning version $2..."
        ssh $SERVER "python3 $SCRAPER --scan-version $2"
        ;;
    *)
        echo "Unknown command: $1"
        exit 1
        ;;
esac
```

**Usage:**

```bash
chmod +x manage-mikrotik.sh

./manage-mikrotik.sh start
./manage-mikrotik.sh status
./manage-mikrotik.sh stats
./manage-mikrotik.sh versions
./manage-mikrotik.sh stop
```

## Step 7: Monitor Downloads

### Check Disk Usage
```bash
ssh user@your-server.com "du -sh /opt/mikrotik/archive"
```

### Monitor in Real-Time
```bash
ssh user@your-server.com "tail -f /var/log/mikrotik.log"
```

### Archive Specific Versions
```bash
ssh user@your-server.com "tar -czf mikrotik-6.51.tar.gz /opt/mikrotik/archive/6.51"
```

### Download Archive to Local Machine
```bash
scp user@your-server.com:/opt/mikrotik/archive/6.51.tar.gz ./
```

## Troubleshooting

### Daemon won't start
```bash
# Check if process already running
ssh user@your-server.com "ps aux | grep mikrotik"

# Check if PID file is stale
ssh user@your-server.com "rm /opt/mikrotik/archive/.daemon.pid"

# Try starting again
ssh user@your-server.com "python3 /opt/mikrotik/mikrotik_headless.py --daemon start"
```

### Check logs for errors
```bash
ssh user@your-server.com "tail -100 /var/log/mikrotik.log | grep ERROR"
```

### Systemd service issues
```bash
# If using systemd
ssh user@your-server.com "sudo journalctl -u mikrotik-scraper -n 50"

# Restart service
ssh user@your-server.com "sudo systemctl restart mikrotik-scraper"
```

### Disk space issues
```bash
# Check available space
ssh user@your-server.com "df -h /opt/mikrotik"

# Find largest downloads
ssh user@your-server.com "du -sh /opt/mikrotik/archive/*/ | sort -rh | head -10"
```

## Advanced: Restore Existing Archive

If you already have downloads:

```bash
# Copy existing archive
scp -r /path/to/existing/archive/* user@your-server.com:/opt/mikrotik/archive/

# Regenerate JSON files
ssh user@your-server.com "python3 -c \"
from pathlib import Path
import json

archive = Path('/opt/mikrotik/archive')
versions = set()
for v_dir in archive.glob('*/'):
    if v_dir.name.startswith('.'):
        continue
    versions.add(v_dir.name)

with open(archive / 'found_versions.json', 'w') as f:
    json.dump({'versions': sorted(list(versions))}, f, indent=2)
\""

# Start daemon
ssh user@your-server.com "python3 /opt/mikrotik/mikrotik_headless.py --daemon start"
```

## Security Notes

1. **SSH Key Authentication**: Use SSH keys, not passwords
2. **Firewall**: Don't expose ports unnecessarily
3. **Permissions**: Keep files readable only by needed users
4. **Credentials**: Never hardcode credentials in scripts
5. **Logs**: Monitor for security events

## Performance Tuning

Adjust `--workers` based on server resources:

```bash
# Light server (1-2 cores)
python3 mikrotik_headless.py --workers 2 --daemon start

# Medium server (4-8 cores)
python3 mikrotik_headless.py --workers 6 --daemon start

# Heavy server (8+ cores)
python3 mikrotik_headless.py --workers 12 --daemon start
```

## Backup Strategy

```bash
# Daily backup to local machine
0 3 * * * ssh user@your-server.com "tar -czf /tmp/mikrotik-backup.tar.gz /opt/mikrotik/archive" && scp user@your-server.com:/tmp/mikrotik-backup.tar.gz ~/backups/mikrotik-$(date +\%Y\%m\%d).tar.gz
```

Add this to your crontab for automated daily backups.

## Support

For issues:
1. Check logs: `tail -f /var/log/mikrotik.log`
2. View status: `python3 /opt/mikrotik/mikrotik_headless.py --daemon status`
3. Check permissions: `ls -la /opt/mikrotik/`
4. Review MIKROTIK_HEADLESS_README.md for detailed command reference
