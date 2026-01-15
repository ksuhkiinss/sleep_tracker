import sqlite3

def create_sleep_table():
    conn = sqlite3.connect("database/sleep_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sleep (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            sleep_time TEXT NOT NULL,
            wake_time TEXT NOT NULL,
            duration REAL,
            rating INTEGER,
            notes TEXT
        )
    """)
    conn.commit()
    conn.close()

# Викликаємо функцію одразу, щоб таблиця створилась
if __name__ == "__main__":
    create_sleep_table()
