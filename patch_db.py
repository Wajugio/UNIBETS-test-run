import sqlite3

conn = sqlite3.connect("users.db")
c = conn.cursor()
c.execute("ALTER TABLE bets ADD COLUMN timestamp TEXT")
conn.commit()
conn.close()
print("✅ Timestamp column added.")
