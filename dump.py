import sqlite3
import csv
import config  # your DB_PATH lives here

def import_csv_to_sqlite(csv_file, table_name, columns):
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()

    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = [tuple(row[col] for col in columns) for row in reader]

    placeholders = ','.join(['?'] * len(columns))
    sql = f'INSERT INTO {table_name} ({",".join(columns)}) VALUES ({placeholders})'
    cursor.executemany(sql, rows)

    conn.commit()
    conn.close()

# Example usage for each table
import_csv_to_sqlite("generated_csv/branches.csv", "branches", ["branch_id", "branch_name", "description"])
import_csv_to_sqlite("generated_csv/projects.csv", "projects", ["project_id", "project_name", "branch_id", "description"])
import_csv_to_sqlite("generated_csv/students.csv", "students", ["student_id", "student_name", "project_id"])
import_csv_to_sqlite("generated_csv/project_students.csv", "project_students", ["project_id", "student_id"])
