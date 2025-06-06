import tkinter as tk
from tkinter import messagebox, ttk
from models import (
    create_branch, read_branches, update_branch, delete_branch, read_branch_by_id,
    create_project, read_projects, update_project, delete_project, read_project_by_id,
    create_student, read_students, update_student, delete_student, read_student_by_id,search_projects
)

def create_table_frame(root, title_text):
    frame = tk.Frame(root)
    tk.Label(frame, text=title_text, font=('Angsana New', 30, 'bold')).pack(pady=10)
    table = ttk.Treeview(frame, show='headings')
    table.pack(expand=True, fill='both', padx=10, pady=10)
    return frame, table

def load_data(table, reader):
    table.delete(*table.get_children())
    for row in reader():
        table.insert('', tk.END, values=row[1:], iid=row[0])

def open_modal(table, entity_name, field_names, entry_getters, reader_by_id, updater, creator, loader, entity_id=0):
    modal = tk.Toplevel()
    modal.title(f"แก้ไข{entity_name}" if entity_id else f"เพิ่ม{entity_name}")
    modal.geometry("400x300")
    modal.grab_set()

    entries = []
    branch_dropdown_index = None
    student_dropdown_index = None
    branch_id_map = {}
    student_id_map = {}


    for i,field in  enumerate(field_names):
        handled = False
        
        if entity_name == "โครงงาน"  and field == "สาขา":
            branch_dropdown_index = i
            branches = read_branches()
            branch_id_map = {branch_name:id for id, _  , branch_name, *_ in branches}
            combo = ttk.Combobox(modal, values=list(branch_id_map.keys()), state="readonly")
            entries.append(combo)
            handled = True

        if entity_name == "โครงงาน" and field == "ผู้จัดทำ":
            student_dropdown_index = i
            students = read_students()
            student_id_map = {student_name: id for id, _, student_name, *_ in students}

            listbox = tk.Listbox(modal, selectmode="multiple", exportselection=False, height=6)

            for name in student_id_map.keys():
                listbox.insert(tk.END, name)

            listbox.grid(row=i, column=1, sticky="ew")  # Adjust grid placement as needed
            entries.append(listbox)
            handled = True

        if not handled:
            entries.append(tk.Entry(modal))

    if entity_id:
        data = reader_by_id(entity_id)
        if data:
            for i, entry in enumerate(entries):
                value = data[i + 1]  # Skip ID

                if i == branch_dropdown_index:
                    name = next((n for n, bid in branch_id_map.items() if bid == value), "")
                    entry.set(value)
                elif i == student_dropdown_index:
                    student_names = value.split(", ")  # value is a comma-separated string of names
                    all_names = entry.get(0, tk.END)
                    for idx, name in enumerate(all_names):
                            if name in student_names:
                                entry.selection_set(idx)
                else:
                    entry.delete(0, tk.END)
                    entry.insert(0, value)
        else:
            messagebox.showerror("Error", f"{entity_name} ID {entity_id} not found")
            modal.destroy()
            return

    for i, (label, entry) in enumerate(zip(field_names, entries)):
        tk.Label(modal, text=label).grid(row=i, column=0, padx=10, pady=5, sticky='e')
        entry.grid(row=i, column=1, pady=5)

    def on_save():
        try:
            values = []
            for i, (getter, widget) in enumerate(zip(entry_getters, entries)):
                if i == branch_dropdown_index:
                    selected_name = widget.get()
                    if not selected_name:
                        raise ValueError("กรุณาเลือกสาขา")
                    values.append(branch_id_map[selected_name])
                elif i == student_dropdown_index:
                    selected_indices = widget.curselection()
                    if not selected_indices:
                        raise ValueError("กรุณาเลือกผู้จัดทำ")
                    selected_students = [student_id_map[widget.get(idx)] for idx in selected_indices]
                    values.append(selected_students)
                else:
                    values.append(getter(widget.get()))
            if not all(values):
                raise ValueError("กรุณากรอกข้อมูลให้ครบถ้วน")

            if entity_id:
                updater(entity_id, *values)
            else:
                creator(*values)
            loader(table)
            messagebox.showinfo("Success", "บันทึกข้อมูลสำเร็จ!")
            modal.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            print(e)
            messagebox.showerror("Error", f"เกิดข้อผิดพลาด: {str(e)}")
            modal.destroy()

    tk.Button(modal, text="บันทึก", command=on_save, width=10).grid(row=len(field_names), column=0, pady=10)
    tk.Button(modal, text="ยกเลิก", command=modal.destroy, width=10).grid(row=len(field_names), column=1)

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

    # Main notebook
    main_notebook = ttk.Notebook(root)
    main_notebook.pack(fill='both', expand=True)

    # ------------------- Search Tab (Default) -------------------
    search_frame = tk.Frame(main_notebook)
    ttk.Label(search_frame, text="หน้าค้นหาข้อมูลโครงงาน", font=("TH Sarabun New", 16)).pack(pady=20)
    main_notebook.add(search_frame, text="ค้นหา")

    search_input = tk.Entry(search_frame, font=("TH Sarabun New", 14))
    search_input.pack(pady=10)
    search_button = tk.Button(search_frame, text="ค้นหา", font=("TH Sarabun New", 14))
    search_button.pack()

    table_frame = tk.Frame(search_frame)
    table_frame.pack(pady=10)

    table = ttk.Treeview(table_frame, show='headings')
    table['columns'] = ("รหัสโครงงาน", "ชื่อโครงงาน", "สาขา", "ผู้จัดทำ", "หมายเหตุ")
    for col in table['columns']:
        table.heading(col, text=col)
        table.column(col, anchor='center')
    table.pack(side='left', expand=True, fill='both', padx=10, pady=10)

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
    table.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side='right', fill='y')

    def on_search():
        term = search_input.get()
        if term.strip() == "":
            results = read_projects()
        else:
            results = search_projects(term)
        
        table.delete(*table.get_children())  # Clear table
        for project in results:
            table.insert("", "end", values=(
                project[1],  # project_id
                project[2],  # project_name
                project[3],  # branch_name
                project[4],  # student_names
                project[5],  # description
            ))

    search_button.config(command=on_search)
    search_input.bind("<Return>", lambda event: on_search())

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
    table.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side='right', fill='y')

    load_data(table, read_projects)
    

    # ------------------- Management Tab -------------------
    management_frame = tk.Frame(main_notebook)
    management_notebook = ttk.Notebook(management_frame)
    management_notebook.pack(fill='both', expand=True)



    # ---------- Branch Tab ----------
    branch_frame, branch_table = create_table_frame(management_notebook, 'ตารางสาขา')
    branch_table['columns'] = ("รหัสสาขา", "ชื่อสาขา", "หมายเหตุ")
    for col in branch_table['columns']:
        branch_table.heading(col, text=col)
        branch_table.column(col, anchor='center')
    build_crud_buttons(
        branch_frame,
        lambda: open_modal(branch_table, "สาขา", ["รหัสสาขา", "ชื่อสาขา", "หมายเหตุ"], [str, str, str],
                           read_branch_by_id, update_branch, create_branch,
                           lambda table: load_data(table, read_branches)),
        lambda: open_modal(branch_table, "สาขา", ["รหัสสาขา", "ชื่อสาขา", "หมายเหตุ"], [str, str, str],
                           read_branch_by_id, update_branch, create_branch, 
                           lambda table: load_data(table, read_branches), int(branch_table.selection()[0]))
            if branch_table.selection() else None,
        lambda: delete_selected(branch_table, delete_branch)
    )
    load_data(branch_table, read_branches)
    management_notebook.add(branch_frame, text="สาขา")


