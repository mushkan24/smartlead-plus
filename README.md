# SmartLead+ – AI-Powered Trust & Priority Scoring Tool

SmartLead+ is a data-driven lead scoring application that helps businesses **evaluate trustworthiness** and **prioritize leads** for outreach. Built using machine learning and a clean Streamlit UI, the tool allows users to filter, search, and download their highest-value leads based on AI-driven signals.

---

## Demo Video

[Watch the walkthrough]https://www.loom.com/share/0cc4671cc399474aaf094b8b495d2d0f?sid=c841c6ee-615a-4cef-97f9-d22e967a02b7  

---

## Features

- **Trust Scoring** based on domain, email security, and missing data
- **Lead Prioritization** using company size, industry, and trust alignment
- **Search + Filters** for trust level, priority, and keywords
- **Trained ML model** using Random Forest on engineered features
- **Modern dark-themed UI** for smooth analyst experience
- One-click **CSV export** of filtered leads

---

## Tech Stack

- **Frontend/UI**: Streamlit (Python)
- **ML Backend**: Scikit-learn (Random Forest Classifier)
- **Data Handling**: pandas, joblib
- **Visualization**: matplotlib, seaborn

---

## Project Structure

smartlead_ai_trust_validator/

├── app/ # Streamlit app

├── data/ # Raw & processed datasets

├── models/ # Saved trust_model.pkl

├── notebooks/ # Jupyter notebook for training

├── src/ # Feature extraction, scoring utils

├── report.pdf # 1-page summary report

├── requirements.txt # Python dependencies

└── README.md # You're reading it!

---

## Setup Instructions

> Make sure Python 3.10+ is installed. Create a virtual environment (recommended).

### 1. Clone this Repository

git clone https://github.com/yourusername/smartlead-plus.git
cd smartlead-plus

### 2. Create a Virtual Environment
python -m venv venv

source venv/bin/activate        # On Mac/Linux

venv\Scripts\activate           # On Windows

### 3. Install Requirements
pip install -r requirements.txt

### 4. Run the App
streamlit run app/app.py

### ML Model Training
To retrain the trust model:

jupyter notebook notebooks/trust_model_training.ipynb

•	Saves model to: models/trust_model.pkl

•	You can replace it in the app without any code change.

### Sample Output (UI)
| Name        | Email                                       | TrustScore | TrustLevel | PriorityLevel |
| ----------- | ------------------------------------------- | ---------- | ---------- | ------------- |
| Sarah James | [sarah@legit.io](mailto:sarah@legit.io)     | 92         | High Trust |  High       |
| Mike Dev    | [mike@unknown.biz](mailto:mike@unknown.biz) | 40         | Low Trust  |  Low        |


This project is for educational/demo purposes as part of a submission to Caprae Capital.
All code is original unless otherwise mentioned.
