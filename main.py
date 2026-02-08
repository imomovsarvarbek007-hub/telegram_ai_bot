import os
import requests
from telegram.ext import Updater, MessageHandler, Filters

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = "Sen aqlli, muloyim, o‘zbek tilida gapiradigan sun’iy intellektsan."

def reply(update, context):
    user_text = update.message.text

    url = "https://api.openai.com/v1/responses"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "input": f"{SYSTEM_PROMPT}\nFoydalanuvchi: {user_text}"
    }

    r = requests.post(url, headers=headers, json=data)

    if r.status_code != 200:
        update.message.reply_text("Xatolik bo‘ldi 😢")
        return

    answer = r.json()["output"][0]["content"][0]["text"]
    update.message.reply_text(answer)

updater = Updater(TELEGRAM_TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, reply))

updater.start_polling()
print("Bot ishga tushdi 🤖")
updater.idle()
