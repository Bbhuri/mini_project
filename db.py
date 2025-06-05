import sqlite3
import os
import config

def get_connection():
    return sqlite3.connect(config.DB_PATH)

def initializeBranch_db():
    os.makedirs("data", exist_ok=True)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS branches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        branch_id TEXT NOT NULL UNIQUE,
        branch_name TEXT NOT NULL,
        description TEXT
        )""")
    conn.commit()
    conn.close()

def initializeProject_db():
    os.makedirs("data", exist_ok=True)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_name TEXT NOT NULL,
        branch_id TEXT,
        description TEXT,
        FOREIGN KEY(branch_id) REFERENCES branches(branch_id)
        )""")
    conn.commit()
    conn.close()

def initializeStudents_db():
    os.makedirs("data", exist_ok=True)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT NOT NULL UNIQUE,
        student_name TEXT NOT NULL, 
        project_id TEXT,
        Foreign Key(project_id) REFERENCES projects(project_id)
        )""")
    conn.commit()
    conn.close()