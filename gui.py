import tkinter as tk
from tkinter import messagebox, ttk
from models import (
    create_student, read_students, read_student_by_id, update_student, delete_student,
    create_course,read_courses, read_course_by_id, update_course, delete_course
)

def create_table_frame(root, title_text):
    frame = tk.Frame(root)
    tk.Label(frame, text=title_text, font=('Angsana New', 30, 'bold')).pack(pady=10)
    table = ttk.Treeview(frame, show='headings')
    table.pack(expand=True, fill='both', padx=10, pady=10)
    return frame, table

def load_students(table):
    table.delete(*table.get_children())
    students = read_students()
    for row in students:
        table.insert('', tk.END, values=row[1:], iid=row[0])

def load_courses(table):
    table.delete(*table.get_children())
    courses = read_courses()
    for row in courses:
        table.insert('', tk.END, values=row[1:], iid=row[0])

def open_student_modal(table, student_id=0):
    modal = tk.Toplevel()
    modal.title("แก้ไขผู้ใช้" if student_id else "เพิ่มผู้ใช้")
    modal.geometry("300x200")
    modal.grab_set()

    sid_entry = tk.Entry(modal)
    name_entry = tk.Entry(modal)
    branch_entry = tk.Entry(modal)

    if student_id:
        student = read_student_by_id(student_id)
        if student:
            sid_entry.insert(0, student[1])
            name_entry.insert(0, student[2])
            branch_entry.insert(0, student[3])
        else:
            messagebox.showerror("Error", f"Student ID {student_id} not found")
            modal.destroy()
            return

    labels = ["รหัสนักศึกษา", "ชื่อ", "สาขา"]
    entries = [sid_entry, name_entry, branch_entry]
    for i, (label, entry) in enumerate(zip(labels, entries)):
        tk.Label(modal, text=label).grid(row=i, column=0, padx=10, pady=5, sticky='e')
        entry.grid(row=i, column=1, pady=5)

    def on_save():
        try:
            sid = int(sid_entry.get())
            name = name_entry.get()
            branch = branch_entry.get()
            if not all([sid, name, branch]):
                raise ValueError("กรุณากรอกข้อมูลให้ครบทุกช่อง")
            if student_id:
                update_student(student_id, sid, name, branch)
            else:
                create_student(sid, name, branch)
            load_students(table)
            messagebox.showinfo("Success", "บันทึกข้อมูลสำเร็จ!")
            modal.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"เกิดข้อผิดพลาด: {str(e)}")
            modal.destroy()

    tk.Button(modal, text="บันทึก", command=on_save, width=10).grid(row=3, column=0, pady=10)
    tk.Button(modal, text="ยกเลิก", command=lambda: [modal.destroy(), table.focus_remove()], width=10).grid(row=3, column=1)

def open_course_modal(table, course_id=0):
    modal = tk.Toplevel()
    modal.title("แก้ไขวิชา" if course_id else "เพิ่มวิชา")
    modal.geometry("350x250")
    modal.grab_set()

    course_id_entry = tk.Entry(modal)
    course_name_entry = tk.Entry(modal)
    teacher_entry = tk.Entry(modal)
    description_entry = tk.Entry(modal)

    if course_id:
        course = read_course_by_id(course_id)
        if course:
            course_id_entry.insert(0, course[1])
            course_name_entry.insert(0, course[2])
            teacher_entry.insert(0, course[3])
            description_entry.insert(0, course[4])
        else:
            messagebox.showerror("Error", f"Course ID {course_id} not found")
            modal.destroy()
            return

    labels = ["รหัสวิชา", "ชื่อวิชา", "อาจารย์ผู้สอน", "หมายเหตุ"]
    entries = [course_id_entry, course_name_entry, teacher_entry, description_entry]
    for i, (label, entry) in enumerate(zip(labels, entries)):
        tk.Label(modal, text=label).grid(row=i, column=0, padx=10, pady=5, sticky='e')
        entry.grid(row=i, column=1, pady=5)

    def on_save():
        try:
            cid = course_id_entry.get()
            cname = course_name_entry.get()
            teacher = teacher_entry.get()
            desc = description_entry.get()
            if not all([cid, cname, teacher]):
                raise ValueError("กรุณากรอกข้อมูล รหัสวิชา, ชื่อวิชา, และอาจารย์ผู้สอน ให้ครบ")
            if course_id:
                update_course(course_id, cid, cname, teacher, desc)
            else:
                create_course(cid, cname, teacher, desc)
            load_courses(table)
            messagebox.showinfo("Success", "บันทึกข้อมูลสำเร็จ!")
            modal.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"เกิดข้อผิดพลาด: {str(e)}")
            modal.destroy()

    tk.Button(modal, text="บันทึก", command=on_save, width=10).grid(row=4, column=0, pady=10)
    tk.Button(modal, text="ยกเลิก", command=lambda: [modal.destroy(), table.focus_remove()], width=10).grid(row=4, column=1)


def delete_selected(table, delete_fn):
    selected = table.selection()
    if not selected:
        messagebox.showwarning("ไม่พบรายการ", "กรุณาเลือกรายการ")
        return
    if messagebox.askyesno("ยืนยัน", "คุณต้องการลบข้อมูลนี้ใช่หรือไม่?"):
        delete_fn(selected[0])
        table.delete(selected[0])

def build_crud_buttons(frame, add_fn, edit_fn, delete_fn):
    btn_frame = tk.Frame(frame)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="เพิ่ม", width=10, command=add_fn).pack(side='left', padx=5)
    tk.Button(btn_frame, text="แก้ไข", width=10, command=edit_fn).pack(side='left', padx=5)
    tk.Button(btn_frame, text="ลบ", width=10, command=delete_fn).pack(side='left', padx=5)

def start_gui():
    root = tk.Tk()
    root.title("Class Manager")
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)

    # Student Tab
    student_frame, student_table = create_table_frame(root, 'ตารางรายชื่อนักศึกษา')
    student_table['columns'] = ("รหัสนักศึกษา", "ชื่อ", "สาขา")
    for col in student_table['columns']:
        student_table.heading(col, text=col)
        student_table.column(col, anchor='center')

    build_crud_buttons(
        student_frame,
        lambda: open_student_modal(student_table),
        lambda: open_student_modal(student_table, int(student_table.selection()[0])) if student_table.selection() else None,
        lambda: delete_selected(student_table, delete_student)
    )
    load_students(student_table)
    notebook.add(student_frame, text="นักศึกษา")

    # Course Tab
    course_frame, course_table = create_table_frame(root, 'ตารางรายวิชา')
    course_table['columns'] = ("รหัสวิชา", "ชื่อวิชา", "อาจารย์ผู้สอน", "หมายเหตุ")
    for col in course_table['columns']:
        course_table.heading(col, text=col)
        course_table.column(col, anchor='center')
    build_crud_buttons(
        course_frame,
        lambda: open_course_modal(course_table),
        lambda: open_course_modal(course_table, int(course_table.selection()[0])) if course_table.selection() else None,
        lambda: delete_selected(course_table, delete_course)
    )
    load_courses(course_table)
    notebook.add(course_frame, text="วิชา")

    # Grade Tab (placeholder)
    grade_frame = tk.Frame(root)
    tk.Label(grade_frame, text="ตารางเกรด", font=('Angsana New', 30, 'bold')).pack(pady=10)
    notebook.add(grade_frame, text="เกรด")

    root.mainloop()
