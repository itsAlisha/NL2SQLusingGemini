import sqlite3

# Connect to SQLite
connection = sqlite3.connect("student.db")
cursor = connection.cursor()

# Drop tables if they exist (to reset the database)
cursor.execute("DROP TABLE IF EXISTS STUDENT;")
cursor.execute("DROP TABLE IF EXISTS TEACHERS;")
cursor.execute("DROP TABLE IF EXISTS COURSES;")

# Create TEACHERS table
cursor.execute("""
CREATE TABLE TEACHERS (
    Instructor_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name VARCHAR(50),
    Department VARCHAR(50)
);
""")

# Create COURSES table
cursor.execute("""
CREATE TABLE COURSES (
    Course_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Course_Name VARCHAR(50),
    Instructor_ID INTEGER,
    FOREIGN KEY (Instructor_ID) REFERENCES TEACHERS(Instructor_ID)
);
""")

# Create STUDENT table with Course_ID
cursor.execute("""
CREATE TABLE STUDENT (
    Student_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME VARCHAR(50),
    CLASS VARCHAR(50),
    SECTION VARCHAR(10),
    MARKS INTEGER,
    Course_ID INTEGER,
    FOREIGN KEY (Course_ID) REFERENCES COURSES(Course_ID)
);
""")

# Insert data into TEACHERS
cursor.executemany("INSERT INTO TEACHERS (Name, Department) VALUES (?, ?);", [
    ('Dr. Smith', 'Machine Learning'),
    ('Prof. Johnson', 'Cloud Computing'),
    ('Dr. Lee', 'Big Data')
])

# Insert data into COURSES
cursor.executemany("INSERT INTO COURSES (Course_Name, Instructor_ID) VALUES (?, ?);", [
    ('Machine Learning', 2),
    ('Cloud Computing', 3),
    ('Big Data', 1)
])

# Insert data into STUDENT (including Course_ID)
cursor.executemany("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS, Course_ID) VALUES (?, ?, ?, ?, ?);", [
    ('Krish', 'Machine Learning', 'A', 90, 1),
    ('Sudhanshu', 'Machine Learning', 'B', 100, 1),
    ('Darius', 'Cloud Computing', 'A', 86, 2),
    ('Vikash', 'Big Data', 'A', 50, 3),
    ('Dipesh', 'Big Data', 'A', 35, 3)
])

# Commit and close the database connection
connection.commit()
connection.close()

print("Database setup complete!")
