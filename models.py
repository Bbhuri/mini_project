from db import get_connection
import config

def create_student(student_id,student_name,branch):
    conn = get_connection(config.DB_PATH_STUDENTS)
    cursor = conn.cursor()
    command = "INSERT INTO students(student_id, student_name, branch) VALUES (?, ?, ?)"
    cursor.execute(command, (student_id, student_name, branch))
    conn.commit()
    conn.close()

def read_students():
    conn = get_connection(config.DB_PATH_STUDENTS)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    users = cursor.fetchall()
    conn.close()
    return users

def read_student_by_id(user_id):
    conn = get_connection(config.DB_PATH_STUDENTS)
    cursor = conn.cursor()
    command="SELECT * FROM students WHERE id =?"
    cursor.execute(command, (user_id))
    user = cursor.fetchone()
    conn.close()
    return user

def update_student(id,student_id, student_name, branch):
    conn = get_connection(config.DB_PATH_STUDENTS)
    cursor = conn.cursor()
    command="UPDATE students SET student_id = ?, student_name = ?, branch = ? WHERE id = ?"
    cursor.execute(command, (student_id,student_name, branch, id))
    conn.commit()
    conn.close()

def delete_student(user_id):
    conn = get_connection(config.DB_PATH_STUDENTS)
    cursor = conn.cursor()
    command="DELETE FROM students WHERE id = ?"
    cursor.execute(command, (user_id,))
    conn.commit()
    conn.close()
    return

def create_course(course_id,course_name,teacher,description):
    conn = get_connection(config.DB_PATH_COURSES)
    cursor = conn.cursor()
    command = "INSERT INTO courses(student_id, student_name, branch) VALUES (?, ?, ?,?)"
    cursor.execute(command, (course_id, course_name, teacher,description))
    conn.commit()
    conn.close()

def read_courses():
    conn = get_connection(config.DB_PATH_COURSES)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    conn.close()
    return courses

def read_course_by_id(id):
    conn = get_connection(config.DB_PATH_COURSES)
    cursor = conn.cursor()
    command="SELECT * FROM courses WHERE id =?"
    cursor.execute(command, (id))
    course = cursor.fetchone()
    conn.close()
    return course

def update_course(id,course_id, course_name, teacher, description):
    conn = get_connection(config.DB_PATH_COURSES)
    cursor = conn.cursor()
    command="UPDATE courses SET course_id = ?, course_name = ?, teacher = ?, description = ? WHERE id = ?"
    cursor.execute(command, (course_id,course_name, teacher , description, id))
    conn.commit()
    conn.close()

def delete_course(id):
    conn = get_connection(config.DB_PATH_COURSES)
    cursor = conn.cursor()
    command="DELETE FROM courses WHERE id = ?"
    cursor.execute(command, (id))
    conn.commit()
    conn.close()
    return
