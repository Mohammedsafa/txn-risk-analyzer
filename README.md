# Financial Transaction Risk Analyzer (6M+ Records)

A high-performance analytics engine designed to detect fraudulent patterns in massive financial datasets. This system processes over **6.3 million transactions** using optimized vectorization to identify money muling, overdraft manipulation, and behavioral anomalies.



## 🧠 Risk Scoring Methodology
The system uses a weighted scoring algorithm based on academic research and industry standards.

### 1. Weighted Scoring Model
| Category | Research-Based "Weight" (0-100 Scale) | Scientific Justification |
| :--- | :---: | :--- |
| **Logical Discrepancy** | 45 - 50 Points | **Source: Lopez-Rojas (PaySim Paper).** Features like `is_overdraft` and `balance_drain` have the highest "Information Gain." In this synthetic data, fraud is a "zero-sum" attack. If the balance is zeroed out, the probability of fraud is nearly 100% for TRANSFER types. |
| **Relational / Network** | 25 - 30 Points | **Source: FATF (Financial Action Task Force).** High-velocity incoming transfers to non-merchant accounts (`mule_indicator`) is the primary "Signal" for money laundering. It is a "Leading Indicator." |
| **Contextual / Temporal** | 10 - 15 Points | **Source: Journal of Forensic & Investigative Accounting.** `is_night` and `is_weekend` act as "Supporting Evidence." They rarely prove fraud alone but "multiply" the risk when combined with logical errors. |

> **Note on Localization:** Weekend logic is set to Saturday/Sunday based on the dataset's origin, but can be localized (e.g., Friday/Saturday for Egypt) by adjusting the weekday offset in the `FeatureBuilder` class.

### 2. Risk Bands & Security Actions
| Score | Band | Action (Industry Standard) |
| :--- | :---: | :--- |
| 0 - 30 | **Low** | **Pass:** No intervention. |
| 31 - 70 | **Medium** | **Challenge:** Trigger 2FA (SMS/Biometric). |
| 71 - 90 | **High** | **Review:** Manual review by a fraud analyst. |
| 91 - 100 | **Critical** | **Block:** Automatic transaction decline. |

---

## 🛠️ Feature Engineering & Insights
The system transforms raw data into high-fidelity "Fraud Signals":

* **Balance Asymmetry (`is_bal_asymmetry`):** Detects if the amount subtracted from the origin does not match the amount added to the destination, identifying "phantom" credit attacks.
* **Mule Indicator:** Tracks destination accounts receiving high-frequency, high-value transfers within short time windows, a hallmark of money laundering.
* **Drain Ratio (`pct_of_balance_spent`):** Measures the intensity of the account "wipe-out." Fraudsters typically attempt to move $100\%$ of available funds in a single transaction.
* **Temporal Windows:** Flags "Out-of-Hours" activity, identifying transactions occurring during high-risk windows (e.g., 2 AM - 5 AM).



## 🚀 Performance & Scalability
* **Vectorized Engine:** Built with Python, Pandas, and NumPy to avoid slow iterative loops.
* **Throughput:** Capable of processing **6,362,620 rows** in under 120 seconds on standard hardware.
* **Architecture:** Follows a modular class-based structure for easy integration into existing banking CI/CD pipelines.

## 💻 Installation & Usage
1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/Mohammedsafa/txn-risk-analyzer.git](https://github.com/Mohammedsafa/txn-risk-analyzer.git)
    cd txn-risk-analyzer
    ```
2.  **Install Dependencies:**
    ```bash
    pip install pandas numpy scipy
    ```
3.  **Run the Analyzer:**
    ```bash
    python main.py
    ```

## 👨‍💻 Author
Developed by Mohammed Safa for academic and purposes.
