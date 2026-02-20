# Phase 2 & Deployment Guide

## Phase 2 Features Implementation

Phase 2 introduces user authentication, personalization, and advanced search capabilities.

### New Files Created

1. **auth.py** - JWT authentication with password hashing
   - `hash_password()` - Bcrypt password hashing
   - `verify_password()` - Verify stored passwords
   - `create_access_token()` - JWT token generation
   - `verify_token()` - Token validation middleware

2. **schemas.py** - Request/response validation using Pydantic
   - User management schemas
   - Authentication schemas
   - Advanced article search
   - Dashboard statistics

3. **models.py** (updated) - New User table for Phase 2
   - User authentication and preferences
   - Theme and alert settings
   - Watched keywords per user

### New Endpoints to Implement

```python
# Authentication
POST /api/auth/register       # Create new user
POST /api/auth/login          # Get access token
POST /api/auth/refresh        # Refresh token

# User Management
GET  /api/users/me            # Get current user
PUT  /api/users/me            # Update preferences
GET  /api/users/me/keywords   # Get watched keywords
POST /api/users/me/keywords   # Add keyword alert

# Advanced Search
POST /api/articles/search     # Search with filters
GET  /api/articles/trending   # Trending by category
GET  /api/articles/timeline   # Time-based view

# Analytics
GET  /api/stats/dashboard     # User dashboard stats
GET  /api/stats/categories    # Category breakdown
```

## Docker Deployment

### Local Testing with Docker Compose

```bash
# Build and run with Docker Compose
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop services
docker-compose down
```

Access the application:
- Frontend: http://localhost:80
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Production Configuration

1. **Environment Variables for Production**
   ```bash
   # Create .env.production
   DATABASE_URL=postgresql://user:pass@postgres:5432/intel_terminal
   SECRET_KEY=your-secure-random-key-here
   DISCORD_WEBHOOK_URL=https://discordapp.com/api/webhooks/...
   RSS_CHECK_INTERVAL=5
   ENVIRONMENT=production
   ```

2. **Use PostgreSQL instead of SQLite**
   - Edit docker-compose.yml to add PostgreSQL service
   - Update DATABASE_URL to postgres connection string
   - Run migrations: `alembic upgrade head`

3. **Security for Production**
   - Use strong SECRET_KEY (generate with `openssl rand -base64 32`)
   - Enable HTTPS (use nginx reverse proxy)
   - Set secure cookie flags
   - Use environment variables for all secrets
   - Implement rate limiting on auth endpoints

## Linode VPS Deployment

### Prerequisites
- Linode account with VPS running Ubuntu 22.04 LTS
- Domain name (optional but recommended)
- SSH access to your VPS

### Step 1: SSH into your Linode VPS

```bash
ssh root@your-linode-ip
```

### Step 2: Install Docker and Docker Compose

```bash
# Update system
apt update && apt upgrade -y

# Install Docker
apt install -y docker.io docker-compose-plugin

# Enable Docker
systemctl enable docker
systemctl start docker

# Add your user to docker group
usermod -aG docker $USER
```

### Step 3: Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/intel-terminal.git
cd intel-terminal
```

### Step 4: Configure Environment

```bash
cp backend/.env.example backend/.env

# Edit with your secrets
nano backend/.env

# Generate strong SECRET_KEY
openssl rand -base64 32
```

### Step 5: Deploy with Docker Compose

```bash
# Build and start
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f
```

### Step 6: Set Up Reverse Proxy (Nginx)

```bash
# Install Nginx
apt install -y nginx

# Create configuration
cat > /etc/nginx/sites-available/intel-terminal << 'EOF'
server {
    listen 80;
    server_name your-domain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
EOF

# Enable site
ln -s /etc/nginx/sites-available/intel-terminal /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default

# Test configuration
nginx -t

# Start Nginx
systemctl enable nginx
systemctl restart nginx
```

### Step 7: SSL Certificate with Let's Encrypt

```bash
# Install Certbot
apt install -y certbot python3-certbot-nginx

# Get certificate
certbot certonly --standalone -d your-domain.com

# Auto-renew
systemctl enable certbot.timer
```

### Step 8: Database Persistence

```bash
# Create data backup
docker compose exec backend sqlite3 /app/data/intel.db ".dump" > backup.sql

# Or with PostgreSQL:
docker compose exec postgres pg_dump -U intel_user intel_terminal > backup.sql
```

### Step 9: Monitoring and Updates

```bash
# Check container health
docker compose ps

# View logs
docker compose logs -f backend

# Update application
git pull origin main
docker compose up -d --build

# Prune old images
docker image prune -a
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using port
lsof -i :8000
# Kill it
kill -9 <PID>
```

### Database Connection Issues
```bash
# Check database file
ls -la backend/data/

# Reset database
rm backend/data/intel.db
docker compose restart backend
```

### WebSocket Connection Failed
```bash
# Ensure backend is healthy
curl http://localhost:8000/health

# Check firewall
ufw allow 8000/tcp
```

### Out of Disk Space on Linode
```bash
# Check usage
df -h

# Cleanup Docker
docker system prune -a --volumes
```

## Next Steps

1. ✅ Phase 2 authentication scaffolding complete
2. ⏳ Implement user registration/login endpoints
3. ⏳ Add user-specific article filters
4. ⏳ Create advanced search with AI clustering
5. ⏳ Set up monitoring and alerting
6. ⏳ Create mobile app (React Native)
