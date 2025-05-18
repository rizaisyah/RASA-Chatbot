import os
import requests
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from telegram import Update
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
RASA_URL = "http://localhost:5005/webhooks/rest/webhook"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    sender = update.message.chat_id

    res = requests.post(RASA_URL, json={"sender": str(sender), "message": message})
    for r in res.json():
        await context.bot.send_message(chat_id=sender, text=r.get("text"))

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()