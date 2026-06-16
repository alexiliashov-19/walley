"""
Bot Configuration.
Edit .env on Railway (Variables tab) — never hardcode secrets here.
"""

import os

# ── Required ──────────────────────────────────
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# ── Admin Telegram username (WITHOUT @) ───────
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "bologanvictor")

# ── Numeric chat ID (more reliable than username) ──
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID", "")

# ── Optional: external booking URL ───────────
CONSULTATION_URL = os.getenv("CONSULTATION_URL", "")

# ── Meta Conversions API ──────────────────────
META_PIXEL_ID     = os.getenv("META_PIXEL_ID", "1524453224847070")
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN", "EAAYlJzkZCZCFMBRl25khiWJGmXDgZBZAjsonoLIUZAaSIBaAKCmFZBcInriSrM2ZC9Yn0GDZAh6hKLZCZBbynB23D8VjU7yD1C10HKqhFV3FoTYVCVhwyjnhWAoU73liskcZC0FKiMFlGuEfTnZAPxj3ySeRWBSuozQFoXMTymXbZBEVESSNwtRlUwPJu1ocrGnrLM6k5gQZDZD")

# ── Three videos ──────────────────────────────
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
