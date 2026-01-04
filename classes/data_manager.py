import pandas as pd
import os
class DataManager:
    def __init__(self):
        self.required_cols = [
            'step', 'type', 'amount', 'nameOrig', 'oldbalanceOrg', 
            'newbalanceOrig', 'nameDest', 'oldbalanceDest', 'newbalanceDest'
        ]
    
    def load_csv(self, file_path):
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' not exist!!!")
            return None
        try:
            df = pd.read_csv(file_path)
            if self.validate_data(df):
                print(f"Successfully loaded {len(df)} transactions")
                return df
            return None
        except Exception as e:
            print(f"An error raised: {e}")
            return None
    
    def validate_data(self, df):
        missed = [col for col in self.required_cols if col not in df.columns]
        if missed:
            print(f"Validation error: missing columns {missed}")
            return False
        return True
   
        


    

