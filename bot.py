#!/usr/bin/env python3
"""
Telegram Bot — Victor Bologan Hypnotherapy Funnel
Romanian only 🇷🇴
Flow: /start → welcome + btn → video1 + btn → video2 + btn → video3 + btn → topic → warmup → consultation
"""

import logging
import asyncio
import hashlib
import time
import json
import urllib.request
from datetime import datetime, timedelta

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes, MessageHandler, filters,
)

from config import BOT_TOKEN, CONSULTATION_URL, ADMIN_USERNAME, ADMIN_CHAT_ID, VIDEOS, META_PIXEL_ID, META_ACCESS_TOKEN

from messages import MSG

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────
# Meta Conversions API
# ─────────────────────────────────────────────

def send_meta_event(event_name: str, user_id: int, username: str = None):
    """Send event to Meta Conversions API (server-side)."""
    if not META_PIXEL_ID or not META_ACCESS_TOKEN:
        logger.warning("Meta Pixel not configured, skipping event.")
        return

    # Hash external_id (Telegram user ID) as required by Meta
    external_id_hashed = hashlib.sha256(str(user_id).encode()).hexdigest()

    payload = {
        "data": [
            {
                "event_name": event_name,
                "event_time": int(time.time()),
                "action_source": "other",
                "user_data": {
                    "external_id": external_id_hashed,
                },
                "custom_data": {
                    "content_name": "Consultatie Victor Bologan",
                    "currency": "RON",
                },
            }
        ]
    }

    url = f"https://graph.facebook.com/v19.0/{META_PIXEL_ID}/events?access_token={META_ACCESS_TOKEN}"

    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=5) as resp:
            result = json.loads(resp.read().decode())
            logger.info(f"Meta event '{event_name}' sent for user {user_id}: {result}")
    except Exception as e:
        logger.error(f"Meta CAPI error: {e}")

# ─────────────────────────────────────────────
# State helper
# ─────────────────────────────────────────────

def get_state(context: ContextTypes.DEFAULT_TYPE) -> dict:
    if "state" not in context.user_data:
        context.user_data["state"] = {
            "step": "welcome",
            "videos_watched": 0,
            "topic_chosen": False,
            "joined_at": datetime.now().isoformat(),
        }
    return context.user_data["state"]

# ─────────────────────────────────────────────
# Keyboards
# ─────────────────────────────────────────────

def kb_get_video():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("▶️ Primește video-ul", callback_data="get_video")
    ]])

def kb_watched(video_num: int):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("✅ Am urmărit", callback_data=f"watched_{video_num}")
    ]])

def kb_topics():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(label, callback_data=cb)]
        for label, cb in MSG["topics"]
    ])

def kb_consultation():
    label = "📅 Vreau consultație"
    if CONSULTATION_URL:
        return InlineKeyboardMarkup([[InlineKeyboardButton(label, url=CONSULTATION_URL)]])
    return InlineKeyboardMarkup([[InlineKeyboardButton(label, callback_data="request_consultation")]])

def kb_reminder():
    label = "📅 Analizez cu Victor"
    if CONSULTATION_URL:
        return InlineKeyboardMarkup([[InlineKeyboardButton(label, url=CONSULTATION_URL)]])
    return InlineKeyboardMarkup([[InlineKeyboardButton(label, callback_data="request_consultation")]])

# ─────────────────────────────────────────────
# Scheduled reminders
# ─────────────────────────────────────────────

async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    chat_id = job.data["chat_id"]
    user_data = job.data["user_data"]
    state = user_data.get("state", {})

    if state.get("step") in ("video1_sent", "video2_sent", "video3_sent", "all_watched", "topic_chosen"):
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text=MSG["reminder_24h"],
                reply_markup=kb_reminder(),
            )
            context.job_queue.run_once(
                send_final_cta,
                when=timedelta(hours=24),
                data={"chat_id": chat_id, "user_data": user_data},
                name=f"final_cta_{chat_id}",
            )
        except Exception as e:
            logger.error(f"Reminder error {chat_id}: {e}")

async def send_final_cta(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    chat_id = job.data["chat_id"]
    user_data = job.data["user_data"]
    state = user_data.get("state", {})

    if state.get("step") != "consultation_requested":
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text=MSG["final_cta"],
                reply_markup=kb_consultation(),
            )
        except Exception as e:
            logger.error(f"Final CTA error {chat_id}: {e}")

# ─────────────────────────────────────────────
# Admin notification
# ─────────────────────────────────────────────

