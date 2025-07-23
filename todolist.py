import tkinter as tk
from tkinter import messagebox, simpledialog

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

# list of tasks
tasks = []

# Frame for Listbox and Scrollbar
frame = tk.Frame(root, bg=bluer_indigo)
frame.pack(pady=15)

# Scrollbar
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Styled Listbox
listbox = tk.Listbox(
    frame,
    yscrollcommand=scrollbar.set,
    bg="#E6E6FA",            # Light purple
    fg="black",
    font=("Arial", 12),
    selectbackground="#D8BFD8",  # Thistle when selected
    relief="solid",          # Rectangle border
    bd=2,
    width=30,                # Rectangle width
    height=10                # Number of visible items
)
listbox.pack(side=tk.LEFT, fill=tk.BOTH)

# Configure scrollbar
scrollbar.config(command=listbox.yview)

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
        listbox.delete(0, tk.END) # Clear listbox
        save_tasks()
        for t in tasks:
            listbox.insert(tk.END, t)

# Create a addtask button
my_button = tk.Button(root, text="Add task", command=addtask)

# show the button on the window
my_button.pack(side = "bottom", pady=20)

def update_listbox():
    listbox.delete(0, tk.END) # clear listbox
    for t in tasks:
        listbox.insert(tk.END, t) # INnsert updated tasks

# Function to delete task
def deletetask():
    try:
        selected_index = listbox.curselection()[0] #Get selcted index
        task_to_delete = tasks[selected_index]
        confirm = messagebox.askyesno("Delete Task", f"Are you sure you want to delete task {task_to_delete} ?")
        if confirm:
            tasks.pop(selected_index) # remove from list
            update_listbox()
            save_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "PLease select a task to delete.")


# Create a delete task button
my_delbutton = tk.Button(root, text="Delete task", command=deletetask)

# show the button on the window
my_delbutton.pack(side = "bottom", pady=20)

# save tasks to a file
def save_tasks():
    with open("tasls.txt", "w") as f:
        for task in tasks:
            f.write(task + "\n")

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

# Run application
load_tasks()
update_listbox()
root.mainloop()