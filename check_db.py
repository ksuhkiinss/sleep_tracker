import sqlite3

conn = sqlite3.connect("database/sleep_data.db")
cursor = conn.cursor()

# показує всі таблиці
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print("Таблиці в базі:")
for table in tables:
    print("-", table[0])

conn.close()
