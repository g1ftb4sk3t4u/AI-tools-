import requests
import logging
from app.config import DISCORD_WEBHOOK_URL

logger = logging.getLogger(__name__)

async def send_discord_alert(title: str, link: str, source: str, severity: int = 0):
    """Send alert to Discord webhook"""
    
    if not DISCORD_WEBHOOK_URL:
        logger.debug("Discord webhook not configured")
        return
    
    # Color based on severity
    color_map = {
        9: 16711680,  # Red for critical
        8: 16744448,  # Orange for high
        7: 16776960,  # Yellow for medium
        5: 65535,     # Cyan for low
    }
    
    color = color_map.get(severity, 9999999)
    
    # Severity label
    severity_label = {
        10: "🔴 CRITICAL",
        9: "🔴 CRITICAL",
        8: "🟠 HIGH",
        7: "🟡 MEDIUM",
        5: "🔵 LOW",
    }.get(severity, "ℹ️ INFO")
    
    embed = {
        "title": title,
        "url": link,
        "description": f"**Source:** {source}\n**Severity:** {severity_label}",
        "color": color
    }
    
    payload = {
        "embeds": [embed]
    }
    
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5)
        response.raise_for_status()
        logger.info(f"Discord alert sent: {title[:50]}")
    except Exception as e:
        logger.error(f"Failed to send Discord alert: {e}")
