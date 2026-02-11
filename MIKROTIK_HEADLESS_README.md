# MikroTik Master Scraper - Headless Mode

Run the MikroTik scraper as a daemon on a headless server with full SSH terminal control.

## Features

- **Daemon Mode**: Run as background service with RSS polling
- **CLI Control**: Start/stop daemon and manage settings via terminal
- **No GUI Required**: Perfect for SSH access and server environments
- **Persistent Storage**: All data stored as JSON files
- **Logging**: Full logging to console and optional log file
- **Statistics**: Track downloads and versions found

## Installation

```bash
# Make sure you have the dependencies installed
pip install requests

# Copy both files to your server
# - mikrotik_master.py (main engine)
# - mikrotik_headless.py (CLI wrapper)
```

## Quick Start

### Start Daemon (checks RSS every 15 minutes)
```bash
python mikrotik_headless.py --daemon start
```

### Check Daemon Status
```bash
python mikrotik_headless.py --daemon status
```

### Stop Daemon
```bash
python mikrotik_headless.py --daemon stop
```

### Check RSS Manually (one-time)
```bash
python mikrotik_headless.py --check-rss
```

### Scan Specific Version
```bash
python mikrotik_headless.py --scan-version 6.51
```

## Full Command Reference

### General Options
```bash
--output DIR          # Output directory (default: ./mikrotik_archive)
--workers N           # Number of download workers (default: 8)
--retries N           # Max retries per file (default: 3)
--log-file PATH       # Log file path (optional, auto-created in output dir)
```

### Daemon Commands
```bash
--daemon start        # Start daemon (RSS polling every 15 minutes)
--daemon stop         # Stop daemon
--daemon status       # Check if daemon is running
```

### Manual Operations
```bash
--check-rss           # Check RSS once and download new versions
--scan-version VER    # Scan specific version (e.g., 6.51)
--stats               # Display download statistics
--list-versions       # List all versions found
```

## Usage Examples

### Server Setup with Custom Directory
```bash
# Set up in /opt/mikrotik with 4 workers
python mikrotik_headless.py \
  --output /opt/mikrotik \
  --workers 4 \
  --retries 5 \
  --log-file /var/log/mikrotik-scraper.log \
  --daemon start
```

### Check Status via SSH
```bash
ssh user@server "cd /opt/mikrotik && python mikrotik_headless.py --daemon status"
```

### View Statistics
```bash
ssh user@server "python /opt/mikrotik/mikrotik_headless.py --stats"
```

### List Downloaded Versions
```bash
ssh user@server "python /opt/mikrotik/mikrotik_headless.py --list-versions"
```

### Manually Download a Version
```bash
ssh user@server "python /opt/mikrotik/mikrotik_headless.py --scan-version 6.50.5"
```

### Stop Daemon Remotely
```bash
ssh user@server "python /opt/mikrotik/mikrotik_headless.py --daemon stop"
```

## Running as a System Service (Optional)

### Using systemd (Linux)

Create `/etc/systemd/system/mikrotik-scraper.service`:

```ini
[Unit]
Description=MikroTik Master Scraper Daemon
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/opt/mikrotik
ExecStart=/usr/bin/python3 /opt/mikrotik/mikrotik_headless.py \
  --output /opt/mikrotik \
  --workers 8 \
  --log-file /var/log/mikrotik-scraper.log \
  --daemon start
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable mikrotik-scraper
sudo systemctl start mikrotik-scraper
sudo systemctl status mikrotik-scraper
```

## File Structure

After running, your output directory will contain:

```
mikrotik_archive/
├── found_versions.json       # List of all versions found
├── download_stats.json       # Download statistics
├── headless.log             # Detailed logs
├── .daemon.pid              # Daemon process ID (while running)
└── [version folders]/       # Downloaded files organized by version
    ├── 6.51/
    ├── 6.50.5/
    └── ...
```

## Monitoring

### Check Logs in Real-Time
```bash
tail -f /var/log/mikrotik-scraper.log
```

### Monitor Disk Usage
```bash
du -sh /opt/mikrotik
```

### Check What Versions Are Downloaded
```bash
python mikrotik_headless.py --list-versions
```

### View Download Stats
```bash
python mikrotik_headless.py --stats
```

## Troubleshooting

### Daemon Won't Start
```bash
# Check if another instance is running
python mikrotik_headless.py --daemon status

# Check logs
tail /opt/mikrotik/headless.log
```

### Permission Denied
```bash
# Make sure the output directory is writable
chmod -R 755 /opt/mikrotik
```

### RSS Feed Issues
```bash
# Try manually checking RSS
python mikrotik_headless.py --check-rss

# Check logs for specific errors
grep ERROR /opt/mikrotik/headless.log | tail -20
```

## SSH Automation

You can automate management via SSH in your own scripts:

```bash
#!/bin/bash
SERVER="user@mikrotik-server"
SCRAPER_PATH="/opt/mikrotik/mikrotik_headless.py"

# Check status
echo "Checking daemon status..."
ssh $SERVER "python $SCRAPER_PATH --daemon status"

# View statistics
echo "Getting statistics..."
ssh $SERVER "python $SCRAPER_PATH --stats"

# List versions
echo "Available versions..."
ssh $SERVER "python $SCRAPER_PATH --list-versions"
```

## Notes

- Daemon checks RSS every 15 minutes by default (hardcoded, can be modified)
- All data is persistent across restarts
- Logs are automatically created in the output directory
- The scraper respects rate limits and includes retry logic
- Perfect for arm, arm64, x86, and other architectures

## Support

For issues with the GUI version, see `mikrotik_master.py`.
For headless mode specific issues, check the log file and ensure dependencies are installed.
