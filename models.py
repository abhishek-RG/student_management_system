import sqlite3

class DatabaseManager:
    # ... (init, enroll_in_course, get_student_courses, student_exists are the same) ...
    def __init__(self, db_name='school.db'):
        self.conn = sqlite3.connect(db_name)
        self.conn.execute("PRAGMA foreign_keys = 1") # Enforce foreign key constraints
        self.cursor = self.conn.cursor()

    # --- MODIFIED FUNCTION ---
    def add_student(self, student_id, name, category):
        """Adds a new student with a specific ID and category."""
        # The INSERT query now includes id and category columns.
        self.cursor.execute("INSERT INTO students (id, name, category) VALUES (?, ?, ?)", 
                            (student_id, name, category))
        self.conn.commit()
        print(f"Student '{name}' with ID {student_id} added successfully.")

    def enroll_in_course(self, student_id, course_name):
        self.cursor.execute("INSERT INTO courses (student_id, course_name) VALUES (?, ?)", (student_id, course_name))
        self.conn.commit()
        print(f"Student ID {student_id} enrolled in '{course_name}'.")

    def get_student_courses(self, student_id):
        self.cursor.execute('''
            SELECT s.name, c.course_name
            FROM students s
            JOIN courses c ON s.id = c.student_id
            WHERE s.id = ?
        ''', (student_id,))
        return self.cursor.fetchall()

    def student_exists(self, student_id):
        self.cursor.execute("SELECT id FROM students WHERE id = ?", (student_id,))
        return self.cursor.fetchone() is not None

    # --- MODIFIED FUNCTION ---
    def get_all_students(self):
        """Retrieves all students including their category."""
        # The SELECT query now also fetches the category.
        self.cursor.execute("SELECT id, name, category FROM students ORDER BY id")
        return self.cursor.fetchall()
        
    # --- NEW FUNCTION ---
    def delete_student(self, student_id):
        # Step 1: Delete all courses linked to this student from the 'courses' table first.
        self.cursor.execute("DELETE FROM courses WHERE student_id = ?", (student_id,))
        
        # Step 2: Now that the courses are gone, it's safe to delete the student.
        self.cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        
        # Save the changes to the database
        self.conn.commit()
        print(f"Student with ID {student_id} and their courses were deleted successfully.")

    def close(self):
        self.conn.close()