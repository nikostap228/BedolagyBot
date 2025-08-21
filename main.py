import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
import commands

load_dotenv()
commands.migrate_db()

# ===== Кнопки =====
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Увеличить пенис")],
        [KeyboardButton(text="Оскорбиться")],
        [KeyboardButton(text="Мой размер")],
        [KeyboardButton(text="Таблица пенисов")]
    ],
    resize_keyboard=True
)

start_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Старт")]],
    resize_keyboard=True
)

# ===== Router =====
router = Router()

@router.message(F.text == "/start")
async def start_cmd(message: Message):
    await message.answer("Алло бедолага, выбери действие:", reply_markup=main_kb)

@router.message(F.text == "Увеличить пенис")
async def dick_cmd(message: Message):
    response = commands.increase_dick(message.from_user.id, message.from_user.username)
    await message.answer(response, reply_markup=main_kb)

@router.message(F.text == "Оскорбиться")
async def offend_cmd(message: Message):
    response = commands.get_offended()
    await message.answer(response, reply_markup=main_kb)

@router.message(F.text == "Мой размер")
async def my_size_cmd(message: Message):
    response = commands.get_current_size(message.from_user.id)
    await message.answer(response, reply_markup=main_kb)

@router.message(F.text == "Таблица пенисов")
async def leaderboard_cmd(message: Message):
    response = commands.get_leaderboard()
    await message.answer(response, parse_mode="Markdown", reply_markup=main_kb)

# ===== Reset Webhook и запуск бота =====
async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"))

    # Сброс webhook на случай старого экземпляра
    await bot.delete_webhook(drop_pending_updates=True)

    dp = Dispatcher()
    dp.include_router(router)

    print("Бот запущен, polling...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
