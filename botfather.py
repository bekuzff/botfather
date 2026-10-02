import telebot
from telebot import types

# --- SOZLAMALAR ---
API_TOKEN = "8843916751:AAEaF0WS1IEhAwqGpOorfk74h3alMWu7Zvg"
ADMIN_IDS = [8372285180, 8654996917]
REQUIRED_CHANNELS = ["@bekuzbotmaker"]  # Shu yerga qaysi kanal kerak bo'lsa yozing yoki bo'sh qoldiring []

bot = telebot.TeleBot(API_TOKEN)

db_free_settings = []
db_paid_settings = []
user_states = {}

texts_db = {
    "foizli": """
⚙️ **FOIZLI NASTROYKALAR (HEADSHOT & DPI)** 🎮

🔹 **25% NASTROYKA** — 20 000 so'm ⚙️
🔹 **50% NASTROYKA** — 30 000 so'm ⚙️
🔹 **75% NASTROYKA** — 40 000 so'm ⚙️
🔹 **85% NASTROYKA** — 50 000 so'm ⚙️
🔹 **90% NASTROYKA** — 60 000 so'm ⚙️
🔹 **92% NASTROYKA** — 65 000 so'm ⚙️
🔹 **94% NASTROYKA** — 80 000 so'm ⚙
🔹 **97% NASTROYKA** — 90 000 so'm ⚙️

💬 **Sotib olish uchun adminga yozing:** @jasurbrzl
""",
    "almaz": """
💎 **ALMAZ NARXLARI**
🆔 **ID ORQALI QBERAMIZ** ⚡️

🔹 110 💎 - 11.000 uzs ✅
🔹 220 💎 - 22.000 uzs ✅
🔹 341 💎 - 33.000 uzs ✅
🔹 572 💎 - 53.000 uzs ✅
🔹 1166 💎 - 109.000 uzs ✅
🔹 2398 💎 - 212.000 uzs ✅
🔹 6160 💎 - 535.000 uzs ✅

💬 **Murojaat uchun:** @jasurbrzl
"""
}

def check_subscription(user_id: int) -> bool:
    if not REQUIRED_CHANNELS:
        return True
    for channel in REQUIRED_CHANNELS:
        try:
            member = bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in ['left', 'kicked']:
                return False
        except Exception:
            pass
    return True

def get_main_menu(user_id: int):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(
        types.KeyboardButton("🎁 Tekin Nastroykalar"),
        types.KeyboardButton("💎 Soft Nastroyka (Pullik)")
    )
    keyboard.add(
        types.KeyboardButton("⚙️ Foizli Nastroykalar"),
        types.KeyboardButton("💎 Almaz Narxlari")
    )
    keyboard.add(types.KeyboardButton("📢 Kanalimiz"))
    if user_id in ADMIN_IDS:
        keyboard.add(types.KeyboardButton("👑 Admin Panel"))
    return keyboard

@bot.message_handler(commands=['start'])
def cmd_start(message):
    user_id = message.from_user.id
    if not check_subscription(user_id):
        channels_text = "\n".join([f"👉 {ch}" for ch in REQUIRED_CHANNELS])
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✅ Obunani tekshirish", callback_data="check_sub"))
        bot.send_message(
            message.chat.id,
            f"❌ Botdan foydalanish uchun quyidagi kanalga obuna bo'lishingiz kerak:\n\n{channels_text}",
            reply_markup=markup
        )
        return
    bot.send_message(message.chat.id, "Salom! Free Fire botiga xush kelibsiz. Kerakli bo'limni tanlang:", reply_markup=get_main_menu(user_id))

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def process_check_sub(call):
    user_id = call.from_user.id
    if check_subscription(user_id):
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception:
            pass
        bot.send_message(call.message.chat.id, "Rahmat! Obuna tasdiqlandi. Asosiy menyu:", reply_markup=get_main_menu(user_id))
    else:
        bot.answer_callback_query(call.id, "❌ Hali kanalga obuna bo'lmadingiz!", show_alert=True)

@bot.message_handler(func=lambda message: message.text == "⚙️ Foizli Nastroykalar")
def show_foizli(message):
    if not check_subscription(message.from_user.id): return
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🛒 Sotib olish / Murojaat", url="https://t.me/jasurbrzl"))
    bot.send_message(message.chat.id, texts_db["foizli"], parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "💎 Almaz Narxlari")
