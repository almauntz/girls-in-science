import sqlite3

conn = sqlite3.connect('sql_app.db')
cursor = conn.cursor()

# Dodaj kolone ako ne postoje
try:
    cursor.execute("ALTER TABLE students ADD COLUMN has_business_idea VARCHAR")
    print("Added has_business_idea column")
except sqlite3.OperationalError as e:
    print(f"has_business_idea: {e}")

try:
    cursor.execute("ALTER TABLE students ADD COLUMN session_commitment BOOLEAN DEFAULT 0")
    print("Added session_commitment column")
except sqlite3.OperationalError as e:
    print(f"session_commitment: {e}")

try:
    cursor.execute("ALTER TABLE students ADD COLUMN consent_data BOOLEAN DEFAULT 0")
    print("Added consent_data column")
except sqlite3.OperationalError as e:
    print(f"consent_data: {e}")

try:
    cursor.execute("ALTER TABLE students ADD COLUMN consent_evaluation BOOLEAN DEFAULT 0")
    print("Added consent_evaluation column")
except sqlite3.OperationalError as e:
    print(f"consent_evaluation: {e}")

conn.commit()
conn.close()

print("Database updated successfully!")
