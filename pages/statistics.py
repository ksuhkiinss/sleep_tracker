import streamlit as st
import sqlite3
import pandas as pd

st.header("Статистика сну 💤")

# --- Перевірка, чи користувач увійшов ---
if "user_id" not in st.session_state:
    st.warning("Будь ласка, увійдіть, щоб переглянути статистику")
    st.stop()

# --- Отримуємо дані з бази ---
conn = sqlite3.connect("database/sleep_data.db")
cursor = conn.cursor()
cursor.execute("""
    SELECT date, sleep_time, wake_time, duration, rating, notes
    FROM sleep
    WHERE user_id = ?
    ORDER BY date
""", (st.session_state["user_id"],))
rows = cursor.fetchall()
conn.close()

# --- Якщо записів немає ---
if not rows:
    st.info("У вас ще немає записів сну")
    st.stop()

# --- Перетворюємо в DataFrame ---
df = pd.DataFrame(rows, columns=["Дата", "Час засинання", "Час пробудження", "Тривалість (годин)", "Оцінка", "Нотатки"])
df["Дата"] = pd.to_datetime(df["Дата"])
df = df.set_index("Дата")

# --- Відображення таблиці ---
st.subheader("Таблиця сну")
st.dataframe(df)

# --- Графік тривалості сну ---
st.subheader("Графік тривалості сну")
st.line_chart(df["Тривалість (годин)"])
