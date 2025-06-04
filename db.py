import sqlite3
import os
import config

def get_connection():
    return sqlite3.connect(config.DB_PATH)

def initializeStudents_db():
    os.makedirs("data", exist_ok=True)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT NOT NULL UNIQUE,
        student_name TEXT NOT NULL, 
        branch TEXT NOT NULL
        )""")
    conn.commit()
    conn.close()

def initializeCourses_db():
    os.makedirs("data", exist_ok=True)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id TEXT NOT NULL UNIQUE,
        course_name TEXT NOT NULL,
        teacher TEXT,
        description TEXT
        )""")
    conn.commit()
    conn.close()

def initializeEnrollments_db():
    os.makedirs("data", exist_ok=True)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS enrollments (
        student_id INTEGER,
        course_id INTEGER,
        FOREIGN KEY(student_id) REFERENCES students(id),
        FOREIGN KEY(course_id) REFERENCES courses(id),
        PRIMARY KEY (student_id, course_id)
        )""")
    conn.commit()
    conn.close()

def initializeAssessments_db():
    os.makedirs("data", exist_ok=True)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS assessments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        course_id INTEGER,
        max_score REAL,
        FOREIGN KEY(course_id) REFERENCES courses(id)
        )""")
    conn.commit()
    conn.close()

def initializeGrade_db():
    os.makedirs("data", exist_ok=True)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS grade (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        assessment_id INTEGER,
        score REAL,
        FOREIGN KEY(student_id) REFERENCES students(id),
        FOREIGN KEY(assessment_id) REFERENCES assessments(id)
        )""")
    conn.commit()
    conn.close()