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
    cursor.execute(command, (user_id,))
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
