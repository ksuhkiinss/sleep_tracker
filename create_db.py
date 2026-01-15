import sqlite3

# Підключаємося (або створюємо) базу даних
conn = sqlite3.connect("database/sleep_data.db")
cursor = conn.cursor()

# Таблиця сну
cursor.execute("""
CREATE TABLE IF NOT EXISTS sleep (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    sleep_time TEXT,
    wake_time TEXT,
    duration REAL,
    rating INTEGER,
    notes TEXT
)
""")

# Таблиця користувачів
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

conn.commit()
conn.close()

print("База даних і таблиці створені!")
