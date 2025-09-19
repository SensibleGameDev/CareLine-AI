import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    message TEXT NOT NULL,
    timestamp DATETIME NOT NULL
)
""")

conn.commit()
conn.close()

print("База данных и таблица 'requests' успешно созданы.")