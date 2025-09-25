# alzheimers-risk-prediction
Alzheimer’s Risk Prediction using Ensemble Learning (Random Forest, XGBoost, Gradient Boosting, Stacking) with 96% accuracy, integrated with gamified cognitive testing and GenAI-powered personalized recommendations via a Flask web app.
# Alzheimer’s Risk Prediction with GenAI Recommendations

## 📌 Project Overview
This project focuses on **early detection of Alzheimer’s disease** using ensemble machine learning models combined with a **Flask-based web application**.  
It integrates **gamified cognitive testing** and a **GenAI-powered personalized recommendation system** to assist patients, caregivers, and healthcare professionals.  

## 🚀 Features
- Alzheimer’s risk classification: **Healthy, Mild Cognitive Impairment (MCI), Alzheimer’s**
- Ensemble models: **Random Forest, XGBoost, Gradient Boosting, Stacking**
- **96% prediction accuracy** on Kaggle Alzheimer’s dataset
- **Gamified cognitive test module** for early detection
- **GenAI-powered recommendation system** generating personalized health guidance
- **Caregiver Mode** for patient profile management and secure result storage

## 🛠️ Tech Stack
- **Python**, **scikit-learn**, **XGBoost**, **Pandas**
- **Flask** (web app), **SQLite** (database)
- **GenAI (LLM integration)** for recommendations

## 📂 Dataset
[Kaggle Alzheimer’s Dataset](https://www.kaggle.com/datasets/rabieelkharoua/alzheimers-disease-dataset)

## 🎯 Outcomes
- Accurate, explainable Alzheimer’s detection
- User-friendly interface for patients & caregivers
- Personalized lifestyle and health recommendations powered by GenAI

ALZHEIMER_APP/
│
├── static/
│   └── style.css
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── index.html
│   ├── login.html
│   ├── memory_game.html
│   ├── reaction_game.html
│   ├── result.html
│   └── signup.html
│
├── app.py                # Flask main app
├── setup_db.py           # Script to initialize database
├── users.db              # SQLite DB (⚠️ better keep this in .gitignore)
├── stacked_model.pkl     # Trained ML model
├── column_order.pkl      # Preprocessing artifact
├── label_encoder.pkl     # Encoder artifact
├── requirements.txt      # Dependencies (generate with pip freeze)
├── README.md             # Project overview
└── .gitignore            # Ignore unnecessary files
