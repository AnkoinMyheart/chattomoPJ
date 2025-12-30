# 🧠 Chattomo Mini – 可視化する心 × Python AI × Power Platform

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![PowerBI](https://img.shields.io/badge/PowerBI-Analytics-yellow)
![Status](https://img.shields.io/badge/Status-Development-orange)

---

## 🌟 Overview
Chattomo Mini is a **lightweight emotional-support AI assistant** that:
- Receives your daily feelings
- Evaluates emotional mood score
- Detects mental trends
- Visualizes emotions via Power BI

No external AI APIs.  
Everything runs **locally + free** to demonstrate real engineering skills.

---

## 🏗 Architecture



---

## ✨ Key Features
- ✔️ English & Japanese mood detection
- ✔️ Mood score (-3 ~ +3)
- ✔️ Emotional tagging (work / sleep / people / love / future …)
- ✔️ CSV logging
- ✔️ Power BI dashboards
- ✔️ Designed for portfolio & interview demonstration

---

## 📊 Power BI Dashboards
- 📈 Mood Trend (daily / monthly)
- 🎯 Today Dashboard
- 🔎 Topic / Stress Analysis Heatmap

---

## 🚀 Tech Stack
- Python 3.10
- FastAPI
- CSV storage
- Power BI Desktop

---

## 🧪 API Example
```json
POST /analyze
{
  "mood_text": "happy",
  "comment": "Great day today!",
  "user_id": "honoka"
}

{
  "mood_label": "happy",
  "mood_score": 2,
  "tags": ["general"],
  "comment": "Love this mood! ..."
}
