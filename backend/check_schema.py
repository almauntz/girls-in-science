"""
Direktno SQL script za popravku baze
"""
import sqlite3

conn = sqlite3.connect('sql_app.db')
cursor = conn.cursor()

# Provjera šta stulje u mentors tabeli
cursor.execute("PRAGMA table_info(mentors)")
columns = cursor.fetchall()

print("Kolone u mentors tabeli:")
for col in columns:
    print(f"  - {col[1]} ({col[2]})")

conn.close()
