# MikroTik Headless Quick Reference

## Common Commands

### From Local Machine (via SSH)

```bash
# Start daemon on server
ssh user@server.com "python3 /opt/mikrotik/mikrotik_headless.py --daemon start"

# Stop daemon
ssh user@server.com "python3 /opt/mikrotik/mikrotik_headless.py --daemon stop"

# Check daemon status
ssh user@server.com "python3 /opt/mikrotik/mikrotik_headless.py --daemon status"

# View all statistics
ssh user@server.com "python3 /opt/mikrotik/mikrotik_headless.py --stats"

# List downloaded versions
ssh user@server.com "python3 /opt/mikrotik/mikrotik_headless.py --list-versions"

# Manually check RSS for new versions
ssh user@server.com "python3 /opt/mikrotik/mikrotik_headless.py --check-rss"

# Download a specific version
ssh user@server.com "python3 /opt/mikrotik/mikrotik_headless.py --scan-version 6.51"

# View logs (live)
ssh user@server.com "tail -f /var/log/mikrotik.log"

# View disk usage
ssh user@server.com "du -sh /opt/mikrotik/archive"
```

## Configuration Options

```bash
--output DIR        # Output directory (default: ./mikrotik_archive)
--workers N         # Download workers (default: 8, adjust for server capacity)
--retries N         # Max retries (default: 3)
--log-file PATH     # Custom log file path
```

## Real-World Examples

### Example 1: Start with Custom Config
```bash
ssh user@server.com "python3 /opt/mikrotik/mikrotik_headless.py \
  --output /mnt/storage/mikrotik \
  --workers 4 \
  --log-file /var/log/mikrotik.log \
  --daemon start"
```

### Example 2: Download Specific Version (One-time)
```bash
ssh user@server.com "python3 /opt/mikrotik/mikrotik_headless.py \
  --output /opt/mikrotik/archive \
  --scan-version 6.51.3"
```

### Example 3: Check Everything
```bash
# Status
ssh user@server.com "python3 /opt/mikrotik/mikrotik_headless.py --daemon status"

# Versions
ssh user@server.com "python3 /opt/mikrotik/mikrotik_headless.py --list-versions"

# Stats
ssh user@server.com "python3 /opt/mikrotik/mikrotik_headless.py --stats"

# Disk
ssh user@server.com "du -sh /opt/mikrotik/archive"

# Recent Logs
ssh user@server.com "tail -20 /var/log/mikrotik.log"
```

### Example 4: Systemd Control (if installed)
```bash
# Start
ssh user@server.com "sudo systemctl start mikrotik-scraper"

# Stop
ssh user@server.com "sudo systemctl stop mikrotik-scraper"

# Status
ssh user@server.com "sudo systemctl status mikrotik-scraper"

# Logs
ssh user@server.com "sudo journalctl -u mikrotik-scraper -n 50"

# Restart
ssh user@server.com "sudo systemctl restart mikrotik-scraper"
```

## Daemon Behavior

- **Checks RSS** every 15 minutes (hardcoded)
- **Auto-downloads** any new versions found
- **Persists** all data to JSON files
- **Respects rate limits** and includes retry logic
- **Logs everything** to file and console

## File Locations on Server

```
/opt/mikrotik/
├── mikrotik_master.py
├── mikrotik_headless.py
└── archive/
    ├── found_versions.json      # All discovered versions
    ├── download_stats.json      # Statistics
    ├── headless.log            # Detailed logs
    ├── .daemon.pid             # PID while running
    └── [versions]/
        ├── 6.51/
        ├── 6.50.5/
        └── ...

/var/log/
└── mikrotik.log               # System logs (if configured)
```

## Performance Tips

- **Slow connection?** → Lower workers: `--workers 2`
- **Fast server?** → Higher workers: `--workers 16`
- **Large archive?** → Check disk: `df -h /opt/mikrotik`
- **High bandwidth?** → Monitor: `iftop`, `nethogs`

## Common Issues

| Issue | Solution |
|-------|----------|
| Daemon won't start | `rm /opt/mikrotik/archive/.daemon.pid && retry` |
| Permission denied | `chmod 755 /opt/mikrotik` |
| Out of disk | `du -sh /opt/mikrotik/archive/*/ \| sort -rh` |
| Slow downloads | Reduce `--workers` or check network |
| Missing versions | Manually run `--check-rss` |

## One-Line Setup (Copy-Paste)

```bash
# SSH to server, then paste:
cd /opt/mikrotik && python3 mikrotik_headless.py --output ./archive --workers 8 --log-file ./headless.log --daemon start && echo "Daemon started!" && python3 mikrotik_headless.py --daemon status
```

## One-Line Status Check (Copy-Paste)

```bash
# From local machine:
ssh user@server.com "python3 /opt/mikrotik/mikrotik_headless.py --daemon status && python3 /opt/mikrotik/mikrotik_headless.py --stats" | head -30
```

## Useful Shell Aliases (Add to ~/.bashrc)

```bash
# Add these to your ~/.bashrc for easy access
alias mikrotik-start='ssh user@server.com "python3 /opt/mikrotik/mikrotik_headless.py --daemon start"'
alias mikrotik-stop='ssh user@server.com "python3 /opt/mikrotik/mikrotik_headless.py --daemon stop"'
alias mikrotik-status='ssh user@server.com "python3 /opt/mikrotik/mikrotik_headless.py --daemon status"'
alias mikrotik-stats='ssh user@server.com "python3 /opt/mikrotik/mikrotik_headless.py --stats"'
alias mikrotik-versions='ssh user@server.com "python3 /opt/mikrotik/mikrotik_headless.py --list-versions"'
alias mikrotik-logs='ssh user@server.com "tail -f /var/log/mikrotik.log"'

# Then use:
# mikrotik-start
# mikrotik-status
# mikrotik-stats
```

## Help

```bash
python3 mikrotik_headless.py --help
```
