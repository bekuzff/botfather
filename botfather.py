import os
import threading
import logging
from flask import Flask
from telethon import TelegramClient, events

# Logging sozlamalari
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Sizning shaxsiy ma'lumotlaringiz
API_ID = 37958522
API_HASH = '6df46040542832e1e164e65f5e8746b0'
BOT_TOKEN = '7708286324:AAHmtv15lEf0TAVMT0nBiJq8nvAuT9ymK4U'

# --- RENDER UCHUN FLASK SERVERI (Port talabini qondirish uchun) ---
app = Flask('')


@app.route('/')
def home():
    return "Telethon Bot Render'da ishlayapti!"


def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)


# --- TELETHON BOT QISMI ---
client = TelegramClient('bot_session', API_ID, API_HASH)


@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    sender = await event.get_sender()
    name = sender.first_name if sender else "Foydalanuvchi"

    await event.respond(
        f"Assalomu alaykum, {name}! 🚀\n"
        "Telethon boti Render serverida muvaffaqiyatli ishga tushdi va xizmatga tayyor!"
    )


@client.on(events.NewMessage(pattern=r'^(?!/).*'))
async def echo_handler(event):
    text = event.raw_text
    await event.respond(f"Sizning xabaringiz qabul qilindi: <b>{text}</b>", parse_mode='html')


if __name__ == '__main__':
    # 1. Flask serverini alohida oqimda (thread) ishga tushiramiz
    t = threading.Thread(target=run_flask)
    t.start()

    print("Telethon bot ishga tushmoqda...")

    # 2. Telethon botini token orqali ishga tushiramiz
    client.start(bot_token=BOT_TOKEN)
    client.run_until_disconnected()