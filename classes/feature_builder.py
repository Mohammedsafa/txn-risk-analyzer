import numpy as np

class FeatureBuilder():
    def __init__(self):
        pass

    def build(self, df):
        print("Starting Feature Builder...")
        df['hour_of_day'] = df['timestamp'].dt.hour
        df['day_of_month'] = df['timestamp'].dt.day
        df['is_weekend'] = df['timestamp'].dt.weekday.isin([5, 6]).astype(int)
        df['is_night_transaction'] = (df['hour_of_day']<6).astype(int)
        df['pct_of_balance_spent'] = np.where(
            df['oldbalanceOrg']>0,
            df['amount'] / df['oldbalanceOrg'],
            np.where(df['amount']>0, 1.0, 0.0)
        )
        df['is_overdraft'] = ((df['type']!="CASH_IN") & (df['amount']> df['oldbalanceOrg'])).astype(int)

        expected_orig = np.where(
            df['type'] == "CASH_IN",
            df['oldbalanceOrg'] + df['amount'],
            df['oldbalanceOrg'] - df['amount']  
        )

        df['is_bal_asymmetry'] = (np.abs(df['newbalanceOrig'] - expected_orig) > 0.01).astype(int)


        df['dest_receive_count'] = df.groupby('nameDest')['amount'].transform('count')
        df['dest_total_volume'] = df.groupby('nameDest')['amount'].transform('sum')
        df['is_merchant_dest'] = df['nameDest'].str.startswith("M").astype(int)
        df['mule_indicator'] = np.where(
            df['nameDest'].str.startswith("C"),
            df['dest_receive_count'],
            0
        )
        expected_dest = np.where(
            df['type'] == "CASH_IN",
            df['oldbalanceDest'] - df['amount'], 
            df['oldbalanceDest'] + df['amount']  
        )

        df['is_dest_misaligned'] = (
            (np.abs(df['newbalanceDest'] - expected_dest) > 0.01) & 
            (~df['nameDest'].str.startswith("M"))
        ).astype(int)

        print(f"Feature Builder complete, New {len(df.columns)-11}")

        return df
