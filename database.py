import sqlite3

conn = sqlite3.connect("emails.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS scans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    prediction TEXT,
    confidence REAL
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")