# ---------- Student Tab ----------
    student_frame, student_table = create_table_frame(management_notebook, 'ตารางนักศึกษา')
    student_table['columns'] = ("รหัสนักศึกษา", "ชื่อ", "โครงงาน")
    for col in student_table['columns']:
        student_table.heading(col, text=col)
        student_table.column(col, anchor='center')
    build_crud_buttons(
        student_frame,
        lambda: open_modal(student_table, "นักศึกษา", ["รหัสนักศึกษา", "ชื่อ"], [int, str ],
                           read_student_by_id, update_student, create_student,
                           lambda table: load_data(table, read_students)),
        lambda: open_modal(student_table, "นักศึกษา", ["รหัสนักศึกษา", "ชื่อ"], [int, str],
                           read_student_by_id, update_student, create_student,
                           lambda table: load_data(table, read_students), int(student_table.selection()[0]))
            if student_table.selection() else None,
        lambda: delete_selected(student_table, delete_student)
    )
    load_data(student_table, read_students)
    management_notebook.add(student_frame, text="นักศึกษา")

    # ---------- Project Tab ----------
    project_frame, project_table = create_table_frame(management_notebook, 'ตารางโครงงาน')
    project_table['columns'] = ("รหัสโครงงาน", "ชื่อโครงงาน", "สาขา","ผู้จัดทำ","หมายเหตุ")
    for col in project_table['columns']:
        project_table.heading(col, text=col)
        project_table.column(col, anchor='center')
    build_crud_buttons(
        project_frame,
        lambda: open_modal(project_table, "โครงงาน", ["รหัสโครงงาน", "ชื่อโครงงาน", "สาขา","ผู้จัดทำ","หมายเหตุ"], [str, str, str,str,str],
                           read_project_by_id, update_project, create_project, 
                           lambda table: load_data(table, read_projects)),
        lambda: open_modal(project_table, "โครงงาน", ["รหัสโครงงาน", "ชื่อโครงงาน", "สาขา", "ผู้จัดทำ","หมายเหตุ"], [str, str,str,str,str],
                           read_project_by_id, update_project, create_project, 
                           lambda table: load_data(table, read_projects), int(project_table.selection()[0]))
            if project_table.selection() else None,
        lambda: delete_selected(project_table, delete_project)
    )
    load_data(project_table, read_projects)
    management_notebook.add(project_frame, text="โครงงาน")

    main_notebook.add(management_frame, text="การจัดการ")

    # Set Search as the default tab (index 0)
    main_notebook.select(0)

    root.mainloop()
