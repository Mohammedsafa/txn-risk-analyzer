

class ReportGenerator:
    def __init__(self, output_dir="reports/"):
        self.output_dir = output_dir

    def generate(self, df):
        print("Generating Reports....")

        lead_risks = df[df['risk_band'].isin(['High','Critical'])].copy()
        cols_to_save = [
            'type', 'amount', 'nameOrig', 'nameDest', 'risk_score',
            'risk_band', 'security_action', 'is_bal_asymmetry', 'is_overdraft',
            'mule_indicator', 'pct_of_balance_spent'
        ]

        lead_risks_path = f"{self.output_dir}investigation.csv"
        lead_risks[cols_to_save].to_csv(lead_risks_path)

        print(f"CSV Report saved: {lead_risks_path}")

        total_transactions = len(df)
        total_vol = df['amount'].sum()

        money_saved = df[df['security_action']=='BLOCK_AND_REPORT']['amount'].sum()

        total_flagged = df['is_flagged_suspicious'].sum()
        alert_rate = (total_flagged / total_transactions) *100

        risk_counts = df['risk_band'].value_counts()

        top_mules = df.groupby('nameDest')['mule_indicator'].max().sort_values(ascending=False).head(5)

        report_path = f"{self.output_dir}report_summary.txt"

        with open(report_path, 'w')as f:
            f.write("FRAUD DETECTION SYSTEM - REPORT SUMMARY\n")
            f.write("="*42 + "\n\n")

            f.write("A. DATASET OVERVIEW\n")
            f.write(f"- Total Transaction Processed: {total_transactions:,}\n")
            f.write(f"- Total Volume Moved: ${total_vol:,.2f}\n\n")

            f.write("B. PERFORMANCE METRICS\n")
            f.write(f"- TOTAL MONEY SAVED (BLOCKED): ${money_saved:,.2f}\n")
            f.write(f"- System Alert Rate: {alert_rate:.2f}%\n")
            f.write(f"- Total High-Risk Alerts: {total_flagged:,}\n\n")

            f.write("C. RISK DISTRIBUTION\n")
            for band, count in risk_counts.items():
                f.write(f"- {band}: {count:,}\n")
            f.write("\n")


            f.write("D. TOP SUSPECT INDIVIDUAL ACCOUNTS (BY FREQUENCY)\n")
            for acc, count in top_mules.items():
                if count > 0: 
                    f.write(f"- Account: {acc} | Received Transfers: {int(count)}\n")

        print(f"Text Report saved: {report_path}")




