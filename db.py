import sqlite3

conn = sqlite3.connect("database.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS resumes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    skills TEXT,
    match_score INTEGER,
    upload_time DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

conn.close()

print("Database and table created successfully")
