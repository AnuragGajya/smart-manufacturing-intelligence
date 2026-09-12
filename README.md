# 🏭 Smart Manufacturing Intelligence System

> Real-time Predictive Maintenance Dashboard with ML & Automation

---

## 📌 Overview

Smart Manufacturing Intelligence System is an end-to-end
predictive maintenance solution built for electronics and
manufacturing companies. It uses Machine Learning to predict
machine failures in real-time, sends automated alerts, and
displays live insights on an interactive dashboard.

Built by **Anurag Gajya** — Electronics Data Analyst |
BSc Electronics (Hons) + CS Minor | Delhi University

---

## 🚀 Live Demo

👉 [Click here to view live dashboard](https://your-app.streamlit.app)

---

## ✨ Features

- 📊 **Real-time Dashboard** — Auto-refreshes every 3 seconds
- 🤖 **ML Predictions** — XGBoost model with 96% accuracy
- 🔴 **Risk Classification** — High / Medium / Low risk levels
- 🌡️ **Live Temperature Monitoring** — Real-time trend charts
- ⚙️ **Manual Prediction** — Sidebar input for instant prediction
- 📧 **Automated Email Alerts** — High risk machine notifications
- 📱 **Telegram Bot Alerts** — Instant mobile notifications
- 📋 **Excel Report Generator** — Daily automated reports
- ⏰ **Scheduler** — Runs predictions every 6 hours automatically
- 💰 **Financial Impact Calculator** — ROI analysis

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| Language | Python |
| ML Models | XGBoost, Random Forest, Scikit-learn |
| Dashboard | Streamlit, Plotly |
| Data | Pandas, NumPy |
| Automation | Schedule, smtplib, Telegram Bot |
| Reports | openpyxl |
| Deployment | Streamlit Cloud |

---

## 📁 Project Structure

```
smart_manufacturing_dashboard/
│
├── app.py                 # Streamlit dashboard
├── best_model.pkl         # Trained ML model
├── data_scaler.pkl        # Feature scaler
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

---

## ⚙️ Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/smart-manufacturing-intelligence.git
cd smart-manufacturing-intelligence
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Dashboard
```bash
streamlit run app.py
```

### 4. Open in Browser
```
http://localhost:8501
```

---

## 🤖 ML Model Details

| Metric | Value |
|---|---|
| Best Model | XGBoost Classifier |
| Accuracy | 96% |
| AUC Score | 0.98 |
| Features | 9 (including engineered) |
| Training Data | 10,000+ sensor records |
| Class Imbalance | Handled with SMOTE |

### Features Used
- Air Temperature (K)
- Process Temperature (K)
- Rotational Speed (RPM)
- Torque (Nm)
- Tool Wear (min)
- Temperature Difference (engineered)
- Power (engineered)
- Tool Wear Rate (engineered)
- Machine Type (encoded)

---

## 📊 Dataset

**Source:** Machine Predictive Maintenance Classification
**Platform:** Kaggle
**Records:** 10,000+
**Link:** [Kaggle Dataset](https://www.kaggle.com/datasets/shivamb/machine-predictive-maintenance-classification)

---

## 🔄 How Automation Works

```
Factory Sensors
      ↓
Data Collection (CSV/API)
      ↓
Prediction Pipeline (Every 6 hours)
→ Load Model
→ Run Predictions
→ Save Results CSV
→ Send Email + Telegram Alerts
→ Generate Excel Report
      ↓
Streamlit Dashboard (Every 3 seconds)
→ Read Latest Data
→ Update Charts
→ Show Live Alerts
      ↓
Manager sees real-time insights
```

---

## 💰 Financial Impact

This system can save manufacturing companies:
- **₹2M+** annually through early failure detection
- **96%** of machine failures detected before they occur
- **Reduced downtime** through predictive scheduling
- **Lower maintenance costs** through planned interventions

---

## 🎯 Business Value

| Without System | With System |
|---|---|
| Reactive maintenance | Predictive maintenance |
| Unknown failure timing | 96% prediction accuracy |
| High downtime costs | Reduced unplanned downtime |
| Manual monitoring | Automated 24/7 monitoring |
| No financial tracking | ROI calculator included |

---

## 📸 Screenshots

### Live Dashboard
![Dashboard](screenshots/dashboard.png)

### Risk Distribution
![Risk](screenshots/risk_chart.png)

### Machine Status Table
![Status](screenshots/machine_status.png)

---

## 👨‍💻 About the Author

**Anurag Gajya**
- 🎓 BSc Electronics (Hons) + CS Minor — Delhi University
- 💼 Electronics Data Analyst
- 🔧 Robotics Enthusiast
- 📊 Skills: SQL · Python · Power BI · ML · Electronics

**Connect:**
- LinkedIn: [linkedin.com/in/anurag-gajya](https://linkedin.com/in/anurag-gajya)
- GitHub: [github.com/anurag-gajya](https://github.com/anurag-gajya)

---

## 📄 License

This project is open source and available under the MIT License.

---

⭐ **If this project helped you, please give it a star!**
