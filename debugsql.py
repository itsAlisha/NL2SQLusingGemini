import sqlite3

# Connect to the database
conn = sqlite3.connect("student.db")
cur = conn.cursor()

# List all tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cur.fetchall()
print("Tables in database:", tables)

# Check data in tables
for table in ["STUDENT", "TEACHERS", "COURSES"]:
    print(f"\nData from {table}:")
    try:
        cur.execute(f"SELECT * FROM {table} LIMIT 5;")
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except sqlite3.OperationalError as e:
        print(f"Error: {e}")

conn.close()
