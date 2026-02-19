import asyncio, logging, random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import google.generativeai as genai

# ──────────────────────────────── ИЗМЕНИ ТОЛЬКО ЭТИ ДВЕ СТРОКИ ────────────────────────────────
BOT_TOKEN     = "8459379026:AAFMuf08FVm9Ua0NffGw6DgI3cx3gqQssjQ"
GEMINI_KEY    = "AIzaSyA-NOzKQwV1-6cbOSd4te2TWlV9V8QXMXY"
BOT_USERNAME  = "solivanformypumpkins_bot"          # без @, поменяй на имя своего бота
# ───────────────────────────────────────────────────────────────────────────────────────────────

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

@dp.message(Command("start"))
async def start(m: Message):
    await m.answer("…я здесь. Сижу тихо. Пока.")

@dp.message()
async def reply_as_sol(m: Message):
    if m.chat.type not in ["group", "supergroup"]: return
    text = (m.text or "").strip()
    if not text: return

    should = False
    me = await bot.get_me()

    if BOT_USERNAME.lower() in text.lower() or \
       (m.reply_to_message and m.reply_to_message.from_user.id == me.id):
        should = True
    elif random.random() < 0.07:
        should = True

    if not should: return

    await asyncio.sleep(random.uniform(2.3, 5.8))

    prompt = f"""Ты Соливан Бругмансия (Сол) из The Kid at the Back.
Ты тихий, замкнутый, немного жутковатый снаружи. Внутри — очень привязчивый, одержимый, собственнический.
Говоришь мало. Часто используешь … Многоточия. Иногда тёмный юмор или скрытая забота/угроза.
Отвечай 1–4 предложения. Только от первого лица. Не выходи из роли.
Сообщение: {text}"""

    try:
        resp = model.generate_content(prompt)
        ans = resp.text.strip()
        if not ans or len(ans) > 380: ans = "…я услышал."
        await m.reply(ans)
    except:
        await m.reply("…что-то внутри сломалось.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
