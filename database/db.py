import sqlite3 
conn = sqlite3.connect("sleep_data.db") 
cursor = conn.cursor() 
conn.commit() 
conn.close() 
