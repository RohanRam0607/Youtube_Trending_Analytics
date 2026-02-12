# 📊 YouTube Trending Analytics Dashboard

A professional **data analytics and machine learning dashboard** that analyzes **real‑time YouTube trending videos**, visualizes growth patterns, and predicts engagement potential using machine learning.

🔗 **Live App:**  
https://youtubetrendinganalytics-ucjm8jek7grxktmnulduqc.streamlit.app/

---

## 🚀 Features

- 🔴 **Real‑time YouTube Trending Data** using YouTube Data API  
- 📈 **View Velocity & Growth Analysis**
- 📊 Interactive analytics & visualizations
- 🤖 **Machine Learning Predictions** (High / Low Engagement)
- 🔗 Clickable video titles (opens YouTube directly)
- 🔐 Secure API key handling using Streamlit Secrets
- 🎨 Modern, professional UI built with Streamlit

---

## 🧠 Machine Learning Details

- **Algorithm Used:** Random Forest Classifier  
- **Preprocessing:** StandardScaler  
- **Prediction Task:**  
  Predict whether a trending video has **HIGH** or **LOW** engagement potential.

### Features used for prediction:
- Video age (days)
- Title length
- Title word count
- Number of tags

---

## 🛠️ Tech Stack

- **Frontend / UI:** Streamlit  
- **Backend Logic:** Python  
- **Machine Learning:** scikit‑learn  
- **Data Source:** YouTube Data API v3  
- **Deployment:** Streamlit Cloud  
- **Version Control:** GitHub  

---

## 📂 Project Structure

yt-project/
│
├── .github/
│   └── workflows/
│       └── ci.yml                # (optional) GitHub Actions CI
│
├── .streamlit/
│   └── config.toml               # Streamlit config (NOT secrets)
│
├── app/
│   ├── __init__.py
│   ├── main.py                   # Streamlit entry point (renamed from app.py)
│   ├── ui/
│   │   ├── __init__.py
│   │   └── components.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── model_service.py
│   │   └── prediction_service.py
│   │
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
│
├── models/
│   ├── random_forest_model.pkl
│   └── scaler.pkl
│
├── scripts/
│   └── train_model.py            # renamed from train_model_api.py
│
├── tests/
│   └── test_model.py
│
├── .gitignore
├── README.md
├── requirements.txt
├── setup.py (optional)
└── pyproject.toml (recommended modern approach)
