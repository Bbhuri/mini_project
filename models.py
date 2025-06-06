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


def create_student(student_id, student_name):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        command = "INSERT INTO students(student_id, student_name) VALUES (?, ?)"
        cursor.execute(command, (student_id, student_name, ))
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError("Student ID already exists")
    finally:
        conn.close()

def read_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            s.id,
            s.student_id,
            s.student_name,
            p.project_name
        FROM students s
        LEFT JOIN projects p ON s.project_id = p.id
    """)
    students = cursor.fetchall()
    conn.close()
    return students

def read_student_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    command="SELECT * FROM students WHERE id =?"
    cursor.execute(command, (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def update_student(id,student_id, student_name, ):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        command="UPDATE students SET student_id = ?, student_name = ? WHERE id = ?"
        cursor.execute(command, (student_id,student_name, id))
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

def create_project (project_id,project_name, branch_id,student_ids,description):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        command = "INSERT INTO projects (project_id,project_name,branch_id, description) VALUES (?,?,?,?)"
        cursor.execute(command, (project_id,project_name, branch_id,description,))
        conn.commit()

        project_id = cursor.lastrowid

        for student_id in student_ids:
            try:
                command = "INSERT INTO project_students (project_id, student_id) VALUES (?, ?)"
                cursor.execute(command, (project_id, student_id))
                conn.commit()
            except sqlite3.IntegrityError:
                conn.rollback()
                continue

    except sqlite3.IntegrityError:
        raise ValueError("Project ID already exists")
    finally:
        conn.close()

def read_projects():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            projects.id,
            projects.project_id,
            projects.project_name,
            branches.branch_name,
            GROUP_CONCAT(students.student_name, ', ') AS student_names,
            projects.description
        FROM projects
        LEFT JOIN project_students ON projects.id = project_students.project_id
        LEFT JOIN students ON project_students.student_id = students.id
        LEFT JOIN branches ON projects.branch_id = branches.id
        GROUP BY projects.id, projects.project_id, projects.project_name, branches.branch_name, projects.description
    """)
    projects = cursor.fetchall()
    conn.close()
    return projects

def update_project (project_id,project_name, branch_id,student_ids,description):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        command = "UPDATE projects SET project_name =?,branch_id=? description =? WHERE id =?"
        cursor.execute(command, (project_name, description,branch_id, project_id))
        conn.commit()

        for student_id in student_ids:
            try:
                command = "UPDATE project_students SET student_id =? WHERE project_id =?"
                cursor.execute(command, (student_id,project_id,))
                conn.commit()
            except sqlite3.IntegrityError:
                conn.rollback()
                continue

    except sqlite3.IntegrityError:
        raise ValueError("Project ID already exists")
    finally:
        conn.close()

def delete_project (project_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM project_students WHERE project_id = ?", (project_id,))
        cursor.execute("DELETE FROM projects WHERE id =?", (project_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
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