# modules/ui_components.py

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time

def start_pomodoro(parent, task_name):
    pomodoro_window = tk.Toplevel(parent)
    pomodoro_window.title(f"Pomodoro Timer - {task_name}")
    pomodoro_window.geometry("300x200")

    timer_label = tk.Label(pomodoro_window, text="25:00", font=("Helvetica", 48), fg="white", bg="black")
    timer_label.pack(expand=True, fill='both')

    progress = ttk.Progressbar(pomodoro_window, orient="horizontal", length=200, mode="determinate")
    progress.pack(pady=20)

    def countdown(t):
        progress['value'] = 0
        progress['maximum'] = t
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            if timer_label.winfo_exists():
                timer_label.config(text=timer)
                progress['value'] += 1
                pomodoro_window.update()
                time.sleep(1)
                t -= 1
            else:
                return
        if pomodoro_window.winfo_exists():
            messagebox.showinfo("Pomodoro", f"Pomodoro for {task_name} completed!")
            pomodoro_window.destroy()

    threading.Thread(target=countdown, args=(25*60,), daemon=True).start()
