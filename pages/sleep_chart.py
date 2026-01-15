import streamlit as st
import sqlite3
import pandas as pd
import altair as alt

st.header("Графік тривалості сну")

conn = sqlite3.connect("database/sleep_data.db")
df = pd.read_sql_query("SELECT * FROM sleep ORDER BY date ASC", conn)
conn.close()

if df.empty:
    st.info("Поки що немає записів сну")
else:
    df['date'] = pd.to_datetime(df['date'])
    
    chart = alt.Chart(df).mark_bar(color='blue').encode(
        x='date:T',
        y='duration:Q',
        tooltip=['date', 'duration', 'rating']
    )
    
    st.altair_chart(chart, use_container_width=True)
