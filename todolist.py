import tkinter as tk
from tkinter import simpledialog, messagebox

# Create main window
root = tk.Tk()
root.title("Indigo Background Example")

# Set window background color to indigo
bluer_indigo = "#3A00A0"
root.configure(bg=bluer_indigo)

# Set the title of the window
root.title("To Do List")

# Set the window size
root.geometry("600x700")

# Create title label
title_label = tk.Label(root, text="To Do List", font=("Arial", 40, "bold"),
                       bg=bluer_indigo, fg="white")

# Place it at the top and center
title_label.pack(side="top", pady=5)  # top with some padding

# Label to show completed / total tasks
counter_label = tk.Label(root, text="0/0", font=("Arial", 16), bg=bluer_indigo, fg="white")
counter_label.pack()

# list of tasks
tasks = []

# number of completed tasks
completed_count = 0

# total tasks created
total_tasks_created  = 0

# Frame for Listbox and Scrollbar
task_container = tk.Frame(root, bg=bluer_indigo)
task_container.pack(pady=10, fill="both", expand=True)

# Scrollable canvas
canvas = tk.Canvas(task_container, bg=bluer_indigo, highlightthickness=0)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(task_container, orient="vertical", command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.configure(yscrollcommand=scrollbar.set)

# Inner frame for tasks
task_frame = tk.Frame(canvas, bg=bluer_indigo)
canvas.create_window((0, 0), window=task_frame, anchor="nw")

# Adjust scrollregion dynamically
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
task_frame.bind("<Configure>", on_frame_configure)

# Store references to task widgets
checkbox_vars = []
task_widgets = []

# function that runs when button is clicked add task
def addtask():
    # Asks user for input using dialog
    task = simpledialog.askstring("Add Task", "Enter your task:")

    # checks input
    if task is None or task == "":
        messagebox.showerror("Error", "Task connot be empty.")
    else:
        #Add task to tasks list and update Listbox
        tasks.append(task.strip())
        global total_tasks_created
        total_tasks_created += 1
        save_tasks()
        update_listbox()
        update_counter()

# Create a addtask button
my_button = tk.Button(root, text="Add task", command=addtask)

# show the button on the window
my_button.pack(side="bottom", pady=20)

# update listbox (task panel)
def update_listbox():
    # clear listbox
    for widget in task_frame.winfo_children():
        widget.destroy()
    checkbox_vars.clear()
    task_widgets.clear()

    for index, task_text in enumerate(tasks):
        var = tk.BooleanVar()
        row = tk.Frame(task_frame, bg="#E6E6FA", pady=2)
        row.pack(fill="x", padx=10, pady=4)

        cb = tk.Checkbutton(row, text=task_text, variable=var, font=("Arial", 12),
                            bg="#E6E6FA", command=lambda i=index: auto_delete_task(i))
        cb.pack(side="left", anchor="w", padx=5)
        checkbox_vars.append(var)

        dot_button = tk.Button(row, text="⋮", font=("Arial", 12), bg="#E6E6FA", relief="flat",
                               command=lambda i=index: show_popup(i))
        dot_button.pack(side="right", padx=5)
        dot_button.place_forget()

        def on_enter(e, btn=dot_button): btn.place(relx=1.0, rely=0.5, anchor="e")
        def on_leave(e, btn=dot_button): btn.place_forget()

        row.bind("<Enter>", on_enter)
        row.bind("<Leave>", on_leave)
        cb.bind("<Enter>", on_enter)
        cb.bind("<Leave>", on_leave)

        task_widgets.append(row)

# Function to delete task
def deletetask(index=None):
    if index is None:
        try:
            index = next(i for i, v in enumerate(checkbox_vars) if v.get())
        except StopIteration:
            messagebox.showwarning("Warning", "PLease select a task to delete.")
            return

    tasks.pop(index)
    update_listbox()
    update_counter()
    save_tasks()

# save tasks to a file
def save_tasks():
    with open("tasls.txt", "w") as f:
        for task in tasks:
            f.write(task + "\n")

# function to edit task
def edit_task(index=None):
    if index is None:
        try:
            index = next(i for i, v in enumerate(checkbox_vars) if v.get())
        except StopIteration:
            messagebox.showwarning("Warning", "Please select a task to edit.")
            return

    current_task = tasks[index]
    new_task = simpledialog.askstring("Edit Task", "Edit your task:", initialvalue=current_task)

    if new_task is None or new_task.strip() == "":
        messagebox.showerror("Error", "Task cannot be empty.")
    else:
        tasks[index] = new_task.strip()
        update_listbox()
        save_tasks()

# auto-delete when checkbox checked
def auto_delete_task(index):
    global completed_count
    completed_count += 1  # Count as completed
    update_counter()
    tasks.pop(index)
    update_listbox()
    save_tasks()

# Reset counter function
def reset_counters():
    global completed_count, total_tasks_created
    completed_count = 0
    total_tasks_created = len(tasks)
    update_counter()

# Reset counter button
reset_button = tk.Button(root, text="Reset Counter", command=reset_counters)
reset_button.pack(side="bottom", pady=5)


# hover 3-dot menu handler
def show_popup(index):
    popup = tk.Toplevel(root)
    popup.overrideredirect(True)
    popup.geometry(f"100x70+{root.winfo_pointerx()}+{root.winfo_pointery()}")

    edit_btn = tk.Button(popup, text="Edit", width=10, command=lambda: [edit_task(index), popup.destroy()])
    delete_btn = tk.Button(popup, text="Delete", width=10, command=lambda: [deletetask(index), popup.destroy()])
    edit_btn.pack(pady=2)
    delete_btn.pack(pady=2)

    def close_popup(e): popup.destroy()
    popup.bind("<FocusOut>", close_popup)
    popup.focus_set()

# Load tasks from file on startup
def load_tasks():
    try:
        with open("tasls.txt", "r") as f:
            for line in f:
                task = line.strip()
                if task:
                    tasks.append(task)
    except FileNotFoundError:
        # FIle doesn't exist yet, start with empty list
        pass
    update_counter()

def update_counter():
    counter_label.config(text=f"{completed_count}/{total_tasks_created}")

# Run application
load_tasks()
update_listbox()
root.mainloop()
