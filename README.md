# 📊 GaSa Books Sales Analysis

Analysis of Amazon book sales based on exported marketplace data, enriched with own-channel activity to investigate **sales cannibalization** and **seasonality patterns**.

---

## 🚀 Project Overview

This project analyzes book sales from Amazon and compares them with activity from an independent sales channel.

### Goals:
- 📈 Understand sales distribution across products and regions  
- 🔍 Detect potential **cannibalization effects** between Amazon and own sales channel  
- 🕒 Analyze **seasonality trends** (monthly & quarterly)  
- 📊 Build a compact visual dashboard summarizing key insights  

---

### Dashboard:
![Matlib and pandas dashboard](./reports/figures/dashboard.png)

---

## 🧠 Key Questions

- Does running my own sales channel reduce Amazon sales?
- Which products sell best?
- Which regions generate the most sales?
- Are there seasonal patterns in sales?


---

## 📦 Data Sources

### 1. Amazon Sales (`amazon_sales.csv`)

Columns:
- `Date`
- `Title`
- `ASIN`
- `Marketplace`
- `Units`

### 2. Own Channel Activity (`own_channel_activity.csv`)

Columns:
- `Miesiac` (Month)
- `JDG` (activity flag)

---

## ⚙️ Data Pipeline
Loader → Cleaner → Analyzer → Visualizer

### 1. Loader

- Loads CSV files
- Validates schema
- Handles file errors

### 2. Cleaner

- Standardizes column names
- Converts data types
- Handles missing values
- Merges Amazon sales with own-channel activity

### 3. Analyzer

Responsible for business logic:
- KPI calculations
- Aggregations:
  - by product
  - by region
  - by month
- Cannibalization analysis (Amazon vs own channel)
- Seasonality analysis (quarter-based)

### 4. Visualizer

- Generates a single dashboard (`.png`)
- Combines all insights into one view

---

## 📊 Output

The pipeline generates a dashboard:
reports/figures/dashboard.png

Dashboard includes:
- Key metrics
- Top-selling products
- Sales by region
- Monthly trend
- Quarterly seasonality
- Amazon vs own-channel comparison

---

## 📈 Example Insights

- One product dominates total sales
- Majority of sales comes from a single region
- Sales fluctuate monthly with visible peaks
- When own channel is **inactive**, Amazon sales are higher → possible cannibalization effect

---

## 🛠️ How to Run

### 1. Install dependencies
pip install -r requirements.txt

### 2. Run pipeline
python main.py

### 3. Check output
reports/figures/dashboard.png


## 💡 Design Decisions

- Clear separation of concerns (Loader / Cleaner / Analyzer / Visualizer)
- Defensive programming (schema validation, error handling)
- Simple and readable Pandas transformations
- Reproducible pipeline

---

## 🔮 Possible Improvements

- Add unit tests (pytest)
- Export results to CSV / JSON
- Replace static plots with interactive dashboard (Plotly / Streamlit)

---

## 👩‍💻 Author

Marta Mucha-Balcerek

Project created as part of portfolio and real-world sales analysis.
