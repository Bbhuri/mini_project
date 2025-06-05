from db import get_connection
import config
import os
import sqlite3

def create_branch(branch_id, branch_name, description):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        command = "INSERT INTO branches(branch_id, branch_name, description) VALUES (?, ?, ?)"
        cursor.execute(command, (branch_id, branch_name, description))
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError("Branch ID already exists")
    finally:
        conn.close()

def read_branches():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM branches")
    branches = cursor.fetchall()
    conn.close()
    return branches

def read_branch_by_id(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM branches WHERE id = ?", (id,))
    branch = cursor.fetchone()
    conn.close()
    return branch

def update_branch(id, branch_id, branch_name, description):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        command = "UPDATE branches SET branch_id = ?, branch_name = ?, description = ? WHERE id = ?"
        cursor.execute(command, (branch_id, branch_name, description, id))
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError("Branch ID already exists")
    finally:
        conn.close()

def delete_branch(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM branches WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return


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





def create_project (project_name, description):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        command = "INSERT INTO projects (project_name, description) VALUES (?,?)"
        cursor.execute(command, (project_name, description))
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError("Project ID already exists")
    finally:
        conn.close()

def read_projects():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects")
    projects = cursor.fetchall()
    conn.close()
    return projects

def update_project (project_id, project_name, description):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        command = "UPDATE projects SET project_name =?, description =? WHERE id =?"
        cursor.execute(command, (project_name, description, project_id))
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError("Project ID already exists")
    finally:
        conn.close()

def delete_project (project_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM projects WHERE id =?", (project_id,))
    conn.commit()
    conn.close()
    return

def read_project_by_id(project_id):
    conn = get_connection()
    cursor = conn.cursor()
    command="SELECT * FROM projects WHERE id =?"
    cursor.execute(command, (project_id,))
    project = cursor.fetchone()
    conn.close()
    return project