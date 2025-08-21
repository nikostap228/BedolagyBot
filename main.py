import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram import F
import commands

# Загружаем переменные окружения
load_dotenv()

# Миграция базы данных
commands.migrate_db()

# Создаем маршрутизатор
router = Router()

# Главное меню
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Увеличить пенис")],
        [KeyboardButton(text="Оскорбиться")],
        [KeyboardButton(text="Мой размер")],
        [KeyboardButton(text="Таблица пенисов")]
    ],
    resize_keyboard=True
)

# Стартовое меню
start_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Старт")]],
    resize_keyboard=True
)


# Обработчики команд и кнопок
@router.message(F.text == "/start")
async def start_cmd(message: Message):
    await message.answer("Алло бедолага, выбери действие:", reply_markup=main_kb)


@router.message(F.text == "Увеличить пенис")
async def dick_cmd(message: Message):
    response = commands.increase_dick(message.from_user.id, message.from_user.username)
    await message.answer(response)


@router.message(F.text == "Оскорбиться")
async def offend_cmd(message: Message):
    response = commands.get_offended()
    await message.answer(response)


@router.message(F.text == "Мой размер")
async def my_size_cmd(message: Message):
    response = commands.get_current_size(message.from_user.id)
    await message.answer(response)


@router.message(F.text == "Таблица пенисов")
async def leaderboard_cmd(message: Message):
    response = commands.get_leaderboard()
    await message.answer(response, parse_mode="Markdown")


# Функция запуска бота
async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode="HTML")
    dp = Dispatcher()
    dp.include_router(router)
    print("Бот запущен и работает через polling!")
    # Запуск long polling без портов
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
