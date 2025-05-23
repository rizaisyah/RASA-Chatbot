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

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
RASA_URL = "http://localhost:5005/webhooks/rest/webhook"

# Fungsi untuk menampilkan tombol inline menu
async def send_inline_menu(context, chat_id, text="Silakan pilih perangkat yang bermasalah:"):
    keyboard = [
        [InlineKeyboardButton("AP (Internet)", callback_data="AP")],
        [InlineKeyboardButton("LAN", callback_data="LAN")],
        [InlineKeyboardButton("Smart TV", callback_data="smart tv")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)

# Fungsi untuk handle command /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_inline_menu(context, update.message.chat_id, "Selamat datang! Silakan pilih permasalahan Anda.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    sender = update.message.chat_id

    if message.strip().lower() == "/start":
        return

    res = requests.post(RASA_URL, json={"sender": str(sender), "message": message})
    for r in res.json():
        if r.get("custom", {}).get("show_inline_menu"):
            await send_inline_menu(context, sender, r.get("text", "Silakan pilih permasalahan Anda:"))
        else:
            await context.bot.send_message(chat_id=sender, text=r.get("text"))
# Fungsi untuk handle klik tombol inline
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_input = query.data
    sender = query.from_user.id

    res = requests.post(RASA_URL, json={"sender": str(sender), "message": user_input})
    for r in res.json():
        if r.get("custom", {}).get("show_inline_menu"):
            await send_inline_menu(context, sender, r.get("text", "Silakan pilih permasalahan Anda:"))
        else:
            await context.bot.send_message(chat_id=sender, text=r.get("text"))

# Main
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
