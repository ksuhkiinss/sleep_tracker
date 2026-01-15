import streamlit as st
import sqlite3

st.header("Реєстрація")

username = st.text_input("Імʼя користувача")
password = st.text_input("Пароль", type="password")
password2 = st.text_input("Повторіть пароль", type="password")

if st.button("Зареєструватись"):
    if not username or not password or not password2:
        st.error("Заповніть усі поля")
    elif password != password2:
        st.error("Паролі не співпадають")
    else:
        conn = sqlite3.connect("database/sleep_data.db")
        cursor = conn.cursor()

        # перевірка, чи існує користувач
        cursor.execute(
            "SELECT id FROM users WHERE username = ?",
            (username,)
        )
        existing = cursor.fetchone()

        if existing:
            st.error("Користувач з таким імʼям вже існує")
        else:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
            st.success("Реєстрація успішна! Тепер увійдіть.")
        
        conn.close()
