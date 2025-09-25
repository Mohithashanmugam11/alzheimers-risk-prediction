# alzheimers-risk-prediction
Alzheimer’s Risk Prediction using Ensemble Learning (Random Forest, XGBoost, Gradient Boosting, Stacking) with 96% accuracy, integrated with gamified cognitive testing and GenAI-powered personalized recommendations via a Flask web app.
# Alzheimer’s Risk Prediction with GenAI Recommendations

## 📌 Project Overview
This project focuses on **early detection of Alzheimer’s disease** using ensemble machine learning models combined with a **Flask-based web application**.  
It integrates **gamified cognitive testing** and a **GenAI-powered personalized recommendation system** to assist patients, caregivers, and healthcare professionals.  

## 🚀 FeaturesPerfect 👍 Here’s the full README.md content in code format so you can directly copy-paste into your repo:

# 🧠 Alzheimer’s Risk Prediction with GenAI Recommendations

## 📌 Project Overview
This project aims at **early detection of Alzheimer’s disease** using **ensemble machine learning models** combined with a **Flask-based web application**.  
It integrates **gamified cognitive testing** and a **GenAI-powered personalized recommendation system** to assist patients, caregivers, and healthcare professionals.  

## 🚀 Features
- Predicts Alzheimer’s risk levels: **Healthy**, **Mild Cognitive Impairment (MCI)**, **Alzheimer’s**  
- Ensemble models: **Random Forest, XGBoost, Gradient Boosting, Stacking**  
- Achieved **96% accuracy** on the Kaggle Alzheimer’s dataset  
- **Gamified cognitive tests** (memory & reaction games) for early screening  
- **GenAI-powered recommendation module** that generates natural-language health and lifestyle advice  
- **Caregiver Mode** for managing multiple patient profiles and securely storing results  

## 🛠️ Tech Stack
- **Python**, **Flask**, **SQLite**
- **scikit-learn**, **XGBoost**, **Pandas**
- **GenAI (LLM integration)**
- **HTML, CSS (static/templates)**

## 📂 Project Structure


ALZHEIMER_APP/
1.static/style.css
2.templates/
base.html
dashboard.html
index.html
login.html
memory_game.html
reaction_game.html
result.html
signup.html

3.app.py # Flask main app
setup_db.py # Script to initialize database
users.db # SQLite DB (⚠️ ignored in .gitignore for privacy)
stacked_model.pkl # Trained ML model
column_order.pkl # Preprocessing artifact
label_encoder.pkl # Encoder artifact
requirements.txt # Dependencies
README.md # Project overview
.gitignore # Ignore unnecessary files


## 📦 Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/alzheimers-risk-prediction.git
   cd alzheimers-risk-prediction/ALZHEIMER_APP


Create and activate virtual environment:

python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows


Install dependencies:

pip install -r requirements.txt


Setup the database (if needed):

python setup_db.py


Run the Flask app:

python app.py


Open in browser:

http://127.0.0.1:5000/

📊 Dataset

Kaggle Alzheimer’s Dataset

~90,000 patient records

37+ attributes: demographics, lifestyle habits, medical history, cognitive assessments

🎯 Outcomes

Accurate Alzheimer’s risk classification with 96% accuracy

Personalized AI-driven recommendations for patients and caregivers

User-friendly web platform combining diagnosis, cognitive games, and decision support

📌 Future Scope

Deeper integration with Explainable AI (SHAP, LIME)

More interactive GenAI chatbot for patients & caregivers

Support for larger, real-world medical datasets
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
