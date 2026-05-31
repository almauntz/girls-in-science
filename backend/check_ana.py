import sqlite3

conn = sqlite3.connect('sql_app.db')
cursor = conn.cursor()

# Vidite sve podatke za Anu
cursor.execute("""
    SELECT * FROM students WHERE email = 'ana.student@example.com'
""")
columns = [description[0] for description in cursor.description]
student_data = cursor.fetchone()

print("Ana Jovanovic's data:")
for col, value in zip(columns, student_data):
    print(f"  {col}: {value}")

conn.close()
