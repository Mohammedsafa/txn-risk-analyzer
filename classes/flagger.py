import numpy as np

class TransactionFlagger:
    def __init__(self):
        self.high_risk_threshold = 70
        self.critical_threshold = 90

    def flag_transaction(self, df):
        print("Stearing Transaction Flagger....")

        df['is_flagged_suspicious'] = (df['risk_score']>= self.high_risk_threshold).astype(int)

        action_conditions = [
            (df['risk_score'] >= self.critical_threshold),
            (df['risk_score'] >= self.high_risk_threshold) & (df['risk_score'] < self.critical_threshold),
            (df['risk_score'] >= 30) & (df['risk_score'] < self.high_risk_threshold)
        ]

        actions = [
            'BLOCK_AND_REPORT',
            'MANUAL_REVIEW_REQUIRED',
            'SMS_VERIFICATION_SENT'
        ]

        df['security_action'] = np.select(action_conditions, actions, default='ALLOW')

        flagged_count = df['is_flagged_suspicious'].sum()


        print(f"Flagger complete. Total Alerts Founded: {flagged_count}")

        return df