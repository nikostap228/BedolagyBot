import sqlite3
import random
import time
import os

DB_FILE = "user_data.db"


def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            size INTEGER DEFAULT 0,
            last_increase INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


init_db()


insults = [
    "Пидорас",
    "Ну ты гомик ряльно",
    "Иди умойся ряльно",
    "Катя молодец",
    "У Сани скайлайн гнилой"
]


def get_user(user_id: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT size, last_increase, username FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def create_user(user_id: int, username: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
    conn.commit()
    conn.close()


def update_user(user_id: int, size: int, last_increase: int, username: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET size = ?, last_increase = ?, username = ? WHERE user_id = ?",
        (size, last_increase, username, user_id)
    )
    conn.commit()
    conn.close()


def increase_dick(user_id: int, username: str) -> str:
    create_user(user_id, username)
    user = get_user(user_id)

    if user:
        current_size, last_time, _ = user
    else:
        current_size, last_time = 0, 0

    current_time = int(time.time())

    if current_time - last_time < 3600:
        remaining = 3600 - (current_time - last_time)
        minutes = remaining // 60
        return f"Ты уже увеличивал недавно! Подожди ещё {minutes} мин."

    if random.random() < 0.7:
        change = random.randint(1, 15)
    else:
        change = random.randint(-5, -1)

    new_size = current_size + change
    if new_size < 0:
        new_size = 0

    update_user(user_id, new_size, current_time, username)

    return f"Изменение: {change:+} см.\nТеперь твой размер: {new_size} см."


def get_offended() -> str:
    return random.choice(insults)


def get_current_size(user_id: int) -> str:
    user = get_user(user_id)
    size = user[0] if user else 0
    return f"Твой текущий размер: {size} см."


def get_leaderboard() -> str:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT username, size FROM users ORDER BY size DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return "Таблица пуста. Никто еще не увеличил пенис."

    leaderboard = "🏆 *Таблица пенисов*\n\n"
    for i, (username, size) in enumerate(rows, start=1):
        name = username if username else f"Пользователь {i}"
        leaderboard += f"{i}. {name} — {size} см\n"

    return leaderboard


def migrate_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Создаем таблицу, если её нет
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        size INTEGER DEFAULT 0,
        last_update INTEGER DEFAULT 0
    )
    """)

    # Проверяем наличие колонок и добавляем при необходимости
    cursor.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cursor.fetchall()]

    if "username" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN username TEXT")
    if "size" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN size INTEGER DEFAULT 0")
    if "last_update" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN last_update INTEGER DEFAULT 0")

    conn.commit()
    conn.close()
