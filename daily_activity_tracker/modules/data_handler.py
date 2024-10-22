# modules/data_handler.py
import pandas as pd
import os

class DataHandler:
    def __init__(self, data_file='data/activities.csv'):
        self.data_file = data_file
        self.activities = []

    def load_from_csv(self):
        if not os.path.exists(self.data_file):
            self.activities = []
            return
        try:
            df = pd.read_csv(self.data_file)
            df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime('%m-%d-%Y')
            self.activities = df.to_dict('records')
        except Exception as e:
            print(f"An error occurred while loading data: {e}")
            self.activities = []

    def save_to_csv(self):
        try:
            df = pd.DataFrame(self.activities)
            df.to_csv(self.data_file, index=False)
        except Exception as e:
            print(f"An error occurred while saving data: {e}")
