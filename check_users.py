import sqlite3

conn = sqlite3.connect("database/sleep_data.db")
cursor = conn.cursor()

# структура таблиці users
cursor.execute("PRAGMA table_info(users)")
columns = cursor.fetchall()

print("Колонки в users:")
for col in columns:
    print(col)

print("\nДані в users:")
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

if rows:
    for row in rows:
        print(row)
else:
    print("Таблиця users поки пуста")

conn.close()
