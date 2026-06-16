"""
Bot Configuration.
Edit .env on Railway (Variables tab) — never hardcode secrets here.
"""

import os

# ── Required ──────────────────────────────────
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# ── Admin Telegram username (WITHOUT @) ───────
# Consultation requests will be forwarded here as a message.
# The admin must have started a conversation with the bot at least once,
# OR use a numeric chat ID in ADMIN_CHAT_ID instead (see below).
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "bologanvictor")

# ── Alternative: numeric chat ID (more reliable) ──
# Get yours from @userinfobot. Leave empty if using ADMIN_USERNAME.
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID", "7309968901")

# ── Optional: external booking/consultation URL ───
# If set, the "Vreau consultație" button opens this link directly.
# If empty, bot sends a notification to admin instead.
# Examples:
#   https://calendly.com/victor-bologan/consultatie
#   https://wa.me/37360000000
CONSULTATION_URL = os.getenv("CONSULTATION_URL", "")

# ── Three videos ──────────────────────────────
# label  = button text shown to user
# title  = used inside the welcome message
# url    = full YouTube / Vimeo / any link
VIDEOS = {
    "v1": {
        "label": "🎬 Video 1 — Blocaje și venituri",
        "title": "Blocaje interioare și venituri",
        "url":   os.getenv("VIDEO_URL_1", "https://youtu.be/DlRGiBD27FM?si=l3m5sQoyiCVaM94q"),
    },
    "v2": {
        "label": "🎬 Video 2 — Studiu de caz",
        "title": "Studiu de caz: de la blocaj la rezultat",
        "url":   os.getenv("VIDEO_URL_2", "https://youtu.be/dwG5gXhxQzs?si=36hpYES5xNH3BOUc"),
    },
    "v3": {
        "label": "🎬 Video 3 — Reprogramarea subconștientului",
        "title": "Reprogramarea subconștientului",
        "url":   os.getenv("VIDEO_URL_3", "https://youtu.be/AkaRhHtIwB8?si=2ZFLwOLCuVZphDZu"),
    },
}