def show_almaz(message):
    if not check_subscription(message.from_user.id): return
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🛒 Xarid qilish / Murojaat", url="https://t.me/jasurbrzl"))
    bot.send_message(message.chat.id, texts_db["almaz"], parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🎁 Tekin Nastroykalar")
def show_free(message):
    if not check_subscription(message.from_user.id): return
    if not db_free_settings:
        return bot.send_message(message.chat.id, "⚠️ Hozircha tekin nastroykalar mavjud emas!")
    markup = types.InlineKeyboardMarkup(row_width=1)
    for item in db_free_settings:
        markup.add(types.InlineKeyboardButton(f"⚙️ {item['name']}", callback_data=f"get_free_{item['id']}"))
    bot.send_message(message.chat.id, "🎁 Mavjud tekin nastroykalar:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("get_free_"))
def send_free(call):
    item_id = int(call.data.split("_")[2])
    item = next((i for i in db_free_settings if i['id'] == item_id), None)
    if item:
        bot.send_message(call.message.chat.id, f"Siz tanlagan nastroyka: **{item['name']}**\n\n{item['content']}", parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "💎 Soft Nastroyka (Pullik)")
def show_paid(message):
    if not check_subscription(message.from_user.id): return
    if not db_paid_settings:
        return bot.send_message(message.chat.id, "⚠️ Hozircha pullik soft nastroykalar mavjud emas.")
    markup = types.InlineKeyboardMarkup(row_width=1)
    for item in db_paid_settings:
        markup.add(types.InlineKeyboardButton(f"💎 {item['name']} (Pullik)", callback_data=f"get_paid_{item['id']}"))
    bot.send_message(message.chat.id, "💎 Pullik soft nastroykalar:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("get_paid_"))
def send_paid(call):
    item_id = int(call.data.split("_")[2])
    item = next((i for i in db_paid_settings if i['id'] == item_id), None)
    if item:
        bot.send_message(call.message.chat.id, f"💎 **{item['name']}**\n\n{item['content']}\n\n*Sotib olish uchun adminga murojaat qiling.*", parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "👑 Admin Panel")
def admin_panel(message):
    if message.from_user.id not in ADMIN_IDS: return
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton("➕ Tekin Nastroyka qo'shish"), types.KeyboardButton("🗑 Tekin Nastroykani o'chirish"))
    markup.add(types.KeyboardButton("➕ Soft (Pullik) qo'shish"), types.KeyboardButton("🗑 Soft Nastroykani o'chirish"))
    markup.add(types.KeyboardButton("✏️ Foizli Nastroykani o'zgartirish"), types.KeyboardButton("✏️ Almaz Narxini o'zgartirish"))
    markup.add(types.KeyboardButton("📢 Obuna kanal qo'shish"), types.KeyboardButton("❌ Obuna kanalni o'chirish"))
    markup.add(types.KeyboardButton("🔙 Asosiy Menyu"))
    bot.send_message(message.chat.id, "👑 Admin boshqaruv paneli:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🔙 Asosiy Menyu")
def back_to_main(message):
    bot.send_message(message.chat.id, "Asosiy menyu:", reply_markup=get_main_menu(message.from_user.id))

@bot.message_handler(func=lambda message: message.text == "➕ Tekin Nastroyka qo'shish")
def add_free_start(message):
    if message.from_user.id not in ADMIN_IDS: return
    user_states[message.from_user.id] = {"step": "wait_free_name"}
    bot.send_message(message.chat.id, "Yangi tekin nastroyka uchun **nom** kiriting:")

@bot.message_handler(func=lambda message: message.text == "🗑 Tekin Nastroykani o'chirish")
def del_free_menu(message):
    if message.from_user.id not in ADMIN_IDS: return
    if not db_free_settings: return bot.send_message(message.chat.id, "O'chiriladigani yo'q.")
    markup = types.InlineKeyboardMarkup(row_width=1)
    for i in db_free_settings:
        markup.add(types.InlineKeyboardButton(f"❌ O'chirish: {i['name']}", callback_data=f"dfree_{i['id']}"))
    bot.send_message(message.chat.id, "O'chirish uchun tanlang:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("dfree_"))
def process_dfree(call):
    item_id = int(call.data.split("_")[1])
    global db_free_settings
    db_free_settings = [i for i in db_free_settings if i['id'] != item_id]
    try: bot.delete_message(call.message.chat.id, call.message.message_id)
    except: pass
    bot.send_message(call.message.chat.id, "✅ O'chirildi!")

@bot.message_handler(func=lambda message: message.text == "➕ Soft (Pullik) qo'shish")
def add_paid_start(message):
    if message.from_user.id not in ADMIN_IDS: return
    user_states[message.from_user.id] = {"step": "wait_paid_name"}
    bot.send_message(message.chat.id, "Pullik soft nastroyka uchun **nom** kiriting:")

@bot.message_handler(func=lambda message: message.text == "🗑 Soft Nastroykani o'chirish")
def del_paid_menu(message):
    if message.from_user.id not in ADMIN_IDS: return
    if not db_paid_settings: return bot.send_message(message.chat.id, "O'chiriladigani yo'q.")
    markup = types.InlineKeyboardMarkup(row_width=1)
    for i in db_paid_settings:
        markup.add(types.InlineKeyboardButton(f"❌ O'chirish: {i['name']}", callback_data=f"dpaid_{i['id']}"))
    bot.send_message(message.chat.id, "O'chirish uchun tanlang:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("dpaid_"))
def process_dpaid(call):
    item_id = int(call.data.split("_")[1])
    global db_paid_settings
    db_paid_settings = [i for i in db_paid_settings if i['id'] != item_id]
    try: bot.delete_message(call.message.chat.id, call.message.message_id)
    except: pass
    bot.send_message(call.message.chat.id, "✅ O'chirildi!")

@bot.message_handler(func=lambda message: message.text == "✏️ Foizli Nastroykani o'zgartirish")
def edit_foizli_start(message):
    if message.from_user.id not in ADMIN_IDS: return
    user_states[message.from_user.id] = {"step": "wait_edit_foizli"}
    bot.send_message(message.chat.id, "Foizli nastroykalar uchun **yangi matnni** yuboring:")

@bot.message_handler(func=lambda message: message.text == "✏️ Almaz Narxini o'zgartirish")
def edit_almaz_start(message):
    if message.from_user.id not in ADMIN_IDS: return
    user_states[message.from_user.id] = {"step": "wait_edit_almaz"}
    bot.send_message(message.chat.id, "Almaz narxlari uchun **yangi matnni** yuboring:")

@bot.message_handler(func=lambda message: message.text == "📢 Obuna kanal qo'shish")
def add_channel_start(message):
    if message.from_user.id not in ADMIN_IDS: return
    user_states[message.from_user.id] = {"step": "wait_channel"}
    bot.send_message(message.chat.id, "Yangi kanal username'ini yuboring (masalan: `@kanal_nomi`):")

@bot.message_handler(func=lambda message: message.text == "❌ Obuna kanalni o'chirish")
def remove_channel_menu(message):
    if message.from_user.id not in ADMIN_IDS: return
    if not REQUIRED_CHANNELS: return bot.send_message(message.chat.id, "Hozircha majburiy kanallar yo'q.")
    markup = types.InlineKeyboardMarkup(row_width=1)
    for ch in REQUIRED_CHANNELS:
        markup.add(types.InlineKeyboardButton(f"O'chirish: {ch}", callback_data=f"rm_ch_{ch}"))
    bot.send_message(message.chat.id, "O'chiriladigan kanalni tanlang:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("rm_ch_"))
def process_remove_channel(call):
    ch_name = call.data.replace("rm_ch_", "")
    if ch_name in REQUIRED_CHANNELS:
        REQUIRED_CHANNELS.remove(ch_name)
    try: bot.delete_message(call.message.chat.id, call.message.message_id)
    except: pass
    bot.send_message(call.message.chat.id, f"✅ {ch_name} majburiy obunalardan olib tashlandi!")

@bot.message_handler(func=lambda message: message.from_user.id in user_states)
def handle_admin_states(message):
    user_id = message.from_user.id
    state = user_states.get(user_id, {}).get("step")
    
    if state == "wait_free_name":
        user_states[user_id] = {"step": "wait_free_content", "name": message.text}
        bot.send_message(message.chat.id, "Endi ushbu tekin nastroyka uchun **matn yoki ma'lumot** yuboring:")
    elif state == "wait_free_content":
        name = user_states[user_id]["name"]
        content = message.text if message.text else "Ma'lumot"
        db_free_settings.append({"id": len(db_free_settings) + 1, "name": name, "content": content})
        del user_states[user_id]
        bot.send_message(message.chat.id, "✅ Tekin nastroyka qo'shildi!", reply_markup=get_main_menu(user_id))
        
    elif state == "wait_paid_name":
        user_states[user_id] = {"step": "wait_paid_content", "name": message.text}
        bot.send_message(message.chat.id, "Endi pullik soft uchun **matn yoki ma'lumot** yuboring:")
    elif state == "wait_paid_content":
        name = user_states[user_id]["name"]
        content = message.text if message.text else "Ma'lumot"
        db_paid_settings.append({"id": len(db_paid_settings) + 1, "name": name, "content": content})
        del user_states[user_id]
        bot.send_message(message.chat.id, "✅ Pullik soft qo'shildi!", reply_markup=get_main_menu(user_id))
        
    elif state == "wait_edit_foizli":
        texts_db["foizli"] = message.text
        del user_states[user_id]
        bot.send_message(message.chat.id, "✅ Foizli nastroykalar matni o'zgartirildi!", reply_markup=get_main_menu(user_id))

    elif state == "wait_edit_almaz":
        texts_db["almaz"] = message.text
        del user_states[user_id]
        bot.send_message(message.chat.id, "✅ Almaz narxlari matni o'zgartirildi!", reply_markup=get_main_menu(user_id))

    elif state == "wait_channel":
        channel = message.text.strip()
        if channel not in REQUIRED_CHANNELS:
            REQUIRED_CHANNELS.append(channel)
        del user_states[user_id]
        bot.send_message(message.chat.id, f"✅ {channel} obunalarga qo'shildi!", reply_markup=get_main_menu(user_id))

if __name__ == '__main__':
    print("Bot ishga tushdi...")
    bot.infinity_polling(skip_pending=True)
