# main.py

import tkinter as tk
from tkinter import ttk, messagebox
import os
import pandas as pd
import matplotlib.pyplot as plt
import datetime  # Add this line
import time 
from modules.config_loader import ConfigLoader
from modules.data_handler import DataHandler
from modules.utils import capture_speech_to_text, generate_insights
from modules.ui_components import start_pomodoro
from modules.calendar_widget import CustomCalendar

class MainApplication(tk.Tk):
    def __init__(self, config_loader, data_handler, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.config_loader = config_loader
        self.data_handler = data_handler

        self.title("Daily Activity Tracker")
        self.geometry("800x600")

        # Load and set the application icon
        current_dir = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_dir, 'images', 'purdue_univ.png')
        if os.path.exists(image_path):
            self.iconphoto(True, tk.PhotoImage(file=image_path))

        self.create_widgets()
        self.set_default_date()

    def create_widgets(self):
        # Define the layout using grid
        for i in range(17):
            self.grid_rowconfigure(i, pad=5)
        for i in range(3):
            self.grid_columnconfigure(i, weight=1, pad=5)

        # Task
        tk.Label(self, text="Task").grid(row=0, column=0, sticky='w')
        self.task_entry = ttk.Combobox(self, values=self.config_loader.projects.get('projects', []))
        self.task_entry.grid(row=0, column=1, sticky='ew')

        # Category
        tk.Label(self, text="Category").grid(row=1, column=0, sticky='w')
        self.category_combobox = ttk.Combobox(self, values=self.config_loader.config.get('categories', []))
        self.category_combobox.grid(row=1, column=1, sticky='ew')

        # Priority
        tk.Label(self, text="Priority").grid(row=2, column=0, sticky='w')
        self.priority_combobox = ttk.Combobox(self, values=self.config_loader.config.get('priorities', []))
        self.priority_combobox.grid(row=2, column=1, sticky='ew')

        # Status
        tk.Label(self, text="Status").grid(row=3, column=0, sticky='w')
        self.status_combobox = ttk.Combobox(self, values=self.config_loader.config.get('statuses', []))
        self.status_combobox.grid(row=3, column=1, sticky='ew')

        # Start Time
        tk.Label(self, text="Start Time").grid(row=4, column=0, sticky='w')
        self.start_time_combobox = ttk.Combobox(self, values=self.config_loader.config.get('time_options', []))
        self.start_time_combobox.grid(row=4, column=1, sticky='ew')

        # End Time
        tk.Label(self, text="End Time").grid(row=5, column=0, sticky='w')
        self.end_time_combobox = ttk.Combobox(self, values=self.config_loader.config.get('time_options', []))
        self.end_time_combobox.grid(row=5, column=1, sticky='ew')

        # Notes
        tk.Label(self, text="Notes").grid(row=6, column=0, sticky='w')
        self.notes_entry = tk.Entry(self)
        self.notes_entry.grid(row=6, column=1, sticky='ew')
        voice_input_button_notes = tk.Button(self, text="Voice Input", command=lambda: capture_speech_to_text(self.notes_entry, voice_input_button_notes))
        voice_input_button_notes.grid(row=6, column=2, sticky='ew')

        # Comments
        tk.Label(self, text="Comments").grid(row=7, column=0, sticky='w')
        self.comments_entry = tk.Entry(self)
        self.comments_entry.grid(row=7, column=1, sticky='ew')
        voice_input_button_comments = tk.Button(self, text="Voice Input", command=lambda: capture_speech_to_text(self.comments_entry, voice_input_button_comments))
        voice_input_button_comments.grid(row=7, column=2, sticky='ew')

        # Date
        tk.Label(self, text="Date (MM-DD-YYYY)").grid(row=8, column=0, sticky='w')
        self.date_entry = tk.Entry(self)
        self.date_entry.grid(row=8, column=1, sticky='ew')

        date_button = ttk.Button(self, text="Select Date", command=self.open_calendar)
        date_button.grid(row=9, column=0, sticky='ew')

        add_button = tk.Button(
            self, text="Add Activity",
            command=self.add_activity
        )
        add_button.grid(row=9, column=1, sticky='ew')

        # Quick Add Buttons
        quick_add_frame = tk.Frame(self)
        quick_add_frame.grid(row=10, column=0, columnspan=3, sticky='ew')
        for idx, task in enumerate(self.config_loader.config.get('quick_add_tasks', [])):
            btn = tk.Button(quick_add_frame, text=task, command=lambda t=task: self.quick_add(t))
            btn.grid(row=0, column=idx, padx=2, pady=2)

        # Search Bar
        tk.Label(self, text="Search").grid(row=11, column=0, sticky='w')
        self.search_entry = tk.Entry(self)
        self.search_entry.grid(row=11, column=1, sticky='ew')
        search_button = tk.Button(self, text="Search", command=self.search_activity)
        search_button.grid(row=11, column=2)

        # Treeview for activities
        columns = ('Date', 'Task', 'Category', 'Priority', 'Status', 'Start Time', 'End Time', 'Duration', 'Notes', 'Comments')
        self.activity_tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            self.activity_tree.heading(col, text=col)
            self.activity_tree.column(col, anchor='center')
        self.activity_tree.grid(row=12, column=0, columnspan=3, sticky='nsew')

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.activity_tree.yview)
        self.activity_tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=12, column=3, sticky='ns')

        # Buttons at the bottom
        visualize_button = tk.Button(self, text="Visualize Activities", command=self.visualize_activities)
        visualize_button.grid(row=13, column=0, columnspan=3, sticky='ew')

        delete_button = tk.Button(self, text="Delete Activity", command=self.delete_activity)
        delete_button.grid(row=14, column=0, columnspan=3, sticky='ew')

        pomodoro_button = tk.Button(self, text="Start Timer", command=self.start_pomodoro_timer)
        pomodoro_button.grid(row=15, column=0, columnspan=3, sticky='ew')

        insights_button = tk.Button(self, text="Generate Insights", command=lambda: generate_insights(self.data_handler.activities))
        insights_button.grid(row=16, column=0, columnspan=3, sticky='ew')

        # Configure grid weights
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(12, weight=1)  # Make Treeview expandable

    def set_default_date(self):
        today = datetime.datetime.now().strftime(self.config_loader.config.get('default_date_format', '%m-%d-%Y'))
        self.date_entry.insert(0, today)

    def open_calendar(self):
        calendar = CustomCalendar(self, self.update_date_entry)
        calendar.grab_set()

    def update_date_entry(self, selected_date):
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, selected_date)

    def quick_add(self, task_name):
        self.task_entry.set(task_name)
        self.add_activity()

    def add_activity(self):
        unique_id = int(time.time())
        formatted_date = self.date_entry.get()

        if not formatted_date:
            messagebox.showinfo("No Date Selected", "Please select a date.")
            return

        try:
            start_time = pd.to_datetime(self.start_time_combobox.get(), format='%H:%M', errors='coerce')
            end_time = pd.to_datetime(self.end_time_combobox.get(), format='%H:%M', errors='coerce')
        except Exception:
            messagebox.showinfo("Invalid Time", "Please enter valid start and end times.")
            return

        if pd.isnull(start_time) or pd.isnull(end_time):
            messagebox.showinfo("Invalid Time", "Please enter valid start and end times.")
            return

        duration = (end_time - start_time).total_seconds() / 3600  # Duration in hours
        if duration < 0:
            messagebox.showinfo("Invalid Time", "End time cannot be earlier than start time.")
            return

        activity = {
            'id': unique_id,
            'date': formatted_date,
            'task': self.task_entry.get(),
            'category': self.category_combobox.get(),
            'priority': self.priority_combobox.get(),
            'status': self.status_combobox.get(),
            'startTime': self.start_time_combobox.get(),
            'endTime': self.end_time_combobox.get(),
            'duration': round(duration, 2),
            'notes': self.notes_entry.get(),
            'comments': self.comments_entry.get()
        }

        self.data_handler.activities.append(activity)
        self.data_handler.save_to_csv()
        self.update_task_recommendations()
        self.update_activity_tree()

        # Clear input fields
        for widget in [self.task_entry, self.category_combobox, self.priority_combobox,
                       self.status_combobox, self.start_time_combobox, self.end_time_combobox,
                       self.notes_entry, self.comments_entry]:
            widget.set('') if isinstance(widget, ttk.Combobox) else widget.delete(0, tk.END)

    def update_task_recommendations(self):
        existing_tasks = set(activity['task'] for activity in self.data_handler.activities)
        self.task_entry['values'] = list(existing_tasks)

    def update_activity_tree(self, filter_text=''):
        # Clear existing entries
        for item in self.activity_tree.get_children():
            self.activity_tree.delete(item)
        # Insert filtered activities
        for idx, activity in enumerate(self.data_handler.activities):
            task = activity.get('task', '')
            if isinstance(task, str) and filter_text.lower() in task.lower():
                self.activity_tree.insert('', 'end', iid=idx, values=(
                    activity['date'], activity['task'], activity['category'],
                    activity['priority'], activity['status'], activity['startTime'],
                    activity['endTime'], activity.get('duration', ''),
                    activity['notes'], activity['comments']
                ))

    def search_activity(self):
        search_text = self.search_entry.get()
        self.update_activity_tree(search_text)

    def delete_activity(self):
        selected_items = self.activity_tree.selection()
        if not selected_items:
            messagebox.showinfo("No Selection", "Please select an activity to delete.")
            return
        for item in selected_items:
            try:
                index_to_delete = int(item)
                del self.data_handler.activities[index_to_delete]
                self.activity_tree.delete(item)
            except (ValueError, IndexError):
                messagebox.showerror("Error", f"Unable to delete item with id: {item}")
        self.data_handler.save_to_csv()

    def visualize_activities(self):
        df = pd.DataFrame(self.data_handler.activities)
        if df.empty:
            messagebox.showinfo("No Data", "There are no activities to visualize.")
            return

        df['startTime'] = pd.to_datetime(df['startTime'], format='%H:%M', errors='coerce')
        df['endTime'] = pd.to_datetime(df['endTime'], format='%H:%M', errors='coerce')
        df['duration'] = (df['endTime'] - df['startTime']).dt.total_seconds() / 3600
        df['duration'] = df['duration'].apply(lambda x: max(x, 0))

        task_duration = df.groupby('task')['duration'].sum()
        if task_duration.empty or task_duration.sum() == 0:
            messagebox.showinfo("No Data", "There are no tasks with valid durations to visualize.")
            return

        plt.figure(figsize=(8, 8))
        task_duration.plot(kind='pie', autopct='%1.1f%%', startangle=140)
        plt.title('Time Spent on Different Tasks')
        plt.ylabel('')
        plt.tight_layout()
        plt.show()

    def start_pomodoro_timer(self):
        task_name = self.task_entry.get()
        if not task_name:
            messagebox.showinfo("No Task Selected", "Please select or enter a task to start the timer.")
            return
        start_pomodoro(self, task_name)

if __name__ == '__main__':
    # Ensure required directories exist
    os.makedirs('data', exist_ok=True)
    os.makedirs('images', exist_ok=True)
    os.makedirs('config', exist_ok=True)
    os.makedirs('modules', exist_ok=True)

    # Initialize configuration and data handlers
    config_loader = ConfigLoader()
    data_handler = DataHandler()
    data_handler.load_from_csv()

    # Start the application
    app = MainApplication(config_loader, data_handler)
    app.mainloop()
