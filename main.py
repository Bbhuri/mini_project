from db import initializeCourses_db, initializeStudents_db,initializeEnrollments_db, initializeGrade_db,initializeAssessments_db
from gui import start_gui

if __name__ == "__main__":
    initializeStudents_db()
    initializeCourses_db()
    initializeEnrollments_db()
    initializeAssessments_db()
    initializeGrade_db()
    start_gui()
