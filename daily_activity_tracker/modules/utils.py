# modules/utils.py
import speech_recognition as sr
import threading
from collections import Counter
import pandas as pd
from tkinter import messagebox
import datetime

def capture_speech_to_text(entry_widget, button):
    def listen():
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            button.config(bg='red', text='Listening...')
            try:
                audio_data = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio_data)
                entry_widget.delete(0, 'end')
                entry_widget.insert(0, text)
            except sr.UnknownValueError:
                messagebox.showinfo("Speech Recognition", "Could not understand audio")
            except sr.RequestError as e:
                messagebox.showinfo("Speech Recognition", f"Could not request results; {e}")
            except sr.WaitTimeoutError:
                messagebox.showinfo("Speech Recognition", "Listening timed out.")
            finally:
                button.config(bg='SystemButtonFace', text='Voice Input')

    threading.Thread(target=listen, daemon=True).start()

def generate_insights(activities):
    if not activities:
        messagebox.showinfo("No Data", "Not enough data to generate insights.")
        return

    df = pd.DataFrame(activities)
    if df.empty:
        messagebox.showinfo("No Data", "No activities available.")
        return

    # Most common task
    task_counter = Counter(df['task'])
    most_common_task = task_counter.most_common(1)[0][0] if task_counter else "N/A"

    # Total hours logged
    df['startTime'] = pd.to_datetime(df['startTime'], format='%H:%M', errors='coerce')
    df['endTime'] = pd.to_datetime(df['endTime'], format='%H:%M', errors='coerce')
    df['duration'] = (df['endTime'] - df['startTime']).dt.total_seconds() / 3600
    total_hours = df['duration'].sum()

    # Most common category
    category_counter = Counter(df['category'])
    most_common_category = category_counter.most_common(1)[0][0] if category_counter else "N/A"

    # Most common priority
    priority_counter = Counter(df['priority'])
    most_common_priority = priority_counter.most_common(1)[0][0] if priority_counter else "N/A"


    insights_message = (
        f"Most common task: {most_common_task}\n"
        f"Total hours logged: {total_hours:.2f}\n"
        f"Most common category: {most_common_category}\n"
        f"Most common priority: {most_common_priority}"
    )

    messagebox.showinfo("AI-Powered Insights", insights_message)
