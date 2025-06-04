import tkinter as tk
from tkinter import messagebox
from models import create_student, read_students,read_student_by_id, update_student, delete_student
from tkinter import ttk

def add_user(student_id_entry,name_entry, branch_entry):
    student_id = student_id_entry.get()
    student_name = name_entry.get()
    branch = branch_entry.get()
    if student_id and student_name and branch:
        try:
            create_student(student_id, student_name, branch)
        except Exception as e:
            messagebox.showerror("Error", str(e))

def load_students(table):
    for item in table.get_children():
        table.delete(item)
    students = read_students()
    for row in students:
        table.insert('', tk.END, values=row[1:],iid=row[0])

def open_add_user_modal(table,id):
    modal = tk.Toplevel()

    student_id_entry = tk.Entry(modal)
    name_entry = tk.Entry(modal)
    branch_entry = tk.Entry(modal)
    
    if id != 0:
        modal.title("แก้ไขผู้ใช้")
        student = read_student_by_id(id)
        if student: # Add a check if student is found
            student_id_entry.insert(0,student[1])
            name_entry.insert(0,student[2])
            branch_entry.insert(0,student[3])
        else:
             messagebox.showerror("Error", f"Student with ID {id} not found.")
             modal.destroy()
             return
    else:
        modal.title("เพิ่มผู้ใช้")

    modal.grab_set()
    modal.geometry("300x200")

    tk.Label(modal, text="รหัสนักศึกษา").grid(row=0, column=0, padx=10, pady=5, sticky='e')
    student_id_entry.grid(row=0, column=1, pady=5)

    tk.Label(modal, text="ชื่อ").grid(row=1, column=0, padx=10, pady=5, sticky='e')
    name_entry.grid(row=1, column=1, pady=5)

    tk.Label(modal, text="สาขา").grid(row=2, column=0, padx=10, pady=5, sticky='e')
    branch_entry.grid(row=2, column=1, pady=5)

    def on_save():
        student_id_str = student_id_entry.get()
        student_name = name_entry.get()
        branch = branch_entry.get()
        if student_id_str and student_name and branch:
            try:
                student_id = int(student_id_str)
                if id != 0:
                    update_student(id, student_id, student_name, branch)
                else:
                    create_student(student_id, student_name, branch)
                load_students(table)
                if id != 0:
                    messagebox.showinfo("Success", f"อัปเดตข้อมูลนักศึกษา รหัส {student_id} สำเร็จ!")
                else:
                    messagebox.showinfo("Success", "เพิ่มนักศึกษาสำเร็จ!")
                modal.destroy()
            except ValueError:
                messagebox.showerror("Error", "รหัสนักศึกษาต้องเป็นตัวเลขเท่านั้น")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    def on_cancel():
        modal.destroy()

    button_frame = tk.Frame(modal)
    button_frame.grid(row=3, columnspan=2, pady=10)

    tk.Button(button_frame, text="บันทึก", command=on_save, width=10).pack(side="left", padx=5)
    tk.Button(button_frame, text="ยกเลิก", command=on_cancel, width=10).pack(side="left", padx=5)

def edit_selected_student(table):
    selected_item = table.selection()
    if not selected_item:
        messagebox.showwarning("ไม่พบรายการ", "กรุณาเลือกนักศึกษาที่ต้องการแก้ไข")
        return
    student_id = selected_item[0]
    if selected_item:
        open_add_user_modal(table, student_id)


def delete_selected_student(table):
    selected_item = table.selection()
    if not selected_item:
        messagebox.showwarning("ไม่พบรายการ", "กรุณาเลือกผู้ใช้ที่ต้องการลบ")
        return
    student_id = selected_item[0]
    confirm = messagebox.askyesno("ยืนยันการลบ", "ยืนยันการลบใช่หรือไม่?")
    if confirm:
        delete_student(student_id)
        table.delete(student_id)

def start_gui():
    root = tk.Tk()
    root.title("Students Manager")

    columns = ("รหัสนักศึกษา", "ชื่อ", "สาขา")
    table = ttk.Treeview(root, columns=columns, show='headings')

    for col in columns:
        table.heading(col, text=col)
        table.column(col, anchor="center")

    table.pack(expand=True, fill='both')

    def on_row_select(event):
        item_id = table.identify_row(event.y)
        if item_id:
            table.focus(item_id)
            table.selection_set(item_id)

    table.bind('<ButtonRelease-1>', on_row_select)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    edit_button = tk.Button(button_frame, text="แก้ไขผู้ใช้", command=lambda: edit_selected_student(table))
    edit_button.pack(side="left", padx=5)

    delete_button = tk.Button(button_frame, text="ลบผู้ใช้", command=lambda: delete_selected_student(table))
    delete_button.pack(side="left", padx=5)

    add_user_button = tk.Button(root, text="เพิ่มผู้ใช้", command=lambda: open_add_user_modal(table,0))
    add_user_button.pack(pady=10)

    # Load data
    load_students(table)

    root.mainloop()
