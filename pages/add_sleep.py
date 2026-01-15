import streamlit as st
import sqlite3
from datetime import datetime

st.header("Додати новий сон")

# --- Перевірка, чи користувач увійшов ---
if "user_id" not in st.session_state:
    st.warning("Будь ласка, увійдіть, щоб додавати сон")
    st.stop()  # зупиняємо виконання сторінки

# --- Функція для перетворення рядка на час ---
def parse_time(t_str):
    t_str = t_str.replace(".", ":")  # замінюємо крапку на двокрапку
    try:
        t = datetime.strptime(t_str, "%H:%M").time()
        return t
    except:
        return None

# --- Форма для введення сну ---
with st.form(key="sleep_form"):
    date = st.date_input("Дата сну", datetime.today())
    sleep_time_str = st.text_input("Час засинання (формат 23:30 або 23.30)", key="sleep")
    wake_time_str = st.text_input("Час пробудження (формат 07:00 або 7.00)", key="wake")
    rating = st.slider("Оцінка сну (1-5)", 1, 5, 3)
    notes = st.text_area("Нотатки")
    
    submit_button = st.form_submit_button(label="Додати сон")

# --- Обробка форми ---
if submit_button:
    sleep_time = parse_time(sleep_time_str)
    wake_time = parse_time(wake_time_str)
    
    if sleep_time is None or wake_time is None:
        st.error("Будь ласка, введіть час у правильному форматі (наприклад, 23:30 або 23.30)")
    else:
        # обчислення тривалості
        duration = (datetime.combine(date, wake_time) - datetime.combine(date, sleep_time)).seconds / 3600
        if duration < 0:
            duration += 24

        # --- Зберігаємо сон в базі з прив'язкою до користувача ---
        conn = sqlite3.connect("database/sleep_data.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO sleep (date, sleep_time, wake_time, duration, rating, notes, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            date.strftime("%Y-%m-%d"),
            sleep_time.strftime("%H:%M"),
            wake_time.strftime("%H:%M"),
            duration,
            rating,
            notes,
            st.session_state["user_id"]  # тут прив'язка до користувача
        ))
        conn.commit()
        conn.close()
        
        # Перетворимо тривалість на години та хвилини
        hours = int(duration)
        minutes = int((duration - hours) * 60)

        st.success(f"Запис сну додано! Тривалість: {hours} год {minutes} хв")
