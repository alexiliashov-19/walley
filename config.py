"""
Bot Configuration — reads from environment variables or .env file.
Edit .env, not this file.
"""

import os

# ── Required ──
BOT_TOKEN   = os.getenv("BOT_TOKEN",   "YOUR_BOT_TOKEN_HERE")

# ── Video URLs (one per language) ──
VIDEO_URL_RO = os.getenv("VIDEO_URL_RO", "https://www.youtube.com/watch?v=C0DPdy98e4c")
VIDEO_URL_RU = os.getenv("VIDEO_URL_RU", "https://www.youtube.com/watch?v=eCHaiEjCDFM")

# ── Optional: booking page (Calendly, WhatsApp, etc.)
# If empty, bot sends a notification to ADMIN_CHAT_ID instead ──
CONSULTATION_URL = os.getenv("CONSULTATION_URL", "")

# ── Optional: your personal Telegram numeric ID for notifications ──
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID", "")
