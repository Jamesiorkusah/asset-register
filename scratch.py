import sqlite3

conn = sqlite3.connect("scratch.db")
cur = conn.cursor()


cur.execute("""
     CREATE TABLE IF NOT EXISTS assets (
         id INTEGER PRIMARY KEY,
         tag TEXT NOT NULL UNIQUE,
         model TEXT,
         status TEXT
     )
""")
conn.commit()
print("Table ready.")


cur.execute(
    "INSERT INTO assets (tag, model, status) VALUES (?, ?, ?)",
    ('NIT-001', 'HP Elitebook 840', 'in use')
)
cur.execute(
    "INSERT INTO assets (tag, model, status) VALUES (?, ?, ?)",
    ('NIT-003', 'HP LaserJet Pro ', 'in use')
)
conn.commit()
print("Data inserted.")

print("---Everything---")
for row in cur.execute("SELECT * FROM assets"):
    print(row)


print("---Only Faulty---")
for row in cur.execute("SELECT tag, model FROM assets WHERE status = 'Faulty'"):
    print(row)


print("---how many---")
print(cur.execute("SELECT COUNT(*) FROM assets").fetchone())

cur.execute("UPDATE assets SET status = ? WHERE tag = ?", ("Retired", "NIT-003"))
conn.commit()