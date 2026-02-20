#!/bin/bash
# ============================================
# Intel Terminal - Linode Deployment Script
# ============================================
# Run this on a fresh Ubuntu 22.04 Linode
# Recommended: Nanode 1GB ($5/mo) or Linode 2GB ($12/mo)
#
# Usage:
#   curl -sSL https://raw.githubusercontent.com/g1ftb4sk3t4u/AI-tools-/main/intel-terminal/deploy/linode-setup.sh | bash
#
# Or manually:
#   wget https://raw.githubusercontent.com/g1ftb4sk3t4u/AI-tools-/main/intel-terminal/deploy/linode-setup.sh
#   chmod +x linode-setup.sh
#   ./linode-setup.sh
# ============================================

set -e  # Exit on error

echo "============================================"
echo "  Intel Terminal - Linode Setup"
echo "============================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Please run as root (sudo)${NC}"
    exit 1
fi

echo -e "${GREEN}[1/6]${NC} Updating system packages..."
apt-get update -qq
apt-get upgrade -y -qq

echo -e "${GREEN}[2/6]${NC} Installing Docker..."
# Remove old versions
apt-get remove -y docker docker-engine docker.io containerd runc 2>/dev/null || true

# Install prerequisites
apt-get install -y -qq \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker's official GPG key
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

# Set up repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
apt-get update -qq
apt-get install -y -qq docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Start Docker
systemctl start docker
systemctl enable docker

echo -e "${GREEN}[3/6]${NC} Creating app directory..."
mkdir -p /opt/intel-terminal
cd /opt/intel-terminal

echo -e "${GREEN}[4/6]${NC} Cloning Intel Terminal..."
if [ -d ".git" ]; then
    git pull
else
    git clone https://github.com/g1ftb4sk3t4u/AI-tools-.git temp
    mv temp/intel-terminal/* .
    mv temp/intel-terminal/.* . 2>/dev/null || true
    rm -rf temp
fi

echo -e "${GREEN}[5/6]${NC} Creating environment file..."
if [ ! -f ".env" ]; then
    cat > .env << 'EOF'
# Intel Terminal Configuration
# Edit these values as needed

# Discord Webhook (optional - leave empty to disable)
DISCORD_WEBHOOK_URL=

# Secret key for sessions (CHANGE THIS!)
SECRET_KEY=$(openssl rand -hex 32)

# Database (SQLite, stored in Docker volume)
DATABASE_URL=sqlite:///./data/intel.db

# RSS Settings
RSS_CHECK_INTERVAL=5
MAX_ARTICLES_PER_FEED=10
EOF
    # Generate actual secret key
    SECRET=$(openssl rand -hex 32)
    sed -i "s/\$(openssl rand -hex 32)/$SECRET/" .env
    echo -e "${YELLOW}Created .env file - edit /opt/intel-terminal/.env to add Discord webhook${NC}"
fi

echo -e "${GREEN}[6/6]${NC} Building and starting containers..."
docker compose up -d --build

# Get server IP
SERVER_IP=$(curl -s ifconfig.me)

echo ""
echo "============================================"
echo -e "${GREEN}  Intel Terminal is now running!${NC}"
echo "============================================"
echo ""
echo "  Access your dashboard:"
echo -e "  ${GREEN}http://${SERVER_IP}${NC}"
echo ""
echo "  Useful commands:"
echo "  - View logs:     docker compose logs -f"
echo "  - Stop:          docker compose down"
echo "  - Restart:       docker compose restart"
echo "  - Update:        git pull && docker compose up -d --build"
echo ""
echo "  Configuration:"
echo "  - Edit .env:     nano /opt/intel-terminal/.env"
echo "  - Add Discord:   Add DISCORD_WEBHOOK_URL to .env"
echo ""
echo "============================================"
echo ""

# Optional: Set up firewall
echo -e "${YELLOW}Setting up firewall (UFW)...${NC}"
apt-get install -y -qq ufw
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable
echo -e "${GREEN}Firewall configured (SSH, HTTP, HTTPS allowed)${NC}"

echo ""
echo -e "${GREEN}Setup complete! Bookmark http://${SERVER_IP} on your phone.${NC}"
