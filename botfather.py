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
    return "BotFather Klon Tizimi Mukammal Ishlamoqda!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- TELETHON KLIENTLARI ---
user_client = TelegramClient('user_session', API_ID, API_HASH)
bot_client = TelegramClient('bot_session', API_ID, API_HASH)

user_states = {}

# --- BOTFATHER KLON BUYRUQLARI ---

@bot_client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    await event.respond(
        "🤖 **Welcome to BotFather**\n\n"
        "I can help you create and manage Telegram bots. "
        "Use these commands to control me:\n\n"
        "/newbot - create a new bot\n"
        "/cancel - cancel current operation\n\n"
        "Xuddi haqiqiy BotFather kabi ishlaydi!"
    )

@bot_client.on(events.NewMessage(pattern='/cancel'))
async def cancel_handler(event):
    sender_id = event.sender_id
    user_states.pop(sender_id, None)
    await event.respond("❌ Amal bekor qilindi. Yangi bot ochish uchun /newbot ni bosing.")

@bot_client.on(events.NewMessage(pattern='/newbot'))
async def newbot_handler(event):
    sender_id = event.sender_id
    user_states[sender_id] = {'step': 'waiting_for_name'}
    await event.respond(
        "Alright, a new bot. How are we going to call it? Please choose a name for your bot."
    )

@bot_client.on(events.NewMessage(pattern=r'^(?!/).*'))
async def message_handler(event):
    sender_id = event.sender_id
    text = event.raw_text.strip()
    
    state = user_states.get(sender_id)
    if not state:
        return
        
    if state.get('step'] == 'waiting_for_name':
        user_states[sender_id] = {'step': 'waiting_for_username', 'name': text}
        await event.respond(
            "Good. Now choose a username for your bot. It must end in `bot`. "
            "Like, ExampleBot or example_bot."
        )
        
    elif state.get('step'] == 'waiting_for_username':
        bot_name = state['name']
        bot_username = text
        
        if not (bot_username.endswith('bot') or bot_username.endswith('_bot')):
            await event.respond(
                "Sorry, the username must end in either 'bot' or '_bot'. "
                "You can choose a different username:"
            )
            return
            
        await event.respond("⏳ @BotFather orqali bot yaratilmoqda, iltimos kuting...")
        
        try:
            botfather = await user_client.get_entity('BotFather')
            
            # Asl BotFather bilan ketma-ket muloqot
            await user_client.send_message(botfather, '/newbot')
            await asyncio.sleep(1.5)
            
            await user_client.send_message(botfather, bot_name)
            await asyncio.sleep(1.5)
            
            await user_client.send_message(botfather, bot_username)
            await asyncio.sleep(2.5)
            
            # Tokenni qidirib topish
            token_found = None
            async for message in user_client.iter_messages(botfather, limit=3):
                if message.text and ("HTTP API" in message.text or ":" in message.text):
                    token_found = message.text
                    break
            
            if token_found:
                await event.respond(
                    f"Done! Congratulations on your new bot. You will find it at t.me/{bot_username}.\n\n"
                    f"Use this token to access the HTTP API:\n{token_found}\n\n"
                    f"Keep your token safe and secure!"
                )
            else:
                await event.respond("⚠️ Bot yaratildi, lekin tokenni avtomatik o'qib bo'lmadi. @BotFather tarixini tekshiring.")
                
        except Exception as e:
            await event.respond(f"❌ Xatolik yuz berdi: `{str(e)}`")
            
        user_states.pop(sender_id, None)

if __name__ == '__main__':
    t = threading.Thread(target=run_flask)
    t.start()
    
    print("BotFather klon tizimi ishga tushmoqda...")
    user_client.start()
    bot_client.start(bot_token=BOT_TOKEN)
    
    user_client.run_until_disconnected()
    bot_client.run_until_disconnected()
