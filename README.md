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
- Initial analysis suggested higher Amazon sales when the own channel was inactive. However, after  correcting for missing time periods and controlling for seasonality, this effect was no longer consistent.
This indicates that the observed differences are likely driven by external factors (e.g. seasonality or growth trends) rather than direct cannibalization between channels.

---

## ⚠️ Analytical Caveats

During development, a key issue was identified:

- Early analysis excluded months with no Amazon sales
- This introduced **survivorship bias**, significantly distorting results

To address this:
- A full monthly timeline was reconstructed using own-channel activity data
- Missing sales were treated as zero (not missing)

Additionally:
- A normalized KPI was introduced to control for seasonality

This highlights the importance of:
- validating assumptions behind the data  
- distinguishing correlation from causation  

---

## 🛠️ How to Run

### 1. Install dependencies
pip install -r requirements.txt

### 2. Run pipeline
python main.py

### 3. Check output
reports/figures/dashboard.png

---

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
