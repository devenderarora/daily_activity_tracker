# modules/calendar_widget.py
import tkinter as tk
from tkinter import ttk
import calendar as cal
import datetime

class CustomCalendar(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.title("Select Date")
        self.geometry("532x220")

        self.current_date = datetime.datetime.today()
        self.selected_date = None

        self.init_widgets()

    def init_widgets(self):
        self.header = ttk.Frame(self)
        self.header.pack(fill='x')

        self.prev_button = ttk.Button(self.header, text='<', command=self.go_prev)
        self.prev_button.pack(side='left')

        self.next_button = ttk.Button(self.header, text='>', command=self.go_next)
        self.next_button.pack(side='right')

        self.month_year_label = ttk.Label(self.header)
        self.month_year_label.pack(fill='x', expand=True)

        self.calendar_frame = ttk.Frame(self)
        self.calendar_frame.pack(fill='both', expand=True)

        self.draw_calendar()

    def draw_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        year, month = self.current_date.year, self.current_date.month
        month_cal = cal.monthcalendar(year, month)
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

        self.month_year_label.config(text=f'{cal.month_name[month]} {year}')

        for i, day in enumerate(days):
            lbl = ttk.Label(self.calendar_frame, text=day)
            lbl.grid(row=0, column=i, padx=5, pady=5)

        for row, week in enumerate(month_cal):
            for col, day in enumerate(week):
                if day == 0:
                    continue
                btn = ttk.Button(self.calendar_frame, text=str(day), command=lambda d=day: self.select_date(d))
                btn.grid(row=row+1, column=col, padx=2, pady=2)

    def select_date(self, day):
        self.selected_date = datetime.date(self.current_date.year, self.current_date.month, day)
        self.callback(self.selected_date.strftime('%m-%d-%Y'))
        self.destroy()

    def go_prev(self):
        first_day = self.current_date.replace(day=1)
        prev_month = first_day - datetime.timedelta(days=1)
        self.current_date = prev_month.replace(day=1)
        self.draw_calendar()

    def go_next(self):
        days_in_month = cal.monthrange(self.current_date.year, self.current_date.month)[1]
        next_month = self.current_date + datetime.timedelta(days=days_in_month)
        self.current_date = next_month.replace(day=1)
        self.draw_calendar()
