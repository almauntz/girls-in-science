import sqlite3

conn = sqlite3.connect('sql_app.db')
cursor = conn.cursor()

# Vidite sve studente
cursor.execute("SELECT id, first_name, last_name, email, areas_of_interest FROM students")
students = cursor.fetchall()

print("All students in database:")
for student in students:
    print(f"  {student[0]}: {student[1]} {student[2]} - {student[3]}")
    print(f"     Areas: {student[4]}")

conn.close()
