import os
import requests
from telegram.ext import Updater, MessageHandler, Filters
from dotenv import load_dotenv
load_dotenv()


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # Atur lewat .env atau langsung string
RASA_URL = "http://localhost:5005/webhooks/rest/webhook"

def handle_message(update, context):
    message = update.message.text
    sender = update.message.chat_id

    res = requests.post(RASA_URL, json={"sender": str(sender), "message": message})
    for r in res.json():
        context.bot.send_message(chat_id=sender, text=r.get("text"))

if __name__ == "__main__":
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()
