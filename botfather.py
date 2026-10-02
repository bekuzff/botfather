import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

# --- SOZLAMALAR ---
API_TOKEN = "8843916751:AAEaF0WS1IEhAwqGpOorfk74h3alMWu7Zvg"

# Adminlarning Telegram ID raqamlari (Siz va sherigingiz):
ADMIN_IDS = [8372285180, 8654996917]

# Majburiy obuna kanallari/guruhlari ro'yxati (Admin panel orqali o'zgartirilishi mumkin)
REQUIRED_CHANNELS = ["@sizning_kanal"] 

# Xotirada saqlanadigan bazalar
db_free_settings = []  
db_paid_settings = []  

# FOIZLI NASTROYKALAR (5 mingga arzonlashtirilgan variant)
FOIZLI_NASTROYKALAR_TEXT = """
⚙️ **FOIZLI NASTROYKALAR (HEADSHOT & DPI)** 🎮

🔹 **25% NASTROYKA** — 20 000 so'm ⚙️
🔹 **50% NASTROYKA** — 30 000 so'm ⚙️
🔹 **75% NASTROYKA** — 40 000 so'm ⚙️
🔹 **85% NASTROYKA** — 50 000 so'm ⚙️
🔹 **90% NASTROYKA** — 60 000 so'm ⚙️
🔹 **92% NASTROYKA** — 65 000 so'm ⚙️
🔹 **94% NASTROYKA** — 80 000 so'm ⚙️
🔹 **97% NASTROYKA** — 90 000 so'm ⚙️

💬 **Sotib olish uchun adminga yozing:** @jasurbrzl
"""

# ALMAZ NARXLARI MATNI
ALMAZ_TEXT = """
💎 **ALMAZ NARXLARI**

🆔 **ID ORQALI QBERAMIZ** ⚡️

🔹 110 💎 - 11.000 uzs ✅
🔹 220 💎 - 22.000 uzs ✅
🔹 341 💎 - 33.000 uzs ✅
🔹 572 💎 - 53.000 uzs ✅
🔹 1166 💎 - 109.000 uzs ✅
🔹 2398 💎 - 212.000 uzs ✅
🔹 6160 💎 - 535.000 uzs ✅

📦 **Vaucherlar va Paketlar:**
🔸 Mini haftalik (90 💎) - 7.000 uzs ✅
🔸 Haftalik (450 💎) - 20.000 uzs ✅
🔸 Oylik (2600 💎) - 80.000 uzs ✅ *(2 tadan ko'p oselar 78 mingdan)*

💬 **Murojaat uchun:** @jasurbrzl
"""

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# FSM holatlari
class AdminStates(StatesGroup):
    waiting_for_free_name = State()
    waiting_for_free_content = State()
    waiting_for_paid_name = State()
    waiting_for_paid_content = State()
    waiting_for_channel = State()

# --- OBUNANI TEKSHIRISH ---
async def check_subscription(user_id: int) -> bool:
    if not REQUIRED_CHANNELS:
        return True
    for channel in REQUIRED_CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except Exception:
            return False
    return True

# --- ASOSIY MENYU ---
def get_main_menu(user_id: int):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(
        types.KeyboardButton("🎁 Tekin Nastroykalar"),
        types.KeyboardButton("💎 Soft Nastroyka (Pullik)")
    )
    keyboard.add(
        types.KeyboardButton("⚙️️ Foizli Nastroykalar"),
        types.KeyboardButton("💎 Almaz Narxlari")
    )
    keyboard.add(types.KeyboardButton("📢 Kanalimiz"))
    if user_id in ADMIN_IDS:
        keyboard.add(types.KeyboardButton("👑 Admin Panel"))
    return keyboard

# --- START KOMANDASI ---
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    
    is_subscribed = await check_subscription(user_id)
    if not is_subscribed:
        channels_text = "\n".join([f"👉 {ch}" for ch in REQUIRED_CHANNELS])
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✅ Obunani tekshirish", callback_data="check_sub"))
        await message.answer(
            f"❌ Botdan foydalanish uchun quyidagi kanal yoki guruhlarga obuna bo'lishingiz kerak:\n\n{channels_text}",
            reply_markup=markup
        )
        return

    await message.answer(
        "Salom! Free Fire botiga xush kelibsiz. Kerakli bo'limni tanlang:",
        reply_markup=get_main_menu(user_id)
    )

