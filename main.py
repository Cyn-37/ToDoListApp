import tkinter as tk
from tkinter import messagebox, simpledialog
from tkcalendar import Calendar
from datetime import datetime
import sqlite3

class Task:
    def __init__(self, title, description, deadline, category, priority):
        self.title = title
        self.description = description
        self.completed = False
        self.deadline = deadline
        self.category = category
        self.priority = priority
        self.reminder_shown = False

    def mark_completed(self):
        self.completed = True
    
    def __str__(self):
        status = "✓" if self.completed else "✗"
        return f"[{status}] {self.title} ({self.category}, Priority: {self.priority}) - {self.description} (Deadline: {self.deadline.strftime('%Y-%m-%d %H:%M')})"

class ToDoListApp:
    def __init__(self, root):
        self.root = root # main window
        self.root.title("To-Do List")
        self.root.configure(bg="#001f3f")

        self.tasks = []
        self.init_db()  # Initialize the database
        
        self.frame = tk.Frame(self.root, bg="#001f3f") 
        self.frame.pack(pady=10)
        
        self.task_listbox = tk.Listbox(self.frame, width=50, height=10, font=("Arial", 12), bg="#ffffff", selectbackground="#cce5ff", selectforeground="#000000")
        self.task_listbox.pack(side=tk.LEFT)
        
        # scrollbars
        self.scrollbar_y = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.scrollbar_x = tk.Scrollbar(self.root, orient=tk.HORIZONTAL)
        self.scrollbar_x.pack(fill=tk.X)
        
        self.task_listbox.config(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set) # Link the vertical and horizontal scrollbars to the listbox
        self.scrollbar_y.config(command=self.task_listbox.yview) # Update the listbox when the vertical scrollbar is used
        self.scrollbar_x.config(command=self.task_listbox.xview) # Update the listbox when the horizontal scrollbar is used

        # search field 
        self.search_entry = tk.Entry(self.root, width=50, font=("Arial", 12))
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<KeyRelease>", self.search_tasks) # Bind key release event to search tasks in real-time

        # Create a frame for the buttons
        self.button_frame = tk.Frame(self.root, bg="#001f3f")
        self.button_frame.pack(pady=5)

        self.add_button = tk.Button(self.button_frame, text="Add Task", command=self.open_task_window, bg="#5c92b4", fg="#ffffff", font=("Arial", 12), padx=10, pady=5)  # رنگ خاص‌تر برای دکمه Add Task
        self.add_button.grid(row=0, column=0, padx=5, pady=5)

        self.remove_button = tk.Button(self.button_frame, text="Remove Task", command=self.remove_task, bg="#ff9999", fg="#000000", font=("Arial", 12), padx=10, pady=5)  # قرمز ملایم برای Remove Task
        self.remove_button.grid(row=0, column=1, padx=5, pady=5)

        self.complete_button = tk.Button(self.button_frame, text="Mark Completed", command=self.mark_completed, bg="#77dd77", fg="#000000", font=("Arial", 12), padx=10, pady=5)  # سبز پاستلی
        self.complete_button.grid(row=1, column=0, padx=5, pady=5)

        # sort
        self.sort_priority_button = tk.Button(self.button_frame, text="Sort by Priority", command=self.sort_by_priority, bg="#c2d1ff", fg="#000000", font=("Arial", 12), padx=10, pady=5)  # رنگ ملایم
        self.sort_priority_button.grid(row=1, column=1, padx=5, pady=5)

        self.sort_deadline_button = tk.Button(self.button_frame, text="Sort by Deadline", command=self.sort_by_deadline, bg="#c2d1ff", fg="#000000", font=("Arial", 12), padx=10, pady=5)  # رنگ ملایم
        self.sort_deadline_button.grid(row=2, column=0, padx=5, pady=5)

        # About Us
        self.about_button = tk.Button(self.button_frame, text="About Us", command=self.show_about, bg="#c2d1ff", fg="#000000", font=("Arial", 12), padx=10, pady=5)  # رنگ ملایم
        self.about_button.grid(row=2, column=1, padx=5, pady=5)

        self.load_tasks()  # Load tasks after initializing the task_listbox
        self.root.after(60000, self.check_reminders)

    def init_db(self):
        self.conn = sqlite3.connect('tasks.db') # Connect to the SQLite database (create if it doesn't exist)
        self.cursor = self.conn.cursor()  # Create a cursor to execute SQL commands
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
            title TEXT,
            description TEXT,
            deadline TEXT,
            category TEXT,
            priority INTEGER,
            completed INTEGER
        )''')
        self.conn.commit()  # Commit changes to the database

    def load_tasks(self):
        self.cursor.execute("SELECT * FROM tasks")  # Execute SQL to fetch all tasks from the database
        rows = self.cursor.fetchall()  # Retrieve all rows from the executed query
        for row in rows:  
            title, description, deadline, category, priority, completed = row  # Unpack the row into variables
            task = Task(title, description, datetime.strptime(deadline, "%Y-%m-%d %H:%M"), category, priority)  # Create a Task object
            task.completed = bool(completed)  # Set the completed status (convert to boolean)
            self.tasks.append(task) 
        self.update_task_listbox() 


    def save_task(self, task): # Insert a new task into the tasks table in the database
        self.cursor.execute("INSERT INTO tasks (title, description, deadline, category, priority, completed) VALUES (?, ?, ?, ?, ?, ?) ",
                            (task.title, task.description, task.deadline.strftime("%Y-%m-%d %H:%M"), task.category, task.priority, int(task.completed)))
        self.conn.commit() # Commit the changes to the database

    def show_about(self):
        messagebox.showinfo("About Us", "This is a simple To-Do List application.\n\n"
                                           "You can add, remove, and manage your tasks efficiently.\n"
                                           "Developed to help you stay organized and productive!\n"
                                           "For more information, contact the developer.")

    def open_task_window(self):
        self.task_window = tk.Toplevel(self.root) # Create a new Toplevel window
        self.task_window.title("Add Task")
        self.task_window.configure(bg="#5c92b4")  

        tk.Label(self.task_window, text="Title:", bg="#5c92b4").pack(pady=5)
        self.title_entry = tk.Entry(self.task_window)
        self.title_entry.pack(pady=5)

        tk.Label(self.task_window, text="Description: (optional)", bg="#5c92b4").pack(pady=5)
        self.description_entry = tk.Entry(self.task_window)
        self.description_entry.pack(pady=5)

        tk.Label(self.task_window, text="Category:", bg="#5c92b4").pack(pady=5)
        self.category_entry = tk.Entry(self.task_window)
        self.category_entry.pack(pady=5)

        tk.Label(self.task_window, text="Priority (1=High, 2=Medium, 3=Low):", bg="#5c92b4").pack(pady=5)
        self.priority_entry = tk.Entry(self.task_window)
        self.priority_entry.pack(pady=5)

        tk.Label(self.task_window, text="Deadline:", bg="#5c92b4").pack(pady=5)
        self.deadline_label = tk.Label(self.task_window, text="Select Date", bg="#5c92b4")
        self.deadline_label.pack(pady=5)
        
        self.calendar = Calendar(self.task_window, selectmode='day', date_pattern="y-mm-dd")
        self.calendar.pack(pady=20)

        add_task_button = tk.Button(self.task_window, text="Add Task", command=self.add_task, bg="#77dd77", fg="#000000")  
        add_task_button.pack(pady=10)

    def add_task(self):
        # Check if the task window exists and is open; if not, exit the function
        if not hasattr(self, 'task_window') or not self.task_window.winfo_exists():
            return
        
        title = self.title_entry.get()
        description = self.description_entry.get()
        category = self.category_entry.get()
        priority = self.priority_entry.get()
        
        if not title or not category or not priority:
            messagebox.showwarning("Warning", "Please fill Title, Category, and Priority fields.")
            return

        # Error handling
        try:
            priority = int(priority)
            if priority not in [1, 2, 3]:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Warning", "Priority must be 1, 2, or 3.")
            return

        selected_date = self.calendar.get_date()
        time_str = simpledialog.askstring("Task Time", "Enter time (HH:MM, 24-hour format):")
        try:
            deadline_str = f"{selected_date} {time_str}"
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
            if deadline < datetime.now() :
                raise ValueError
        except ValueError:
            messagebox.showwarning("Warning", "Invalid date or time format.")
            return

        task = Task(title, description, deadline, category, priority)
        self.tasks.append(task)
        self.save_task(task) 
        self.update_task_listbox()
        self.task_window.destroy()

    def remove_task(self):
        selected_index = self.task_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "Please select a task to remove.")
            return
        
        task_to_remove = self.tasks[selected_index[0]]
        self.tasks.remove(task_to_remove)
        self.cursor.execute("DELETE FROM tasks WHERE title = ? AND deadline = ?", (task_to_remove.title, task_to_remove.deadline.strftime("%Y-%m-%d %H:%M")))
        self.conn.commit()  
        self.update_task_listbox()

    def mark_completed(self):
        selected_index = self.task_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "Please select a task to mark as completed.")
            return
        
        task_to_complete = self.tasks[selected_index[0]]
        task_to_complete.mark_completed()
        self.cursor.execute("UPDATE tasks SET completed = 1 WHERE title = ? AND deadline = ?", (task_to_complete.title, task_to_complete.deadline.strftime("%Y-%m-%d %H:%M")))
        self.conn.commit() 
        self.update_task_listbox()

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END) # Clear all items from the task listbox
        now = datetime.now()  

        for task in self.tasks:
            task_str = str(task)

            if task.completed:
                # If the task is completed, set a green background
                self.task_listbox.insert(tk.END, task_str)
                self.task_listbox.itemconfig(tk.END, {'bg': '#c4e1c4'})  

            elif task.deadline < now:
                # If the task is overdue, set a gray background
                self.task_listbox.insert(tk.END, task_str)
                self.task_listbox.itemconfig(tk.END, {'bg': '#d3d3d3'}) 

            elif (task.deadline - now).total_seconds() <= 3600:
                # If the task is due in less than an hour, set a red background
                self.task_listbox.insert(tk.END, task_str)
                self.task_listbox.itemconfig(tk.END, {'bg': '#ffcccb'})  

            else:
                # the default background color
                self.task_listbox.insert(tk.END, task_str)

    def search_tasks(self, event):
        search_query = self.search_entry.get().lower()
        self.task_listbox.delete(0, tk.END)

        for task in self.tasks:
            if search_query in task.title.lower() or search_query in task.description.lower() or search_query in task.category.lower():
                self.task_listbox.insert(tk.END, str(task))

    def sort_by_priority(self):
        self.tasks.sort(key=lambda x: x.priority) # Sort tasks by their priority in ascending order
        self.update_task_listbox()

    def sort_by_deadline(self):
        self.tasks.sort(key=lambda x: x.deadline) # Sort tasks by their deadline in ascending order
        self.update_task_listbox()

    def check_reminders(self):
        for task in self.tasks:
            if not task.reminder_shown and not task.completed and (task.deadline - datetime.now()).total_seconds() <= 300:
                messagebox.showinfo("Reminder", f"Reminder: Task '{task.title}' is due soon!")
                task.reminder_shown = True
        self.root.after(60000, self.check_reminders)

if __name__ == "__main__":
    # Create the main application window
    root = tk.Tk()
    # Initialize the ToDoListApp with the main window
    app = ToDoListApp(root)
    # Start the main loop to listen for events
    root.mainloop()
