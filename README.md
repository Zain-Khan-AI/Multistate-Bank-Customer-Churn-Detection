# 📊 Multistate Bank Customer Churn Detection

An interactive, high-performance **Analytics Dashboard and Machine Learning Churn Predictor** built with Python and Streamlit. This project aims to analyze bank customer attrition (churn) patterns from historical data (10,000 customers) and predict individual customer churn risk in real-time.

---

## 🌟 Key Features

### 1. 🔍 Interactive Analytics Filter Panel
- Filter customer data dynamically by **Country**, **Gender**, **Number of Products**, **Active Membership Status**, **Age Range**, and **Credit Score Range**.
- Dynamic KPI counters automatically update based on selection:
  - **Total Customers**
  - **Average Credit Score**
  - **Average Balance**
  - **Active Member Rate**
  - **Churn Rate**

### 2. 📈 Rich Visualizations (8 Plotly Charts)
- **Overall Churn Distribution:** Donut chart showcasing customer share.
- **Churn Rate by Country:** Geographic attrition highlights (with Germany showing double the churn rate of others).
- **Churn Rate by Number of Products:** Insights showing product proliferation risks.
- **Churn Rate by Age Group:** Area chart illustrating high-risk older age demographics.
- **Churn Rate by Gender:** Visualizing gender-based attrition variation.
- **Active vs Inactive Churn:** Contrast between engaged and disengaged accounts.
- **Churn Rate by Tenure:** Continuous area trend analysis.
- **Credit Score Distribution:** Interactive Box plot comparing churned vs. retained customers.

### 3. 🔗 Feature Correlation Heatmap
- Interactive coefficient matrix showing linear correlations between key features and customer attrition (Age has the highest positive correlation with churn).

### 4. 🤖 Real-Time Churn Predictor
- Predict individual churn probability using a selection of machine learning models:
  - **Random Forest (Recommended)**
  - **Logistic Regression**
  - **Decision Tree**
- Actions-oriented predictions: Categorized as **Low Risk** (Strategy suggestions provided) or **High Risk** (Customized retention action plans generated based on customer characteristics).

---

## 🔬 Model Performance Comparison

Calculated on a holdout test set (20% of the dataset):

| Model | Accuracy | Precision | Recall | F1-Score | Verdict |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Random Forest** | **86.65%** | **76.47%** | 46.31% | **57.68%** | **🏆 Best Overall Model (Selected by default)** |
| **Decision Tree** | 78.40% | 45.49% | **50.12%** | 47.69% | High recall but excessive False Positives (236) |
| **Logistic Regression** | 81.10% | 55.24% | 20.10% | 29.48% | Poor recall (fails to capture 80% of churn cases) |

---

## 🚀 Installation & Setup

Follow these steps to run the application locally on your machine.

### 1. Clone the Repository
```bash
git clone https://github.com/Zain-Khan-AI/Multistate-Bank-Customer-Churn-Detection.git
cd Multistate-Bank-Customer-Churn-Detection
```

### 2. Setup Virtual Environment (Recommended)
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Dashboard
```bash
streamlit run app.py
```

---

## 📂 Project Structure

```
├── bank customer churn models/    # Pre-trained ML Models & Scaler
│   ├── decision_tree_model.pkl
│   ├── logistic_regression_model.pkl
│   ├── random_forest_model.pkl
│   └── scaler.pkl
├── app.py                         # Streamlit Dashboard & Interface code
├── Bank_Customer_Churn_Analaysis_Prediction.ipynb # Model Training Notebook
├── requirements.txt               # Dependencies list
├── .gitignore                     # Config files & Dataset exclusions
└── README.md                      # Project Documentation
```
## 🌐 Live Demo
https://multistate-bank-customer-churn-detection.streamlit.app/
---

## 💡 Key Business Insights & Recommendations
- **German Regional Service Audit:** German customers churn at **32.4%**, which is double France (16.2%) and Spain (16.7%). Audit local services, fee structures, or regional competitor pricing.
- **Product Package Limits:** Holding 3 or 4 products results in an attrition rate exceeding **80%** (100% for 4 products). Review pricing pressure on multi-product customers.
- **Target Inactive Members:** Inactive members churn at **26.9%** compared to active members at **14.3%**. Focus engagement rewards on inactive clients.
- **VIP Accounts for 45-60 Age Group:** Attrition peaks between ages 45-60 at **56.2%**. Design specialized retirement wealth packages to retain mature depositors.

---

Developed with ❤️ by **[Zain Khan](https://github.com/Zain-Khan-AI)**
