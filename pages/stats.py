import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

st.header("Редагування та видалення сну")

conn = sqlite3.connect("database/sleep_data.db")
df = pd.read_sql_query("SELECT * FROM sleep ORDER BY date ASC", conn)
conn.close()

if df.empty:
    st.info("Поки що немає записів сну")
else:
    for idx, row in df.iterrows():
        st.write(f"**Дата:** {row['date']}  |  **Тривалість:** {int(row['duration'])} год {int((row['duration'] - int(row['duration']))*60)} хв  |  **Оцінка:** {row['rating']}")
        st.write(f"Нотатки: {row['notes']}")
        
        col1, col2 = st.columns(2)
        
        # Редагування
        with col1:
            if st.button("Редагувати", key=f"edit_{row['id']}"):
                with st.form(key=f"edit_form_{row['id']}"):
                    date = st.date_input("Дата сну", datetime.strptime(row['date'], "%Y-%m-%d"))
                    sleep_time_str = st.text_input("Час засинання", row['sleep_time'], key=f"sleep_edit_{row['id']}")
                    wake_time_str = st.text_input("Час пробудження", row['wake_time'], key=f"wake_edit_{row['id']}")
                    rating = st.slider("Оцінка сну", 1, 5, int(row['rating']))
                    notes = st.text_area("Нотатки", row['notes'])
                    submit_edit = st.form_submit_button("Зберегти зміни")
                    
                    if submit_edit:
                        sleep_time = datetime.strptime(sleep_time_str.replace(".", ":"), "%H:%M").time()
                        wake_time = datetime.strptime(wake_time_str.replace(".", ":"), "%H:%M").time()
                        duration = (datetime.combine(date, wake_time) - datetime.combine(date, sleep_time)).seconds / 3600
                        if duration < 0:
                            duration += 24
                        
                        conn = sqlite3.connect("database/sleep_data.db")
                        cursor = conn.cursor()
                        cursor.execute("""
                            UPDATE sleep SET date=?, sleep_time=?, wake_time=?, duration=?, rating=?, notes=?
                            WHERE id=?
                        """, (date.strftime("%Y-%m-%d"), sleep_time.strftime("%H:%M"), wake_time.strftime("%H:%M"), duration, rating, notes, row['id']))
                        conn.commit()
                        conn.close()
                        st.success("Запис оновлено!")
                        st.experimental_rerun()
        
        # Видалення
        with col2:
            if st.button("Видалити", key=f"delete_{row['id']}"):
                conn = sqlite3.connect("database/sleep_data.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM sleep WHERE id=?", (row['id'],))
                conn.commit()
                conn.close()
                st.warning("Запис видалено!")
                st.experimental_rerun()
