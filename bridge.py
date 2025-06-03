import os
import requests
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# Load token dari .env
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
RASA_URL = "http://localhost:5005/webhooks/rest/webhook"

# Fungsi untuk kirim menu tombol inline
async def send_inline_menu(context, chat_id, text=""):
    keyboard = [
        [InlineKeyboardButton("AP (Internet)", callback_data='/choose_device_ap{"device_type": "AP"}')],
        [InlineKeyboardButton("LAN", callback_data='/choose_device_lan{"device_type": "LAN"}')],
        [InlineKeyboardButton("Smart TV", callback_data='/choose_device_tv{"device_type": "Smart TV"}')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)

# Fungsi /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_inline_menu(context, update.message.chat_id, "Selamat datang! Silakan pilih permasalahan Anda.")

# Fungsi untuk handle pesan user
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text.strip()
    sender = update.message.chat_id

    if message.lower() == "/start":
        return

    res = requests.post(RASA_URL, json={"sender": str(sender), "message": message})
    for r in res.json():
        custom = r.get("custom", {})
        text = r.get("text", "")

        if custom.get("show_inline_menu"):
            await send_inline_menu(context, sender, text or "Silakan pilih permasalahan Anda:")
        elif text:
            await context.bot.send_message(chat_id=sender, text=text)

# Fungsi untuk handle klik tombol
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    sender = query.from_user.id
    user_input = query.data  # Sudah dalam bentuk /choose_device_ap{"device_type": "AP"}

    res = requests.post(
        RASA_URL,
        json={
            "sender": str(sender),
            "message": user_input
        }
    )

    for r in res.json():
        text = r.get("text", "")
        custom = r.get("custom", {})
        if custom.get("show_inline_menu"):
            await send_inline_menu(context, sender, text or "Silakan pilih permasalahan Anda:")
        elif text:
            await context.bot.send_message(chat_id=sender, text=text)

    print(f"[DEBUG] Telegram button clicked: {user_input}")

# Main program
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
