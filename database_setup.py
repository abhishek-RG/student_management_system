import sqlite3

conn = sqlite3.connect('school.db')
cursor = conn.cursor()

# This is the new, correct schema for the 'students' table
# It includes the 'category' column.
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL DEFAULT 'General'
)
''')

# 'courses' table is unchanged
cursor.execute('''
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT NOT NULL,
    student_id INTEGER,
    FOREIGN KEY(student_id) REFERENCES students(id)
)
''')

print("Database and tables created successfully!")
conn.commit()
conn.close()