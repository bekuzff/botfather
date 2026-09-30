import os
import threading
import logging
import asyncio
from flask import Flask
from telethon import TelegramClient, events

# Logging sozlamalari
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Ma'lumotlar
API_ID = 37958522
API_HASH = '6df46040542832e1e164e65f5e8746b0'
BOT_TOKEN = '8956644482:AAFgkx1HS6oSEe57zzFSiVCoUflLtKdSQnI'

# --- RENDER UCHUN FLASK SERVERI ---
app = Flask('')

@app.route('/')
def home():
    return "BotFather Konstruktor Tizimi Ishlamoqda!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- TELETHON KLIENTLARI ---
user_client = TelegramClient('user_session', API_ID, API_HASH)
bot_client = TelegramClient('bot_session', API_ID, API_HASH)

user_states = {}

# --- ASOSIY BOT QISMI ---
@bot_client.on(events.NewMessage(pattern='/start'))
async def bot_start(event):
    sender_id = event.sender_id
    user_states[sender_id] = {'step': 'waiting_for_name'}
    await event.respond(
        "🤖 **BotFather Konstruktoriga xush kelibsiz!**\n\n"
        "Yangi bot yaratish uchun menga botingiz uchun **Ism (Title)** yuboring.\n"
        "_(Masalan: Mening Botim)_"
    )

@bot_client.on(events.NewMessage(pattern=r'^(?!/).*'))
async def bot_messages(event):
    sender_id = event.sender_id
    text = event.raw_text.strip()
    
    state = user_states.get(sender_id)
    if not state:
        return
        
    if state.get('step') == 'waiting_for_name':
        user_states[sender_id] = {'step': 'waiting_for_username', 'name': text}
        await event.respond(
            f"✅ Bot nomi qabul qilindi: **{text}**\n\n"
            "Endi botingiz uchun **Username** yuboring (oxiri `_bot` yoki `bot` bilan tugashi shart).\n"
            "_(Masalan: my_new_test_bot)_"
        )
        
    elif state.get('step') == 'waiting_for_username':
        bot_name = state['name']
        bot_username = text
        
        if not (bot_username.endswith('bot') or bot_username.endswith('_bot')):
            await event.respond("❌ Xato! Username albatta `bot` yoki `_bot` bilan tugashi kerak. Qaytadan yuboring:")
            return
            
        await event.respond("⏳ @BotFather bilan bog'lanib, botingiz avtomatik ochilmoqda, biroz kuting...")
        
        try:
            botfather = await user_client.get_entity('BotFather')
            
            await user_client.send_message(botfather, '/newbot')
            await asyncio.sleep(1.5)
            
            await user_client.send_message(botfather, bot_name)
            await asyncio.sleep(1.5)
            
            await user_client.send_message(botfather, bot_username)
            await asyncio.sleep(2.5)
            
            token_found = None
            async for message in user_client.iter_messages(botfather, limit=3):
                if message.text and ("HTTP API" in message.text or ":" in message.text):
                    token_found = message.text
                    break
            
            if token_found:
                await event.respond(
                    f"🎉 **Tabriklayman! Botingiz muvaffaqiyatli yaratildi!**\n\n"
                    f"📌 Nomi: {bot_name}\n"
                    f"🔗 Username: @{bot_username}\n\n"
                    f"🔑 **Bot Tokeni:**\n{token_found}\n\n"
                    f"Yangi bot ochish uchun /start ni bosing."
                )
            else:
                await event.respond("⚠️ Bot yaratildi, lekin tokenni o'qib bo'lmadi. @BotFather tarixini tekshiring.")
                
        except Exception as e:
            await event.respond(f"❌ Xatolik yuz berdi: `{str(e)}`")
            
        user_states.pop(sender_id, None)

if __name__ == '__main__':
    t = threading.Thread(target=run_flask)
    t.start()
    
    user_client.start()
    bot_client.start(bot_token=BOT_TOKEN)
    
    user_client.run_until_disconnected()
    bot_client.run_until_disconnected()
