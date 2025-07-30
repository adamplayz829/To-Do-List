import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import simpledialog, messagebox

# Create main window with modern theme
root = tb.Window(themename="superhero")
root.title("To Do List")
root.geometry("600x700")

# Instead of setting background=bluer_indigo, use:
bg_color = root.cget("background")

title_label = tb.Label(root, text="To Do List", font=("Arial", 40, "bold"),
                       bootstyle="light", background=bg_color, foreground="white")
title_label.pack(pady=(10, 5))

counter_label = tb.Label(root, text="0/0", font=("Arial", 16),
                         bootstyle="light", background=bg_color, foreground="white")
counter_label.pack(pady=(10, 5))


# List of tasks and stats
tasks = []
checkbox_vars = []
task_widgets = []
completed_count = 0
total_tasks_created = 0

# Frame to hold task list
task_container = tb.Frame(root, padding=10)
task_container.pack(fill=BOTH, expand=YES, pady=10)

canvas = tb.Canvas(task_container, bg="white", highlightthickness=0)
canvas.pack(side=LEFT, fill=BOTH, expand=True)

scrollbar = tb.Scrollbar(task_container, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)
canvas.configure(yscrollcommand=scrollbar.set)

task_frame = tb.Frame(canvas, padding=5)
canvas.create_window((0, 0), window=task_frame, anchor="nw")

def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
task_frame.bind("<Configure>", on_frame_configure)

# Core functions
def update_counter():
    counter_label.config(text=f"{completed_count}/{total_tasks_created}")

def save_tasks():
    with open("tasks.txt", "w") as f:
        for task in tasks:
            f.write(task + "\n")
    with open("counter.txt", "w") as f:
        f.write(f"{completed_count},{total_tasks_created}")



def load_tasks():
    try:
        with open("tasks.txt", "r") as f:
            for line in f:
                task = line.strip()
                if task:
                    tasks.append(task)
    except FileNotFoundError:
        pass

    global completed_count, total_tasks_created
    try:
        with open("counter.txt", "r") as f:
            counts = f.read().strip().split(",")
            completed_count = int(counts[0])
            total_tasks_created = int(counts[1])
    except (FileNotFoundError, IndexError, ValueError):
        completed_count = 0
        total_tasks_created = len(tasks)

    update_counter()

def auto_delete_task(index):
    global completed_count
    completed_count += 1
    tasks.pop(index)
    update_listbox()
    update_counter()
    save_tasks()

def update_listbox():
    for widget in task_frame.winfo_children():
        widget.destroy()
    checkbox_vars.clear()
    task_widgets.clear()

    for index, task_text in enumerate(tasks):
        var = tb.BooleanVar()
        row = tb.Frame(task_frame, padding=5)
        row.pack(fill=X, pady=3)

        cb = tb.Checkbutton(row, text=task_text, variable=var, bootstyle="success",
                            command=lambda i=index: auto_delete_task(i))
        cb.pack(side=LEFT, fill=X, expand=True)
        checkbox_vars.append(var)

        dot_btn = tb.Button(row, text="⋮", bootstyle="secondary-outline", width=2,
                            command=lambda i=index: show_popup(i))
        dot_btn.pack(side=RIGHT)

def add_task():
    task = simpledialog.askstring("Add Task", "Enter your task:")
    if task is None or task.strip() == "":
        messagebox.showerror("Error", "Task cannot be empty.")
        return
    tasks.append(task.strip())
    global total_tasks_created
    total_tasks_created += 1
    update_listbox()
    update_counter()
    save_tasks()

def deletetask(index=None):
    if index is None:
        try:
            index = next(i for i, v in enumerate(checkbox_vars) if v.get())
        except StopIteration:
            messagebox.showwarning("Warning", "Select a task to delete.")
            return
    tasks.pop(index)
    update_listbox()
    update_counter()
    save_tasks()

def edit_task(index=None):
    if index is None:
        try:
            index = next(i for i, v in enumerate(checkbox_vars) if v.get())
        except StopIteration:
            messagebox.showwarning("Warning", "Select a task to edit.")
            return
    current = tasks[index]
    new = simpledialog.askstring("Edit Task", "Edit your task:", initialvalue=current)
    if new is None or new.strip() == "":
        messagebox.showerror("Error", "Task cannot be empty.")
    else:
        tasks[index] = new.strip()
        update_listbox()
        save_tasks()

def reset_counters():
    global completed_count, total_tasks_created, tasks
    completed_count = 0
    total_tasks_created = 0
    tasks.clear()
    update_listbox()
    update_counter()
    save_tasks()

def show_popup(index):
    popup = tb.Toplevel(root)
    popup.overrideredirect(True)
    popup.geometry(f"100x70+{root.winfo_pointerx()}+{root.winfo_pointery()}")

    tb.Button(popup, text="Edit", command=lambda: [edit_task(index), popup.destroy()]).pack(pady=2)
    tb.Button(popup, text="Delete", command=lambda: [deletetask(index), popup.destroy()]).pack(pady=2)

    def close_popup(e): popup.destroy()
    popup.bind("<FocusOut>", close_popup)
    popup.focus_set()

# Buttons at bottom
btn_frame = tb.Frame(root)
btn_frame.pack(pady=10)

tb.Button(btn_frame, text="Add Task", command=add_task, bootstyle="primary").pack(side=LEFT, padx=10)
tb.Button(btn_frame, text="Reset Counter", command=reset_counters, bootstyle="danger").pack(side=LEFT, padx=10)

# Run
load_tasks()
update_listbox()
root.mainloop()
