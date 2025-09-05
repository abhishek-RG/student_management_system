from flask import Flask, render_template, request, redirect, url_for, flash
from models import DatabaseManager
import sqlite3 # Import for catching database errors

app = Flask(__name__)
# A secret key is required for flash messages
app.config['SECRET_KEY'] = 'your_super_secret_key'

@app.route('/')
def index():
    db = DatabaseManager()
    students = db.get_all_students()
    student_data = []
    for student_tuple in students:
        student_id, student_name, student_category = student_tuple # Unpack category
        courses = db.get_student_courses(student_id)
        student_data.append({
            'id': student_id,
            'name': student_name,
            'category': student_category, # Add category to data
            'courses': [course[1] for course in courses]
        })
    db.close()
    return render_template('index.html', students=student_data)

@app.route('/add_student', methods=['POST'])
def add_student():
    db = DatabaseManager()
    try:
        student_id = request.form['student_id']
        student_name = request.form['student_name']
        category = request.form['category']
        if student_id and student_name and category:
            db.add_student(student_id, student_name, category)
            flash(f"Student '{student_name}' added successfully!", 'success')
    except sqlite3.IntegrityError:
        # This error occurs if the student ID already exists
        flash(f"Error: Student ID '{student_id}' already exists.", 'error')
    except Exception as e:
        flash(f"An error occurred: {e}", 'error')
    finally:
        db.close()
    return redirect(url_for('index'))

# --- NEW DELETE ROUTE ---
@app.route('/delete_student/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    db = DatabaseManager()
    try:
        db.delete_student(student_id)
        flash(f"Student with ID {student_id} deleted successfully.", 'success')
    except Exception as e:
        flash(f"An error occurred while deleting: {e}", 'error')
    finally:
        db.close()
    return redirect(url_for('index'))

# ... (add_course route is unchanged) ...
@app.route('/add_course', methods=['POST'])
def add_course():
    db = DatabaseManager()
    student_id = request.form['student_id']
    course_name = request.form['course_name']
    if student_id and course_name:
        db.enroll_in_course(student_id, course_name)
    db.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)