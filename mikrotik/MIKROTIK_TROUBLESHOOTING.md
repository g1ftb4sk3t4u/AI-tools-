# MikroTik Headless - Troubleshooting Guide

## Issue: Daemon Won't Start

### Symptoms
```
[ERROR] Failed to start daemon
Process fails immediately
```

### Diagnosis
```bash
# Check if another instance is running
ps aux | grep mikrotik

# Check PID file
cat /opt/mikrotik/archive/.daemon.pid

# Check permissions
ls -la /opt/mikrotik/archive/

# Check Python
python3 --version

# Check imports
python3 -c "import requests; print('OK')"
```

### Solutions

**Solution 1: Clean PID file**
```bash
rm /opt/mikrotik/archive/.daemon.pid
python3 /opt/mikrotik/mikrotik_headless.py --daemon start
```

**Solution 2: Fix permissions**
```bash
chmod 755 /opt/mikrotik
chmod 755 /opt/mikrotik/archive
```

**Solution 3: Install missing dependencies**
```bash
pip3 install --upgrade requests
```

**Solution 4: Check if port conflict**
```bash
# Check if something is using standard ports
netstat -tuln | grep LISTEN
```

---

## Issue: Daemon Stops Unexpectedly

### Symptoms
```
Daemon was running, now it's not
No obvious error messages
```

### Diagnosis
```bash
# Check if process is still there
ps aux | grep python3 | grep mikrotik

# Check recent logs
tail -50 /var/log/mikrotik.log | grep -i "error\|exception\|traceback"

# Check if it crashed
dmesg | tail -20

# Check memory usage
free -h

# Check disk
df -h /opt/mikrotik
```

### Solutions

**Solution 1: Not enough memory**
```bash
# Check available memory
free -h

# If low, reduce workers
python3 /opt/mikrotik/mikrotik_headless.py \
  --workers 2 \
  --daemon start
```

**Solution 2: Out of disk space**
```bash
# Check usage
du -sh /opt/mikrotik/archive

# Free up space if needed
rm -rf /opt/mikrotik/archive/[oldest-version]/

# Restart daemon
python3 /opt/mikrotik/mikrotik_headless.py --daemon start
```

**Solution 3: Network timeout**
```bash
# Check network connectivity
ping download.mikrotik.com

# Check if RSS is accessible
curl -I https://mikrotik.com/download.rss

# Increase retry count
python3 /opt/mikrotik/mikrotik_headless.py \
  --retries 5 \
  --daemon start
```

**Solution 4: Log file permissions**
```bash
# If log file is unwritable
touch /var/log/mikrotik.log
sudo chmod 666 /var/log/mikrotik.log

# Or use a different log location
python3 /opt/mikrotik/mikrotik_headless.py \
  --log-file /opt/mikrotik/archive/headless.log \
  --daemon start
```

---

## Issue: Downloads Very Slow

### Symptoms
```
Few files per minute
Long wait times between downloads
```

### Diagnosis
```bash
# Check network speed
speedtest-cli

# Check active connections
netstat -an | grep ESTABLISHED | wc -l

# Check worker threads
ps aux | grep python

# Monitor download progress
tail -f /var/log/mikrotik.log | grep -i "download"
```

### Solutions

**Solution 1: Increase workers**
```bash
# Stop daemon
python3 /opt/mikrotik/mikrotik_headless.py --daemon stop

# Start with more workers
python3 /opt/mikrotik/mikrotik_headless.py \
  --workers 16 \
  --daemon start
```

**Solution 2: Check network**
```bash
# Test connectivity to CDN
time curl -I https://download.mikrotik.com/routeros

# Check for packet loss
ping -c 10 download.mikrotik.com
```

**Solution 3: Check server resources**
```bash
# CPU usage
top -bn1 | head -20

# Disk I/O
iostat -x 1 5

# If CPU/IO maxed, reduce workers
python3 /opt/mikrotik/mikrotik_headless.py \
  --workers 4 \
  --daemon stop
```

