import os
import threading
import logging
from flask import Flask
from telethon import TelegramClient, events
from telethon.tl.functions.contacts import SearchRequest
from telethon.tl.functions.messages import StartBotRequest

# Logging sozlamalari
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Sizning shaxsiy ma'lumotlaringiz
API_ID = 37958522
API_HASH = '6df46040542832e1e164e65f5e8746b0'
BOT_TOKEN = '8956644482:AAFgkx1HS6oSEe57zzFSiVCoUflLtKdSQnI'

# --- RENDER UCHUN FLASK SERVERI ---
app = Flask('')

@app.route('/')
def home():
    return "BotFather Klon Bot Render'da ishlayapti!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- TELETHON BOT QISMI ---
client = TelegramClient('bot_session', API_ID, API_HASH)

# Foydalanuvchilar qaysi bosqichda ekanligini saqlash uchunvaqtinchalik xotira
user_states = {}

@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    sender_id = event.sender_id
    user_states[sender_id] = 'waiting_for_name'
    
    await event.respond(
        "🤖 **Assalomu alaykum! BotFather kloniga xush kelibsiz.**\n\n"
        "Yangi bot yaratish uchun menga botingiz uchun **Ism (Title)** yuboring.\n"
        "_(Masalan: Mening Botiim)_"
    )

@client.on(events.NewMessage(pattern=r'^(?!/).*'))
async def message_handler(event):
    sender_id = event.sender_id
    text = event.raw_text.strip()
    
    state = user_states.get(sender_id)
    
    if state == 'waiting_for_name':
        # Foydalanuvchi bot nomini yubordi, endi username so'raymiz
        user_states[sender_id] = {'step': 'waiting_for_username', 'name': text}
        await event.respond(
            f"✅ Bot nomi qabul qilindi: **{text}**\n\n"
            "Endi botingiz uchun **Username** yuboring (oxiri `_bot` yoki `bot` bilan tugashi shart).\n"
            "_(Masalan: my_cool_new_bot)_"
        )
        
    elif isinstance(state, dict) and state.get('step') == 'waiting_for_username':
        bot_name = state['name']
        bot_username = text
        
        # Username to'g'ri tugaganini tekshiramiz
        if not (bot_username.endswith('bot') or bot_username.endswith('_bot')):
            await event.respond("❌ Xato! Bot username'i albatta `bot` yoki `_bot` bilan tugashi kerak. Qaytadan urinib ko'ring:")
            return
            
        await event.respond("⏳ @BotFather bilan bog'lanib, botingiz yaratilmoqda, biroz kuting...")
        
        try:
            # BotFather (@BotFather) bilan avtomatik muloqot qilish
            botfather = await client.get_entity('BotFather')
            
            # /newbot buyrug'ini yuboramiz
            await client.send_message(botfather, '/newbot')
            await client.loop.run_in_executor(None, lambda: __import__('time').sleep(1))
            
            # Bot nomini yuboramiz
            await client.send_message(botfather, bot_name)
            await client.loop.run_in_executor(None, lambda: __import__('time').sleep(1))
            
            # Bot username'ini yuboramiz
            await client.send_message(botfather, bot_username)
            await client.loop.run_in_executor(None, lambda: __import__('time').sleep(2))
            
            # BotFather'ning oxirgi xabarlarini o'qib tokenini olamiz
            async for message in client.iter_messages(botfather, limit=2):
                if "HTTP API" in message.text or ":" in message.text:
                    await event.respond(
                        f"🎉 **Tabriklayman! Botingiz muvaffaqiyatli yaratildi!**\n\n"
                        f"Ma'lumotlar:\n"
                        f"📌 Nomi: {bot_name}\n"
                        f"🔗 Username: @{bot_username}\n\n"
                        f"🔑 **Bot Tokeni va xabarlar:**\n{message.text}\n\n"
                        f"Yana yangi bot ochish uchun /start ni bosing."
                    )
                    break
            else:
                await event.respond("⚠️ Bot yaratildi, lekin tokenni avtokapir qilib bo'lmadi. Iltimos @BotFather'ga o'zingiz kirib tekshiring.")
                
        except Exception as e:
            await event.respond(f"❌ Xatolik yuz berdi: `{str(e)}`\nIltimos keyinroq qaytadan urinib ko'ring.")
            
        # Holatni tozalaymiz
        user_states.pop(sender_id, None)

if __name__ == '__main__':
    # 1. Flask serverini ishga tushiramiz
    t = threading.Thread(target=run_flask)
    t.start()
    
    print("BotFather klon boti ishga tushmoqda...")
    
    # 2. Botni ishga tushiramiz
    client.start(bot_token=BOT_TOKEN)
    client.run_until_disconnected()
