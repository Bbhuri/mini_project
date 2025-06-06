import csv
import os
import random
import string

# Helper functions
def rand_id(prefix, num):
    return f"{prefix}{num:03}"

def random_name():
    return ''.join(random.choices(string.ascii_uppercase, k=1)) + ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 7)))

# Generate 5 branches
branches = []
for i in range(5):
    bid = rand_id("B", i+1)
    branches.append({
        "branch_id": bid,
        "branch_name": f"Branch_{i+1}",
        "description": f"Description for Branch {i+1}"
    })

# Generate 20 projects
projects = []
for i in range(20):
    pid = rand_id("P", i+1)
    branch = random.choice(branches)["branch_id"]
    projects.append({
        "project_id": pid,
        "project_name": f"Project_{i+1}",
        "branch_id": branch,
        "description": f"Description for Project {i+1}"
    })

# Generate 10 students
students = []
assigned_projects = random.sample(projects, k=10)  # Ensure unique project assignments
for i in range(10):
    sid = rand_id("S", i+1)
    project_id = assigned_projects[i]["project_id"]
    students.append({
        "student_id": sid,
        "student_name": random_name(),
        "project_id": project_id
    })

# Generate project_students table (1:1 mapping here, same as students)
project_students = [{"project_id": s["project_id"], "student_id": s["student_id"]} for s in students]

# Write CSVs
os.makedirs("generated_csv", exist_ok=True)

def write_csv(filename, data, fieldnames):
    with open(os.path.join("generated_csv", filename), "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

write_csv("branches.csv", branches, ["branch_id", "branch_name", "description"])
write_csv("projects.csv", projects, ["project_id", "project_name", "branch_id", "description"])
write_csv("students.csv", students, ["student_id", "student_name", "project_id"])
write_csv("project_students.csv", project_students, ["project_id", "student_id"])
