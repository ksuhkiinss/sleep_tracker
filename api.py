from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

DB_PATH = "database/sleep_data.db"  # твоя існуюча база

# ==============================
# Додати новий сон (POST)
# ==============================
@app.route('/sleep', methods=['POST'])
def add_sleep():
    data = request.get_json()

    user_id = data.get("user_id")
    date = data.get("date")
    sleep_time = data.get("sleep_time")
    wake_time = data.get("wake_time")
    duration = data.get("duration")
    rating = data.get("rating")
    notes = data.get("notes", "")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO sleep (date, sleep_time, wake_time, duration, rating, notes, user_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (date, sleep_time, wake_time, duration, rating, notes, user_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Sleep added"}), 201

# ==============================
# Отримати всі записи (GET)
# ==============================
@app.route('/sleep/<int:user_id>', methods=['GET'])
def get_sleep(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, date, sleep_time, wake_time, duration, rating, notes FROM sleep WHERE user_id=?", (user_id,))
    rows = cursor.fetchall()
    conn.close()

    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "date": row[1],
            "sleep_time": row[2],
            "wake_time": row[3],
            "duration": row[4],
            "rating": row[5],
            "notes": row[6]
        })

    return jsonify(result), 200

if __name__ == "__main__":
    app.run(debug=True)
