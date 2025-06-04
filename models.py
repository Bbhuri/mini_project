from db import get_connection
import config
import os
import sqlite3

def create_student(student_id, student_name, branch):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        command = "INSERT INTO students(student_id, student_name, branch) VALUES (?, ?, ?)"
        cursor.execute(command, (student_id, student_name, branch))
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError("Student ID already exists")
    finally:
        conn.close()

def read_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    users = cursor.fetchall()
    conn.close()
    return users

def read_student_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    command="SELECT * FROM students WHERE id =?"
    cursor.execute(command, (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def update_student(id,student_id, student_name, branch):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        command="UPDATE students SET student_id = ?, student_name = ?, branch = ? WHERE id = ?"
        cursor.execute(command, (student_id,student_name, branch, id))
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError("Student ID already exists")
    finally:
        conn.close()

def delete_student(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    command="DELETE FROM students WHERE id = ?"
    cursor.execute(command, (user_id,))
    conn.commit()
    conn.close()
    return

def create_course(course_id,course_name,teacher,description):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        command = "INSERT INTO courses(course_id, course_name, teacher,description) VALUES (?, ?, ?, ?)"
        cursor.execute(command, (course_id, course_name, teacher,description))
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError("Course ID already exists")
    finally:
        conn.close()

def read_courses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    conn.close()
    return courses

def read_course_by_id(id):
    conn = get_connection()
    cursor = conn.cursor()
    command="SELECT * FROM courses WHERE id =?"
    cursor.execute(command, (id,))
    course = cursor.fetchone()
    conn.close()
    return course

def update_course(id,course_id, course_name, teacher, description):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        command="UPDATE courses SET course_id = ?, course_name = ?, teacher = ?, description = ? WHERE id = ?"
        cursor.execute(command, (course_id,course_name, teacher , description, id,))
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError("Course ID already exists")
    finally:
        conn.close()

def add_student_to_course(student_id, course_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        command = "INSERT INTO enrollments(student_id, course_id) VALUES (?,?)"
        cursor.execute(command, (student_id, course_id))
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError("Student is already enrolled in this course")
    finally:
        conn.close()

def remove_student_from_course(student_id, course_id):
    conn = get_connection()
    cursor = conn.cursor()
    command="DELETE FROM enrollments WHERE student_id =? AND course_id =?"
    cursor.execute(command, (student_id, course_id))
    conn.commit()
    conn.close()
    return

def read_enrollments():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM enrollments")
    enrollments = cursor.fetchall()
    conn.close()
    return enrollments

def find_enrolled_students(course_id):
    conn = get_connection()
    cursor = conn.cursor()
    command="SELECT student_id FROM enrollments WHERE course_id =?"
    cursor.execute(command, (course_id,))
    enrolled_students = cursor.fetchall()
    conn.close()
    return enrolled_students

def delete_course(id):
    conn = get_connection()
    cursor = conn.cursor()
    command="DELETE FROM courses WHERE id = ?"
    cursor.execute(command, (id,))
    conn.commit()
    conn.close()
    return

def read_grades_for_course(course_id):
    conn = get_connection()
    cursor = conn.cursor()
    command = """
        SELECT s.student_id, s.student_name
        FROM students s
        JOIN enrollments e ON s.id = e.student_id
        WHERE e.course_id = ?
    """
    cursor.execute(command, (course_id,))
    student_rows = cursor.fetchall()
    conn.close()
    return student_rows

def get_assessments_for_course(course_id):
    conn = get_connection()
    cursor = conn.cursor()
    command = """
        SELECT a.id, a.title, a.max_score
        FROM assessments a
        JOIN courses c ON a.course_id = c.id
        WHERE c.id =?
    """
    cursor.execute(command, (course_id,))
    assessment_rows = cursor.fetchall()
    conn.close()
    return assessment_rows

def insert_assessment(title, course_id, max_score):
    conn = get_connection()
    cursor = conn.cursor()
    command = "INSERT INTO assessments (title, course_id, max_score) VALUES (?, ?, ?)"
    cursor.execute(command, (title, course_id, max_score))
    conn.commit()
    conn.close()

def update_assessment(assessment_id, title, max_score):
    conn = get_connection()
    cursor = conn.cursor()
    command = "UPDATE assessments SET title=?, max_score=? WHERE id=?"
    cursor.execute(command, (title,  max_score, assessment_id))
    conn.commit()
    conn.close()

def delete_assessment(assessment_id):
    conn = get_connection()
    cursor = conn.cursor()
    command = "DELETE FROM assessments WHERE id=?"
    cursor.execute(command, (assessment_id,))
    conn.commit()
    conn.close()

def get_assessment_by_id(assessment_id):
    conn = get_connection()
    cursor = conn.cursor()
    command = "SELECT * FROM assessments WHERE id=?"
    cursor.execute(command, (assessment_id,))
    assessment = cursor.fetchone()
    conn.close()
    return assessment

def insert_grade(student_id, assessment_id, score):
    conn = get_connection()
    cursor = conn.cursor()
    command = "INSERT INTO grade (student_id, assessment_id, score) VALUES (?, ?, ?)"
    cursor.execute(command, (student_id, assessment_id, score))
    conn.commit()
    conn.close()

def update_grade(grade_id, score):
    conn = get_connection()
    cursor = conn.cursor()
    command = "UPDATE grade SET score=? WHERE id=?"
    cursor.execute(command, (score, grade_id))
    conn.commit()
    conn.close()