from db import  initializeStudents_db,initializeBranch_db,initializeProject_db
from gui import start_gui

if __name__ == "__main__":
    initializeBranch_db()
    initializeProject_db()
    initializeStudents_db()
    start_gui()