@dp.callback_query_handler(text="check_sub")
async def process_check_sub(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    is_subscribed = await check_subscription(user_id)
    if is_subscribed:
        await callback.message.delete()
        await callback.message.answer(
            "Rahmat! Obuna tasdiqlandi. Asosiy menyu:",
            reply_markup=get_main_menu(user_id)
        )
    else:
        await callback.answer("❌ Hali hamma kanal/guruhlarga obuna bo'lmadingiz!", show_alert=True)

# --- BO'LIMLAR ---
@dp.message_handler(text="⚙️ Foizli Nastroykalar")
async def show_foizli(message: types.Message):
    if not await check_subscription(message.from_user.id):
        return await message.answer("Avval obuna bo'ling! /start ni bosing.")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🛒 Sotib olish / Murojaat", url="https://t.me/jasurbrzl"))
    await message.answer(FOIZLI_NASTROYKALAR_TEXT, parse_mode="Markdown", reply_markup=markup)

@dp.message_handler(text="💎 Almaz Narxlari")
async def show_almaz(message: types.Message):
    if not await check_subscription(message.from_user.id):
        return await message.answer("Avval obuna bo'ling! /start ni bosing.")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🛒 Xarid qilish / Murojaat", url="https://t.me/jasurbrzl"))
    await message.answer(ALMAZ_TEXT, parse_mode="Markdown", reply_markup=markup)

@dp.message_handler(text="🎁 Tekin Nastroykalar")
async def show_free(message: types.Message):
    if not await check_subscription(message.from_user.id):
        return await message.answer("Avval obuna bo'ling! /start ni bosing.")
    if not db_free_settings:
        await message.answer("⚠️ Hozircha tekin nastroykalar mavjud emas, tez kunda qo'shiladi!")
        return
    markup = types.InlineKeyboardMarkup(row_width=1)
    for item in db_free_settings:
        markup.add(types.InlineKeyboardButton(f"⚙️ {item['name']}", callback_data=f"get_free_{item['id']}"))
    await message.answer("🎁 Mavjud tekin nastroykalar:", reply_markup=markup)

@dp.callback_query_handler(text_startswith="get_free_")
async def send_free(callback: types.CallbackQuery):
    item_id = int(callback.data.split("_")[2])
    item = next((i for i in db_free_settings if i['id'] == item_id), None)
    if item:
        await callback.message.answer(f"Siz tanlagan nastroyka: **{item['name']}**\n\n{item['content']}", parse_mode="Markdown")
    else:
        await callback.answer("Topilmadi!", show_alert=True)

@dp.message_handler(text="💎 Soft Nastroyka (Pullik)")
async def show_paid(message: types.Message):
    if not await check_subscription(message.from_user.id):
        return await message.answer("Avval obuna bo'ling! /start ni bosing.")
    if not db_paid_settings:
        await message.answer("⚠️ Hozircha pullik soft nastroykalar mavjud emas.")
        return
    markup = types.InlineKeyboardMarkup(row_width=1)
    for item in db_paid_settings:
        markup.add(types.InlineKeyboardButton(f"💎 {item['name']} (Pullik)", callback_data=f"get_paid_{item['id']}"))
    await message.answer("💎 Pullik soft nastroykalar:", reply_markup=markup)

@dp.callback_query_handler(text_startswith="get_paid_")
async def send_paid(callback: types.CallbackQuery):
    item_id = int(callback.data.split("_")[2])
    item = next((i for i in db_paid_settings if i['id'] == item_id), None)
    if item:
        await callback.message.answer(f"💎 **{item['name']}**\n\n{item['content']}\n\n*Sotib olish uchun adminga murojaat qiling.*", parse_mode="Markdown")
    else:
        await callback.answer("Topilmadi!", show_alert=True)

# --- ADMIN PANEL ---
@dp.message_handler(text="👑 Admin Panel")
async def admin_panel(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("➕ Tekin Nastroyka qo'shish"),
        types.KeyboardButton("🗑 Tekin Nastroykani o'chirish")
    )
    markup.add(
        types.KeyboardButton("➕ Soft (Pullik) qo'shish"),
        types.KeyboardButton("🗑 Soft Nastroykani o'chirish")
    )
    markup.add(
        types.KeyboardButton("📢 Obuna kanal qo'shish"),
        types.KeyboardButton("❌ Obuna kanalni o'chirish")
    )
    markup.add(types.KeyboardButton("🔙 Asosiy Menyu"))
    await message.answer("👑 Admin boshqaruv paneli:", reply_markup=markup)

@dp.message_handler(text="🔙 Asosiy Menyu")
async def back_to_main(message: types.Message):
    await message.answer("Asosiy menyu:", reply_markup=get_main_menu(message.from_user.id))

# --- TEKIN NASTROYKA QO'SHISH/O'CHIRISH ---
@dp.message_handler(text="➕ Tekin Nastroyka qo'shish")
async def add_free_start(message: types.Message):
    if message.from_user.id not in ADMIN_IDS: return
    await message.answer("Yangi tekin nastroyka uchun **nom** kiriting:")
    await AdminStates.waiting_for_free_name.set()

@dp.message_handler(state=AdminStates.waiting_for_free_name)
async def process_free_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Endi ushbu nastroyka uchun **matn yoki fayl** yuboring:")
    await AdminStates.waiting_for_free_content.set()

@dp.message_handler(state=AdminStates.waiting_for_free_content, content_types=types.ContentTypes.ANY)
async def process_free_content(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data.get("name")
    content = message.text if message.text else "Fayl yuklandi"
    new_id = len(db_free_settings) + 1
    db_free_settings.append({"id": new_id, "name": name, "content": content})
    await state.finish()
    await message.answer("✅ Tekin nastroyka qo'shildi!", reply_markup=get_main_menu(message.from_user.id))

@dp.message_handler(text="🗑 Tekin Nastroykani o'chirish")
async def del_free_menu(message: types.Message):
    if message.from_user.id not in ADMIN_IDS: return
    if not db_free_settings: return await message.answer("O'chiriladigani yo'q.")
    markup = types.InlineKeyboardMarkup(row_width=1)
    for i in db_free_settings:
        markup.add(types.InlineKeyboardButton(f"❌ O'chirish: {i['name']}", callback_data=f"dfree_{i['id']}"))
    await message.answer("O'chirish uchun tanlang:", reply_markup=markup)

@dp.callback_query_handler(text_startswith="dfree_")
async def process_dfree(callback: types.CallbackQuery):
    item_id = int(callback.data.split("_")[1])
    global db_free_settings
    db_free_settings = [i for i in db_free_settings if i['id'] != item_id]
    await callback.message.delete()
    await callback.message.answer("✅ O'chirildi!")

# --- SOFT (PULLIK) QO'SHISH/O'CHIRISH ---
@dp.message_handler(text="➕ Soft (Pullik) qo'shish")
async def add_paid_start(message: types.Message):
    if message.from_user.id not in ADMIN_IDS: return
    await message.answer("Pullik soft nastroyka uchun **nom** kiriting:")
    await AdminStates.waiting_for_paid_name.set()

@dp.message_handler(state=AdminStates.waiting_for_paid_name)
async def process_paid_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Endi soft uchun **matn yoki fayl** yuboring:")
    await AdminStates.waiting_for_paid_content.set()

@dp.message_handler(state=AdminStates.waiting_for_paid_content, content_types=types.ContentTypes.ANY)
async def process_paid_content(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data.get("name")
    content = message.text if message.text else "Fayl yuklandi"
    new_id = len(db_paid_settings) + 1
    db_paid_settings.append({"id": new_id, "name": name, "content": content})
    await state.finish()
    await message.answer("✅ Pullik soft qo'shildi!", reply_markup=get_main_menu(message.from_user.id))

@dp.message_handler(text="🗑 Soft Nastroykani o'chirish")
async def del_paid_menu(message: types.Message):
    if message.from_user.id not in ADMIN_IDS: return
    if not db_paid_settings: return await message.answer("O'chiriladigani yo'q.")
    markup = types.InlineKeyboardMarkup(row_width=1)
    for i in db_paid_settings:
        markup.add(types.InlineKeyboardButton(f"❌ O'chirish: {i['name']}", callback_data=f"dpaid_{i['id']}"))
    await message.answer("O'chirish uchun tanlang:", reply_markup=markup)

@dp.callback_query_handler(text_startswith="dpaid_")
async def process_dpaid(callback: types.CallbackQuery):
    item_id = int(callback.data.split("_")[1])
    global db_paid_settings
    db_paid_settings = [i for i in db_paid_settings if i['id'] != item_id]
    await callback.message.delete()
    await callback.message.answer("✅ O'chirildi!")

# --- MAJBURIY OBUNA KANAL/GURUH QO'SHISH VA O'CHIRISH ---
@dp.message_handler(text="📢 Obuna kanal qo'shish")
async def add_channel_start(message: types.Message):
    if message.from_user.id not in ADMIN_IDS: return
    await message.answer("Yangi kanal yoki guruh username'ini yuboring (masalan: `@kanal_nomi`):")
    await AdminStates.waiting_for_channel.set()

@dp.message_handler(state=AdminStates.waiting_for_channel)
async def process_add_channel(message: types.Message, state: FSMContext):
    channel = message.text.strip()
    if channel not in REQUIRED_CHANNELS:
        REQUIRED_CHANNELS.append(channel)
    await state.finish()
    await message.answer(f"✅ {channel} majburiy obunalarga qo'shildi!", reply_markup=get_main_menu(message.from_user.id))

@dp.message_handler(text="❌ Obuna kanalni o'chirish")
async def remove_channel_menu(message: types.Message):
    if message.from_user.id not in ADMIN_IDS: return
    if not REQUIRED_CHANNELS: return await message.answer("Hozircha majburiy kanallar yo'q.")
    markup = types.InlineKeyboardMarkup(row_width=1)
    for ch in REQUIRED_CHANNELS:
        markup.add(types.InlineKeyboardButton(f"O'chirish: {ch}", callback_data=f"rm_ch_{ch}"))
    await message.answer("O'chiriladigan kanalni tanlang:", reply_markup=markup)

@dp.callback_query_handler(text_startswith="rm_ch_")
async def process_remove_channel(callback: types.CallbackQuery):
    ch_name = callback.data.replace("rm_ch_", "")
    if ch_name in REQUIRED_CHANNELS:
        REQUIRED_CHANNELS.remove(ch_name)
    await callback.message.delete()
    await callback.message.answer(f"✅ {ch_name} majburiy obunalardan olib tashlandi!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