**Solution 4: Check rate limiting**
```bash
# Look for 429 or timeout errors
tail -100 /var/log/mikrotik.log | grep -i "429\|timeout\|rate"

# If rate limited, reduce workers and add delays
python3 /opt/mikrotik/mikrotik_headless.py \
  --workers 2 \
  --daemon start
```

---

## Issue: Out of Disk Space

### Symptoms
```
Downloads stop
"No space left on device" errors
```

### Diagnosis
```bash
# Check disk
df -h /opt/mikrotik

# Find largest directories
du -sh /opt/mikrotik/archive/*/ | sort -rh | head -10

# Check file sizes
find /opt/mikrotik/archive -type f -size +100M -exec ls -lh {} \;
```

### Solutions

**Solution 1: Delete old versions**
```bash
# List versions by size
du -sh /opt/mikrotik/archive/*/ | sort -rh

# Delete a specific version
rm -rf /opt/mikrotik/archive/6.40/

# Verify
df -h /opt/mikrotik
```

**Solution 2: Archive to external storage**
```bash
# Compress old versions
tar -czf /backup/mikrotik-6.45.tar.gz /opt/mikrotik/archive/6.45/

# Delete original
rm -rf /opt/mikrotik/archive/6.45/

# Verify
du -sh /opt/mikrotik/archive/
```

**Solution 3: Expand storage**
```bash
# Add new disk and mount at /mnt/new_storage

# Move archive
mv /opt/mikrotik/archive /mnt/new_storage/

# Update symlink
ln -s /mnt/new_storage/archive /opt/mikrotik/archive

# Restart daemon
python3 /opt/mikrotik/mikrotik_headless.py \
  --output /mnt/new_storage/archive \
  --daemon start
```

---

## Issue: Log File Growing Too Large

### Symptoms
```
Log file is gigabytes
Disk filling up from logs
```

### Diagnosis
```bash
# Check log size
ls -lh /var/log/mikrotik.log

# Count lines
wc -l /var/log/mikrotik.log

# See what's being logged
tail -1000 /var/log/mikrotik.log | cut -d' ' -f4 | sort | uniq -c | sort -rn
```

### Solutions

**Solution 1: Rotate logs with logrotate**
```bash
# Create /etc/logrotate.d/mikrotik
sudo cat > /etc/logrotate.d/mikrotik << EOF
/var/log/mikrotik.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    create 0644 $USER $USER
}
EOF

# Test it
sudo logrotate -f /etc/logrotate.d/mikrotik

# Verify
ls -la /var/log/mikrotik*
```

**Solution 2: Archive existing log**
```bash
# Stop daemon
python3 /opt/mikrotik/mikrotik_headless.py --daemon stop

# Archive and compress
gzip /var/log/mikrotik.log

# Restart
python3 /opt/mikrotik/mikrotik_headless.py --daemon start
```

**Solution 3: Change log level**
You can modify `mikrotik_headless.py` to use DEBUG vs INFO level logging.

---

## Issue: Can't SSH to Server

### Symptoms
```
"Connection refused"
"Permission denied"
"Network unreachable"
```

### Diagnosis
```bash
# From local machine
ssh -v user@server.com     # verbose mode shows what's happening

# Check if server is reachable
ping server.com

# Check SSH service on server
ssh user@server.com "systemctl status ssh"
```

### Solutions

**Solution 1: SSH key issues**
```bash
# Generate SSH key (if you don't have one)
ssh-keygen -t ed25519

# Copy key to server
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@server.com

# Test
ssh user@server.com "echo OK"
```

**Solution 2: Firewall blocking**
```bash
# On server, check firewall
sudo ufw status

# Allow SSH
sudo ufw allow 22/tcp

# On local machine, check outbound
telnet server.com 22
```