async def notify_admin(context: ContextTypes.DEFAULT_TYPE, user):
    target = ADMIN_CHAT_ID or (f"@{ADMIN_USERNAME.lstrip('@')}" if ADMIN_USERNAME else None)
    if not target:
        return
    try:
        text = (
            f"🔔 Cerere consultație nouă!\n\n"
            f"👤 {user.first_name} {user.last_name or ''}\n"
            f"📱 @{user.username or 'fără username'}\n"
            f"🆔 ID: {user.id}"
        )
        await context.bot.send_message(chat_id=target, text=text)
    except Exception as e:
        logger.error(f"Admin notify error: {e}")

# ─────────────────────────────────────────────
# Handlers
# ─────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"User: {user.id} @{user.username} {user.first_name}")

    context.user_data["state"] = {
        "step": "welcome",
        "videos_watched": 0,
        "topic_chosen": False,
        "joined_at": datetime.now().isoformat(),
    }

    # Meta: track bot start as ViewContent
    send_meta_event("ViewContent", user.id, user.username)

    await update.message.reply_text(
        MSG["welcome"],
        reply_markup=kb_get_video(),
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    state = get_state(context)
    chat_id = update.effective_chat.id
    user = update.effective_user

    # ── Trimite Video 1 ──────────────────────────────────────────────
    if data == "get_video":
        state["step"] = "video1_sent"
        state["videos_watched"] = 0

        video_text = MSG["video_1"].replace("{video_url_1}", VIDEOS["v1"]["url"])

        await query.edit_message_text(
            video_text,
            reply_markup=kb_watched(1),
        )

        if context.job_queue:
            for j in context.job_queue.get_jobs_by_name(f"reminder_{chat_id}"):
                j.schedule_removal()
            context.job_queue.run_once(
                send_reminder,
                when=timedelta(hours=24),
                data={"chat_id": chat_id, "user_data": context.user_data},
                name=f"reminder_{chat_id}",
            )

    # ── Am urmărit Video 1 → trimite Video 2 ────────────────────────
    elif data == "watched_1":
        state["videos_watched"] = 1
        state["step"] = "video2_sent"

        video_text = MSG["video_2"].replace("{video_url_2}", VIDEOS["v2"]["url"])

        await query.edit_message_text(
            video_text,
            reply_markup=kb_watched(2),
        )

    # ── Am urmărit Video 2 → trimite Video 3 ────────────────────────
    elif data == "watched_2":
        state["videos_watched"] = 2
        state["step"] = "video3_sent"

        video_text = MSG["video_3"].replace("{video_url_3}", VIDEOS["v3"]["url"])

        await query.edit_message_text(
            video_text,
            reply_markup=kb_watched(3),
        )

    # ── Am urmărit Video 3 → Întrebare despre temă ──────────────────
    elif data == "watched_3":
        state["videos_watched"] = 3
        state["step"] = "all_watched"

        await query.edit_message_text(
            MSG["after_video"],
            reply_markup=kb_topics(),
        )

    # ── Temă → warmup → ofertă consultație ──────────────────────────
    elif data.startswith("topic_"):
        state["topic_chosen"] = True
        state["topic"] = data
        state["step"] = "topic_chosen"

        await query.edit_message_reply_markup(reply_markup=None)

        await asyncio.sleep(1)
        await context.bot.send_message(chat_id=chat_id, text=MSG["warmup"])

        await asyncio.sleep(2)
        await context.bot.send_message(
            chat_id=chat_id,
            text=MSG["consultation"],
            reply_markup=kb_consultation(),
        )
        state["step"] = "consultation_offered"

    # ── Cerere consultație ───────────────────────────────────────────
    elif data == "request_consultation":
        state["step"] = "consultation_requested"
        await query.edit_message_text(MSG["received"])

        # Notify admin
        await notify_admin(context, user)

        # 🎯 Meta: track Lead event
        send_meta_event("Lead", user.id, user.username)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = get_state(context)
    step = state.get("step", "welcome")

    if step == "welcome":
        await update.message.reply_text(MSG["welcome"], reply_markup=kb_get_video())
    elif step in ("video1_sent", "video2_sent", "video3_sent"):
        await update.message.reply_text("Apasă «Am urmărit» când ești gata. 😊")
    else:
        await update.message.reply_text("Scrie /start pentru a reporni. 🔄")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Error: {context.error}", exc_info=context.error)

# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def main():
    logger.info("Starting VictorBologanBot...")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_error_handler(error_handler)
    logger.info("Bot running. Ctrl+C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
