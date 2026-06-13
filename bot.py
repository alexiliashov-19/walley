#!/usr/bin/env python3
"""
Telegram Bot — Victor Bologan Hypnotherapy Funnel
Bilingual: Romanian 🇷🇴 / Russian 🇷🇺
"""

import logging
import asyncio
from datetime import datetime, timedelta

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes, MessageHandler, filters,
)

from config import BOT_TOKEN, CONSULTATION_URL, ADMIN_CHAT_ID, VIDEO_URL_RO, VIDEO_URL_RU
from messages import MESSAGES, LANG_SELECT_TEXT

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def get_state(context: ContextTypes.DEFAULT_TYPE) -> dict:
    if "state" not in context.user_data:
        context.user_data["state"] = {
            "step": "lang_select",
            "lang": None,
            "video_sent": False,
            "watched": False,
            "topic_chosen": False,
            "joined_at": datetime.now().isoformat(),
        }
    return context.user_data["state"]

def t(lang: str, key: str) -> str:
    return MESSAGES[lang][key]

def get_video_url(lang: str) -> str:
    return VIDEO_URL_RO if lang == "RO" else VIDEO_URL_RU

# ─────────────────────────────────────────────
# Keyboards
# ─────────────────────────────────────────────

def kb_lang_select():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("🇷🇴 Română", callback_data="lang_RO"),
        InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_RU"),
    ]])

def kb_get_video(lang):
    return InlineKeyboardMarkup([[InlineKeyboardButton(t(lang, "btn_get_video"), callback_data="get_video")]])

def kb_watched(lang):
    return InlineKeyboardMarkup([[InlineKeyboardButton(t(lang, "btn_watched"), callback_data="watched")]])

def kb_topics(lang):
    return InlineKeyboardMarkup([[InlineKeyboardButton(label, callback_data=cb)] for label, cb in t(lang, "topics")])

def kb_consultation(lang):
    label = t(lang, "btn_consultation")
    if CONSULTATION_URL:
        return InlineKeyboardMarkup([[InlineKeyboardButton(label, url=CONSULTATION_URL)]])
    return InlineKeyboardMarkup([[InlineKeyboardButton(label, callback_data="request_consultation")]])

def kb_reminder(lang):
    label = t(lang, "btn_reminder_consult")
    if CONSULTATION_URL:
        return InlineKeyboardMarkup([[InlineKeyboardButton(label, url=CONSULTATION_URL)]])
    return InlineKeyboardMarkup([[InlineKeyboardButton(label, callback_data="request_consultation")]])

# ─────────────────────────────────────────────
# Scheduled jobs
# ─────────────────────────────────────────────

async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    chat_id = job.data["chat_id"]
    user_data = job.data["user_data"]
    state = user_data.get("state", {})
    lang = state.get("lang", "RO")

    if state.get("step") in ("watched", "topic_chosen", "video_sent"):
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text=t(lang, "reminder_24h"),
                parse_mode="Markdown",
                reply_markup=kb_reminder(lang),
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
    lang = state.get("lang", "RO")

    if state.get("step") != "consultation_requested":
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text=t(lang, "final_cta"),
                parse_mode="Markdown",
                reply_markup=kb_consultation(lang),
            )
        except Exception as e:
            logger.error(f"Final CTA error {chat_id}: {e}")

# ─────────────────────────────────────────────
# Admin notification
# ─────────────────────────────────────────────

async def notify_admin(context, chat_id, user, lang):
    if not ADMIN_CHAT_ID:
        return
    try:
        flag = "🇷🇴" if lang == "RO" else "🇷🇺"
        lang_name = "Română" if lang == "RO" else "Русский"
        text = (
            f"🔔 *Cerere consultație / Запрос консультации!*\n\n"
            f"🌐 Limba: {flag} {lang_name}\n"
            f"👤 {user.first_name} {user.last_name or ''}\n"
            f"🆔 ID: `{user.id}`\n"
            f"📱 @{user.username or 'N/A'}"
        )
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=text, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Admin notify error: {e}")

# ─────────────────────────────────────────────
# Handlers
# ─────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"User: {user.id} @{user.username} {user.first_name}")

    context.user_data["state"] = {
        "step": "lang_select",
        "lang": None,
        "video_sent": False,
        "watched": False,
        "topic_chosen": False,
        "joined_at": datetime.now().isoformat(),
    }

    await update.message.reply_text(
        LANG_SELECT_TEXT,
        parse_mode="Markdown",
        reply_markup=kb_lang_select(),
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    state = get_state(context)
    chat_id = update.effective_chat.id

    # ── Language selection ──
    if data.startswith("lang_"):
        lang = data.split("_")[1]
        state["lang"] = lang
        state["step"] = "welcome"
        await query.edit_message_text(
            t(lang, "welcome"),
            parse_mode="Markdown",
            reply_markup=kb_get_video(lang),
        )
        return

    lang = state.get("lang", "RO")

    # ── Send video ──
    if data == "get_video":
        state["video_sent"] = True
        state["step"] = "video_sent"
        url = get_video_url(lang)
        msg = t(lang, "video").replace("{video_url}", url)

        await query.edit_message_text(
            msg,
            parse_mode="Markdown",
            reply_markup=kb_watched(lang),
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

    # ── After watching ──
    elif data == "watched":
        state["watched"] = True
        state["step"] = "watched"
        await query.edit_message_text(
            t(lang, "after_video"),
            parse_mode="Markdown",
            reply_markup=kb_topics(lang),
        )

    # ── Topic chosen ──
    elif data.startswith("topic_"):
        state["topic_chosen"] = True
        state["topic"] = data
        state["step"] = "topic_chosen"

        await query.edit_message_text(t(lang, "thanks_choice"), parse_mode="Markdown")
        await asyncio.sleep(1)
        await context.bot.send_message(chat_id=chat_id, text=t(lang, "warmup"), parse_mode="Markdown")
        await asyncio.sleep(2)
        await context.bot.send_message(
            chat_id=chat_id,
            text=t(lang, "consultation"),
            parse_mode="Markdown",
            reply_markup=kb_consultation(lang),
        )
        state["step"] = "consultation_offered"

    # ── Consultation request (no external URL configured) ──
    elif data == "request_consultation":
        state["step"] = "consultation_requested"
        await query.edit_message_text(t(lang, "received"), parse_mode="Markdown")
        await notify_admin(context, chat_id, update.effective_user, lang)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = get_state(context)
    step = state.get("step", "lang_select")
    lang = state.get("lang", "RO")

    if step == "lang_select":
        await update.message.reply_text(LANG_SELECT_TEXT, parse_mode="Markdown", reply_markup=kb_lang_select())
    elif step == "welcome":
        await update.message.reply_text(t(lang, "welcome"), parse_mode="Markdown", reply_markup=kb_get_video(lang))
    elif step == "video_sent":
        await update.message.reply_text(t(lang, "use_buttons"), parse_mode="Markdown")
    else:
        await update.message.reply_text(t(lang, "use_start"), parse_mode="Markdown")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Error: {context.error}", exc_info=context.error)

# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def main():
    logger.info("Starting Victor Bologan Bot (RO/RU)...")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_error_handler(error_handler)
    logger.info("Bot running. Ctrl+C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
