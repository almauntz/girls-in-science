import sqlite3

conn = sqlite3.connect('sql_app.db')
cursor = conn.cursor()

# Proverite što je u tabeli students
cursor.execute("PRAGMA table_info(students)")
cols = cursor.fetchall()

print("Columns in students table:")
for col in cols:
    print(f"  {col[1]}: {col[2]}")

conn.close()
