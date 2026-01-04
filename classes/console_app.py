import pandas as pd
import time
import os
import sys
from .data_manager import DataManager
from .cleaner import Cleaner
from .feature_builder import FeatureBuilder
from .risk_scorer import RiskScorer
from .flagger import TransactionFlagger
from .report_gen import ReportGenerator


class FraudConsoleApp:
    def __init__(self):
        self.df = None
        self.manager = DataManager()
        self.cleaner = Cleaner()
        self.builder = FeatureBuilder()
        self.scorer = RiskScorer()
        self.flagger = TransactionFlagger()
        self.reporter = ReportGenerator(output_dir="reports/")

    def display_menu(self):
        print("\n" + "="*50)
        print("........ FRAUD DETECTION COMMAND CENTER (6M+ ROWS) ........")
        print("="*50)
        print(" 1. Load dataset")
        print(" 2. Clean and validate data")
        print(" 3. Build features")
        print(" 4. Score customers")
        print(" 5. Flag suspicious transactions")
        print(" 6. Export reports")
        print(" 7. Display summary in console")
        print(" 0. Exit application")
        print("-" * 50)

    def run(self):

        while True:
            self.display_menu()
            choice = input("Select an option [0-7]: ")

            try:
                if choice == '1':
                    print(" * Reading 6 million rows... this may take a moment...")
                    file_path = r"data/paysim_fraud_transactions.csv"
                    start = time.time()
                    self.df = self.manager.load_csv(file_path)
                    if self.df is not None:
                        print(f" + Loaded in {time.time()-start:.2f}s")
                elif choice == '2':
                    if self.df is not None:
                        print(" * Cleaning data and converting timestamps...")
                        start = time.time()
                        self.manager.validate_data(self.df)
                        self.df = self.cleaner.clean_data(self.df)
                        print(f" + Finished in {time.time()-start:.2f}s")
                    else:
                        print("!!! Error: No data found. Load CSV first.")
                elif choice == '3':
                    if self.df is not None and 'timestamp' in self.df.columns:
                        print(" * Calculating features (Overdrafts, Asymmetry, Mules)...")
                        start = time.time()
                        self.df = self.builder.build(self.df)
                        print(f" + Finished in {time.time()-start:.2f}s")
                    else:
                        print("!!! Error: Clean data first.")
                elif choice == '4':
                    if self.df is not None and 'mule_indicator' in self.df.columns:
                        print(" * Scoring 6 million transactions...")
                        start = time.time()
                        self.df = self.scorer.calc_risk(self.df)
                        print(f" + Finished in {time.time()-start:.2f}s")
                    else:
                        print("!!! Error: Build features first.")
                elif choice == '5':
                    if self.df is not None and 'risk_score' in self.df.columns:
                        print(" * Applying security flags and decision logic...")
                        start = time.time()
                        self.df = self.flagger.flag_transaction(self.df)
                        print(f" + Finished in {time.time()-start:.2f}s")
                    else:
                        print("!!! Error: Score data first.")
                elif choice == '6':
                    if self.df is not None and 'security_action' in self.df.columns:
                        start = time.time()
                        if not os.path.exists('reports'): os.makedirs('reports')
                        self.reporter.generate(self.df)
                        print(f" + Finished in {time.time()-start:.2f}s")
                    else:
                        print("!!! Error: Complete flagging before exporting.")
                elif choice == '7':
                    if self.df is not None:
                        self.show_summary()
                    else:
                        print("!!! No data loaded.")
                elif choice == '0':
                    print("Shutting down... Clear memory... Goodbye!")
                    sys.exit()
                else:
                    print("!!! Invalid input.")
            except Exception as e:
                print(f"!!! SYSTEM ERROR during operation: {e}")
    
    def show_summary(self):
        report_path = "reports/report_summary.txt"
        
        print("\n" + "="*50)
        print("........ CONSOLE SUMMARY VIEW ........")
        print("="*50)

        if os.path.exists(report_path):
            with open(report_path, 'r') as f:
                print(f.read())
        else:
            print("!!! No report file found.")
            print(" * Please run Option 6 (Export Reports) first to generate the summary.")
        
        print("="*50)

                

                



