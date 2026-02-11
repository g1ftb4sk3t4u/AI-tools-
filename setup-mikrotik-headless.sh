#!/bin/bash
# Quick setup script for MikroTik Headless Scraper on servers

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== MikroTik Headless Scraper Setup ===${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}Python3 not found. Installing...${NC}"
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip
fi

# Install dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
pip3 install requests --user

# Set paths
INSTALL_DIR="${1:-.}"
OUTPUT_DIR="${2:-$INSTALL_DIR/mikrotik_archive}"

echo -e "${BLUE}Installation directory: $INSTALL_DIR${NC}"
echo -e "${BLUE}Archive directory: $OUTPUT_DIR${NC}"

# Create directories
mkdir -p "$OUTPUT_DIR"
mkdir -p "$(dirname "$OUTPUT_DIR")"

# Copy scripts if needed
if [ ! -f "$INSTALL_DIR/mikrotik_master.py" ]; then
    echo -e "${YELLOW}mikrotik_master.py not found. Please copy it to $INSTALL_DIR/${NC}"
    exit 1
fi

if [ ! -f "$INSTALL_DIR/mikrotik_headless.py" ]; then
    echo -e "${YELLOW}mikrotik_headless.py not found. Please copy it to $INSTALL_DIR/${NC}"
    exit 1
fi

# Make executable
chmod +x "$INSTALL_DIR/mikrotik_headless.py"
chmod +x "$INSTALL_DIR/mikrotik_master.py"

# Test installation
echo -e "${BLUE}Testing installation...${NC}"
if python3 "$INSTALL_DIR/mikrotik_headless.py" --help > /dev/null; then
    echo -e "${GREEN}✓ Installation successful!${NC}"
else
    echo -e "${YELLOW}⚠ Installation test failed${NC}"
    exit 1
fi

# Setup systemd service (optional)
read -p "Setup as systemd service? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    SERVICE_USER="${3:-$(whoami)}"
    SERVICE_FILE="/tmp/mikrotik-scraper.service"
    
    cat > "$SERVICE_FILE" << EOF
[Unit]
Description=MikroTik Master Scraper Daemon
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$SERVICE_USER
WorkingDirectory=$INSTALL_DIR
ExecStart=/usr/bin/python3 $INSTALL_DIR/mikrotik_headless.py \\
  --output $OUTPUT_DIR \\
  --workers 8 \\
  --log-file $OUTPUT_DIR/headless.log \\
  --daemon start
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
    
    echo -e "${BLUE}Systemd service file created at: $SERVICE_FILE${NC}"
    echo "Copy it with: sudo cp $SERVICE_FILE /etc/systemd/system/"
    echo "Then run: sudo systemctl daemon-reload && sudo systemctl enable --now mikrotik-scraper"
fi

echo -e "${GREEN}=== Setup Complete ===${NC}"
echo -e "${BLUE}Quick commands:${NC}"
echo "  Start daemon:   python3 $INSTALL_DIR/mikrotik_headless.py --output $OUTPUT_DIR --daemon start"
echo "  Check status:   python3 $INSTALL_DIR/mikrotik_headless.py --output $OUTPUT_DIR --daemon status"
echo "  Stop daemon:    python3 $INSTALL_DIR/mikrotik_headless.py --output $OUTPUT_DIR --daemon stop"
echo "  View stats:     python3 $INSTALL_DIR/mikrotik_headless.py --output $OUTPUT_DIR --stats"
echo "  View versions:  python3 $INSTALL_DIR/mikrotik_headless.py --output $OUTPUT_DIR --list-versions"
echo ""
echo -e "${YELLOW}For more info, see MIKROTIK_HEADLESS_README.md${NC}"
