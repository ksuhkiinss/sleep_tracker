import streamlit as st
import sqlite3
from datetime import datetime

# ========================
# Перевірка cookies / сесії
# ========================
#from streamlit_cookies_manager import EncryptedCookieManager

#cookies = EncryptedCookieManager(
#    prefix="sleep_app",
#    password="super_secret_password"
#)
#if not cookies.ready():
#    st.stop()

# Відновлюємо сесію з cookies
#if "user_id" not in st.session_state:
#    if "user_id" in cookies:
#        st.session_state["user_id"] = int(cookies["user_id"])
#        st.session_state["username"] = cookies.get("username")

# ========================
# Заголовок
# ========================
st.title("Sleep Tracker 💤")
st.write("Привіт! Це початок нашого трекера сну.")

# ========================
# Статус логіну
# ========================
if "user_id" in st.session_state:
    st.success(f"Ви увійшли як {st.session_state['username']}")

    # ========================
    # Швидкі кнопки "Засинаю" і "Прокидаюсь"
    # ========================
    col1, col2 = st.columns(2)

    if "sleep_start_time" not in st.session_state:
        st.session_state["sleep_start_time"] = None

    with col1:
        if st.button("💤 Засинаю"):
            st.session_state["sleep_start_time"] = datetime.now()
            st.success(f"Час засинання зафіксовано: {st.session_state['sleep_start_time'].strftime('%H:%M')}")

    with col2:
        if st.button("☀️ Прокидаюсь"):
            if st.session_state.get("sleep_start_time"):
                st.session_state["wake_time_temp"] = datetime.now()
                st.session_state["duration_temp"] = (st.session_state["wake_time_temp"] - st.session_state["sleep_start_time"]).seconds / 3600

                # Перетворимо тривалість на години та хвилини
                hours = int(st.session_state["duration_temp"])
                minutes = int((st.session_state["duration_temp"] - hours) * 60)

                st.info(f"Тривалість сну: {hours} год {minutes} хв")

                # --- Слайдер для оцінки сну ---
                rating = st.slider("Оцінка сну (1-5)", 1, 5, 3, key="quick_sleep_rating")

                if st.button("Зберегти сон"):
                    conn = sqlite3.connect("database/sleep_data.db")
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO sleep (date, sleep_time, wake_time, duration, rating, notes, user_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        st.session_state["sleep_start_time"].date().strftime("%Y-%m-%d"),
                        st.session_state["sleep_start_time"].strftime("%H:%M"),
                        st.session_state["wake_time_temp"].strftime("%H:%M"),
                        st.session_state["duration_temp"],
                        rating,
                        "",
                        st.session_state["user_id"]
                    ))
                    conn.commit()
                    conn.close()

                    st.success(f"Сон збережено! Тривалість: {hours} год {minutes} хв, оцінка: {rating}")
                    st.session_state["sleep_start_time"] = None
                    del st.session_state["wake_time_temp"]
                    del st.session_state["duration_temp"]
                    del st.session_state["quick_sleep_rating"]

            else:
                st.warning("Спочатку натисніть 'Засинаю'")

else:
    st.warning("Ви не увійшли. Будь ласка, увійдіть")
