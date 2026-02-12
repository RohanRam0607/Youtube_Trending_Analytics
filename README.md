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

## 📁 Project Structure

```bash
Youtube_Trending_Analytics/
│
├── .github/
│   └── workflows/
│       └── ci.yml                  # (Optional) GitHub Actions CI pipeline
│
├── .streamlit/
│   └── config.toml                 # Streamlit configuration (NOT secrets)
│
├── app/
│   ├── __init__.py
│   ├── main.py                     # Streamlit entry point
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   └── components.py           # UI components
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── model_service.py        # Model loading logic
│   │   └── prediction_service.py   # Prediction pipeline
│   │
│   └── utils/
│       ├── __init__.py
│       └── helpers.py              # Utility/helper functions
│
├── models/
│   ├── random_forest_model.pkl     # Trained ML model
│   └── scaler.pkl                  # Feature scaler
│
├── scripts/
│   └── train_model.py              # Model training script
│
├── tests/
│   └── test_model.py               # Unit tests
│
├── .gitignore
├── README.md
├── requirements.txt
└── pyproject.toml                  # (Recommended) Modern Python configuration
```
