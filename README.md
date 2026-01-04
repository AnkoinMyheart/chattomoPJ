#  Chattomo Mini – Visualizing the Heart × Python AI × Power Platform

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![PowerBI](https://img.shields.io/badge/PowerBI-Analytics-yellow)
![Status](https://img.shields.io/badge/Status-Development-orange)

---

##  Overview
Chattomo Mini is a **lightweight emotional-support AI assistant** that:
- Receives your daily feelings
- Evaluates emotional mood score
- Detects mental trends
- Visualizes emotions via Power BI

No external AI APIs.  
Everything runs **locally + free** to demonstrate real engineering skills.

---

##  Key Features
-  English & Japanese mood detection
-  Mood score (-3 ~ +3)
-  Emotional tagging (work / sleep / people / love / future …)
-  CSV logging
-  Power BI dashboards
-  Designed for portfolio & interview demonstration

---
##  System Architecture

The Chattomo Mini ecosystem is built using a lightweight but fully functional architecture:

![architecture](./images/architecture.png)


**Flow:**

1. **Power Automate (Reminder)**  
   - Sends daily reminder emails to encourage mood input


2. **Power Apps**  
   - Provides the mood input UI  
   - Displays responses returned from Chattomo  
   - Allows users to view Power BI dashboards (optional)


3. **Power Automate (Orchestration)**  
   - Receives input from Power Apps  
   - Sends HTTP requests to the FastAPI backend  
   - Returns analysis results back to Power Apps


4. **FastAPI (Python Backend)**  
   - Acts as the API layer  
   - Processes mood input using Python logic  
   - Returns mood label, mood score, and response text


5. **CSV Storage**  
   - Stores mood logs  
   - Serves as the data source for Power BI


6. **Power BI**  
   - Visualizes moods and emotional trends

---

##  Power BI Dashboards
### 1. Daily Dashboard
![PowerBI-Daily](./images/TodaysFeeling.png)

**Purpose**:
Provide a clear snapshot of today’s emotional state.

**Highlights**
- Automatically displays today’s entry using DAX logic
- Shows Mood Score, Mood Label, Main Tag, Comment, and 7-day Average
- Dynamic emoji changes based on mood label
- Clean card-based UI designed for readability
- Uses calculated columns (DateOnly, MoodScoreToday, MoodSummary)

### 2. Mood Trend
![PowerBI-Trend](./images/MoodTrend.png)

**Purpose**:
Track mood fluctuations over the recent period.

**Highlights**
- Default view fixed to last 30 days for clarity
- Line chart visualizes day-to-day mood changes
- Supports filtering by Mood Label and custom date range
- Average score card summarizes overall trend
- DateOnly column ensures clean, chronological X-axis

### 3. Topic Analysis

![PowerBI-Analysis](./images/TopicAnalysis.png)

**Purpose**:
Track mood fluctuations over the recent period.

**Highlights**
- Horizontal bar chart shows tag frequency
- Heatmap visualizes tag × mood_score relationships
- Dynamic Top 3 Tags extracted with RANKX
- Aggregations and color logic handled in DAX
- Useful for identifying emotional triggers and main focus areas

---

##  Tech Stack
- Python 3.10
- FastAPI
- CSV storage
- Power BI Desktop

---

##  API Example
Below is a simple request/response example.

```json
POST /analyze
{
  "mood_text": "happy",
  "comment": "Great day today!",
  "user_id": "Anko"
}

{
  "mood_label": "happy",
  "mood_score": 2,
  "tags": ["general"],
  "comment": "Love this mood! ..."
}