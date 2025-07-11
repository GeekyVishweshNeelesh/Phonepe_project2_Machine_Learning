# 📊 PhonePe Pulse Data Analysis & Machine Learning Project

This project leverages PhonePe's publicly available Pulse data to uncover business insights, perform exploratory data analysis, and build machine learning models for use cases like customer segmentation, fraud detection, trend forecasting, and state-wise performance benchmarking.

---

## 📁 GitHub Repository

👉 [PhonePe Pulse Data Source](https://github.com/PhonePe/pulse)

Visit the Streamlit Dashboard from here:

👉 https://streamapppy-ml.streamlit.app/
---

## 🚀 Project Highlights

- ✅ Converted raw JSON data from GitHub into structured CSV format (9 datasets across Aggregated, Map, and Top categories).
- 🧼 Performed comprehensive data cleaning, wrangling, and transformation using Python (Pandas, NumPy).
- 📈 Created visualisations to understand transaction trends, user growth, brand penetration, and regional usage.
- 🔬 Performed Hypothesis Testing using ANOVA and Pearson Correlation to validate assumptions.
- 🤖 Built ML Models for:
  - **Customer Segmentation** (KMeans Clustering)
  - **Fraud Detection** (Z-Score, Isolation Forest)
  - **Performance Classification** (Random Forest Classifier)
  - **Time Series Trend Analysis** (Prophet, Line Graphs)
- 📌 Included feature importance interpretation and model explainability for actionable business insights.

---

## 📚 Datasets Used

Converted into CSV format from [PhonePe Pulse Repository](https://github.com/PhonePe/pulse/tree/master/data):

1. `aggregated_user.csv`
2. `aggregated_transaction.csv`
3. `aggregated_insurance.csv`
4. `map_user.csv`
5. `map_transaction.csv`
6. `map_insurance.csv`
7. `top_user.csv`
8. `top_transaction.csv`
9. `top_insurance.csv`

---

## 🔧 Tools & Libraries

- **Languages:** Python 3
- **Libraries:**  
  `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`, `scipy`, `statsmodels`, `plotly`, `prophet`, `streamlit`

---

## 📊 Key Visualizations

- Bar charts of state-wise transaction volume
- Line graphs of transaction trends over quarters
- Pie charts of brand share among PhonePe users
- Scatter plots and pair plots for relational analysis
- Heatmaps and confusion matrices for ML evaluation

---

## 🧠 Machine Learning Models

| Use Case                | Datasets Used               | ML Method             |
|-------------------------|-----------------------------|------------------------|
| Customer Segmentation   | aggregated_user, top_user   | KMeans Clustering      |
| Fraud Detection         | aggregated_transaction      | Z-Score, IsolationForest |
| State Classification    | aggregated_transaction      | Random Forest Classifier |
| Insurance Insights      | aggregated_insurance        | Trend Comparison Charts |

---

## 📈 Performance Summary

- **Random Forest Classifier Accuracy:** ~88%
- **Improved F1-Score for Medium class after tuning**
- **Cluster Profiles:** Clear separation of user behaviour across states
- **Hypothesis Testing Results:** All p-values < 0.05 showed statistically significant insights

---

## 📦 Project Structure

```bash
📁 PhonePe-Pulse-ML-Analysis/
├── data/
│   ├── aggregated_user.csv
│   ├── ...
├── notebooks/
│   └── Phonepe_project.ipynb
├── app/
│   └── streamlit_dashboard.py
├── README.md
