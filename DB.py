import sqlite3


conn = sqlite3.connect("database.db")
c = conn.cursor()


c.execute("""
CREATE TABLE messages (
name TEXT,
email TEXT,
message TEXT
)
""")


conn.commit()
conn.close()

print("Database initialized successfully.")
