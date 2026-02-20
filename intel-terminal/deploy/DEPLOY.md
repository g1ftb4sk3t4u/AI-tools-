# Intel Terminal - Deployment Guide

## Quick Deploy to Linode

### 1. Create Linode
1. Go to [cloud.linode.com](https://cloud.linode.com)
2. Create → Linode
3. **Image**: Ubuntu 22.04 LTS
4. **Region**: Pick closest to you
5. **Plan**: Nanode 1GB ($5/mo) - plenty for this app
6. **Label**: intel-terminal
7. **Root Password**: Set a strong password
8. Create Linode

### 2. Connect via SSH
```bash
ssh root@YOUR_LINODE_IP
```

### 3. Run Setup Script
```bash
curl -sSL https://raw.githubusercontent.com/g1ftb4sk3t4u/AI-tools-/main/intel-terminal/deploy/linode-setup.sh | bash
```

That's it! Access at `http://YOUR_LINODE_IP`

---

## Manual Setup (Alternative)

```bash
# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com | sh

# Clone and run
git clone https://github.com/g1ftb4sk3t4u/AI-tools-.git
cd AI-tools-/intel-terminal
docker compose up -d
```

---

## Add Custom Domain (Optional)

### With Cloudflare (Free SSL)
1. Add domain to Cloudflare
2. Point A record to Linode IP
3. Enable Proxy (orange cloud)
4. SSL/TLS → Full

### With Let's Encrypt (Free SSL)
```bash
# Install Certbot
apt install certbot python3-certbot-nginx -y

# Get certificate
certbot --nginx -d yourdomain.com

# Auto-renewal is automatic
```

---

## Useful Commands

```bash
# View live logs
docker compose logs -f

# Restart services
docker compose restart

# Stop everything
docker compose down

# Update to latest
cd /opt/intel-terminal
git pull
docker compose up -d --build

# Check disk space
df -h

# Check memory
free -m
```

---

## Add Discord Webhook

```bash
# Edit environment
nano /opt/intel-terminal/.env

# Add your webhook URL:
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN

# Restart to apply
docker compose restart
```

---

## Backup Database

```bash
# Copy database out of Docker volume
docker cp intel-terminal-backend:/app/data/intel.db ./backup-$(date +%Y%m%d).db

# Restore
docker cp ./backup.db intel-terminal-backend:/app/data/intel.db
docker compose restart
```

---

## Estimated Costs

| Provider | Plan | RAM | Cost |
|----------|------|-----|------|
| Linode | Nanode | 1GB | $5/mo |
| Linode | Linode 2GB | 2GB | $12/mo |
| DigitalOcean | Basic | 1GB | $6/mo |
| Vultr | Cloud Compute | 1GB | $6/mo |

All are sufficient for Intel Terminal. 1GB RAM handles 50+ RSS sources easily.

---

## Troubleshooting

### Container won't start
```bash
docker compose logs backend
```

### Port 80 in use
```bash
# Check what's using it
lsof -i :80

# Kill it
systemctl stop nginx  # or apache2
```

### Out of memory
```bash
# Add swap
fallocate -l 1G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab
```

### RSS feeds not updating
```bash
# Trigger manual fetch
curl -X POST http://localhost/api/fetch
```
