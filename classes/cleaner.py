import numpy as np
from datetime import datetime, timedelta

class Cleaner():
    def __init__(self, start_date="2016-09-01 00:00:00"):
        self.ref_data = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")

    def clean_data(self, df):
        if df is None or df.empty:
            print("Error: No data provided!!!")
            return None
        print("Starting Data Cleaning & Preparation....")

        df = df.drop_duplicates()

        df['timestamp'] = df['step'].apply(lambda x: self.ref_data + timedelta(hours=int(x-1)))


        df['nameOrig'] = df['nameOrig'].astype(str).str.strip()
        df['nameDest'] = df['nameDest'].astype(str).str.strip()



        print("Cleaning complete...")
        return df





