import streamlit as st
import sqlite3
from streamlit_cookies_manager import EncryptedCookieManager

st.header("Вхід")

# Ініціалізація cookies
cookies = EncryptedCookieManager(
    prefix="sleep_app",
    password="super_secret_password"  # можеш змінити на щось своє
)

if not cookies.ready():
    st.stop()

# Вхід користувача через форму
username = st.text_input("Імʼя користувача")
password = st.text_input("Пароль", type="password")

if st.button("Увійти"):
    conn = sqlite3.connect("database/sleep_data.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE username = ? AND password = ?",
        (username, password)
    )
    user = cursor.fetchone()
    conn.close()

    if user:
        # Зберігаємо в session_state
        st.session_state["user_id"] = user[0]
        st.session_state["username"] = username

        # Зберігаємо в cookies
        cookies["user_id"] = str(user[0])
        cookies["username"] = username
        cookies.save()

        st.success(f"Вітаю, {username}!")
    else:
        st.error("Невірний логін або пароль")
