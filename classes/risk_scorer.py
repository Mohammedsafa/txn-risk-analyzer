import pandas as pd
import numpy as np
from scipy.stats import zscore

class RiskScorer:
    def __init__(self):
        self.WEIGHT_CRITICAL = 45 
        self.WEIGHT_HIGH = 30 
        self.WEIGHT_MEDIUM = 15
        self.WEIGHT_STATS = 10
    def calc_risk(self, df):
        print("Calculating Risk Scores....")

        risk_points = np.zeros(len(df))

        logical_mask = (df['is_bal_asymmetry']==1) | (df['is_overdraft']==1) | (df['is_dest_misaligned'] == 1)
        risk_points += np.where(logical_mask, self.WEIGHT_CRITICAL,0)

        risk_points += np.where(df['pct_of_balance_spent']>=0.9,self.WEIGHT_STATS, 0)

        risk_points += np.where(df['mule_indicator']>5, self.WEIGHT_HIGH,0)

        temp_mask = (df['is_weekend']==1) | (df['is_night_transaction']==1)
        risk_points += np.where(temp_mask, self.WEIGHT_MEDIUM,0)

        df['amount_zscore'] = df.groupby('type')['amount'].transform(lambda x: zscore(x, ddof=0))
        risk_points += np.where(df['amount_zscore'].abs()>3, self.WEIGHT_STATS, 0)
        
        df['risk_score'] = risk_points

        conditions = [
            (df['risk_score'] <=30),
            (df['risk_score']>30) & (df['risk_score']<=70),
            (df['risk_score']>70) & (df['risk_score']<=90),
            (df['risk_score']>90)
        ]

        risk_labels = ['Low', 'Medium', 'High', 'Critical']

        df['risk_band'] = np.select(conditions, risk_labels, default='Low')

        print(f"Risk Scoring complete. Max score found {df['risk_score'].max()}")

        return df


