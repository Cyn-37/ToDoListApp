To-Do List Application
This is a simple To-Do List application built using Python's tkinter library. The app allows users to manage their tasks efficiently by adding, removing, marking as completed, and sorting tasks based on priority or deadline. It also supports setting task reminders and stores tasks in an SQLite database for persistence across sessions.

Features
Add Tasks: Users can add tasks with title, description (optional), category, priority, and a deadline.
Mark Tasks as Completed: Once a task is done, users can mark it as completed.
Remove Tasks: Users can delete tasks from their list.
Search Functionality: Real-time search through tasks based on title, description, or category.
Sort Tasks: Sort tasks by priority or deadline.
Task Reminders: Reminders will pop up when a task's deadline is approaching (within 5 minutes).
Database Storage: Tasks are stored in an SQLite database for persistence across sessions.
Responsive UI: The app features a scrollable task list and a clean, user-friendly interface.

Libraries Used
tkinter: For the graphical user interface (GUI).
tkcalendar: For date selection when setting task deadlines.
sqlite3: For storing tasks in a local database.
datetime: For managing and comparing task deadlines.

Installation
Clone the repository:
git clone https://github.com/your-username/todo-list-app.git
Navigate to the project directory:
cd todo-list-app
Install the required dependencies:
pip install tkcalendar

Usage
Run the application:
python main.py
The main window will open where you can:
Add tasks by clicking "Add Task" and filling in the required information.
Remove tasks by selecting a task and clicking "Remove Task".
Mark tasks as completed by selecting a task and clicking "Mark Completed".
Sort tasks by priority or deadline.
Search for tasks using the search bar.