**Solution 3: Wrong IP/hostname**
```bash
# Verify hostname/IP
nslookup server.com

# Try IP directly
ssh user@x.x.x.x
```

---

## Issue: Daemon Status Shows "Not Running" But Process Exists

### Symptoms
```
ps aux shows python3 process
--daemon status says not running
```

### Diagnosis
```bash
# Check PID file
cat /opt/mikrotik/archive/.daemon.pid

# Check actual process
ps aux | grep python3 | grep mikrotik

# Compare PIDs
ps aux | grep [PID]
```

### Solutions

**Solution 1: Stale PID file**
```bash
# Remove stale PID
rm /opt/mikrotik/archive/.daemon.pid

# Check status
python3 /opt/mikrotik/mikrotik_headless.py --daemon status
```

**Solution 2: Process is hung**
```bash
# Kill the hung process
pkill -f "python3.*mikrotik_headless"

# Remove PID file
rm /opt/mikrotik/archive/.daemon.pid

# Restart
python3 /opt/mikrotik/mikrotik_headless.py --daemon start
```

---

## Issue: Versions Not Showing Up

### Symptoms
```
--list-versions shows nothing
But daemon is running
```

### Diagnosis
```bash
# Check if JSON file exists
ls -la /opt/mikrotik/archive/found_versions.json

# Check contents
cat /opt/mikrotik/archive/found_versions.json

# Check if daemon is working
tail -20 /var/log/mikrotik.log | grep -i "download\|version"
```

### Solutions

**Solution 1: Daemon hasn't run yet**
```bash
# Wait - daemon checks RSS every 15 minutes
sleep 15m

# Or manually check
python3 /opt/mikrotik/mikrotik_headless.py --check-rss
```

**Solution 2: RSS is down**
```bash
# Check if RSS is accessible
curl -I https://mikrotik.com/download.rss

# Try manually
python3 /opt/mikrotik/mikrotik_headless.py --check-rss
```

**Solution 3: No space/permissions**
```bash
# Check disk
df -h /opt/mikrotik/archive

# Check permissions
ls -la /opt/mikrotik/archive/

# If issues, fix:
chmod 755 /opt/mikrotik/archive
```

---

## Quick Diagnostic Commands

Run these to get a full picture:

```bash
# All-in-one diagnostic
echo "=== DAEMON STATUS ===" && \
python3 /opt/mikrotik/mikrotik_headless.py --daemon status && \
echo -e "\n=== PROCESS ===" && \
ps aux | grep "[m]ikrotik_headless" && \
echo -e "\n=== DISK USAGE ===" && \
df -h /opt/mikrotik && \
echo -e "\n=== VERSIONS ===" && \
python3 /opt/mikrotik/mikrotik_headless.py --list-versions | head -10 && \
echo -e "\n=== STATS ===" && \
python3 /opt/mikrotik/mikrotik_headless.py --stats && \
echo -e "\n=== RECENT LOGS ===" && \
tail -5 /var/log/mikrotik.log
```

## Getting Help

If issues persist:

1. Collect diagnostics:
   ```bash
   mkdir -p ~/mikrotik-debug
   python3 /opt/mikrotik/mikrotik_headless.py --daemon status > ~/mikrotik-debug/status.txt
   python3 /opt/mikrotik/mikrotik_headless.py --stats > ~/mikrotik-debug/stats.txt
   tail -100 /var/log/mikrotik.log > ~/mikrotik-debug/logs.txt
   ps aux | grep mikrotik > ~/mikrotik-debug/processes.txt
   df -h > ~/mikrotik-debug/disk.txt
   ```

2. Review logs carefully - most issues are in there

3. Check: MIKROTIK_HEADLESS_README.md and MIKROTIK_DEPLOYMENT_GUIDE.md

4. Try running manually (without daemon) to see real-time errors:
   ```bash
   python3 /opt/mikrotik/mikrotik_headless.py --check-rss
   ```
