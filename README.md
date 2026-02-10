# School-Level Data Analysis

A comprehensive exploratory data analysis (EDA) and strategic dashboard for school enrollment trends, demand drivers, and operational efficiencies.

## 📊 Project Overview

This project analyzes data from **503 school-year records** to identify the primary drivers of enquiry volume and enrollment growth. The findings are presented through high-end interactive visualizations, including a strategic heatmap, scrollytelling narrative, and automated hypothesis testing.

### Key Analysis Artefacts:
*   **[index.html](index.html)**: The primary Executive Dashboard featuring a Strategic Map Heatmap, Regional Bar Charts, and Cluster Analysis.
*   **[hypothesis.html](hypothesis.html)**: A "New York Times" style immersive analysis using scrollytelling to test 20 different hypotheses against real institutional data.
*   **[leaderboard.html](leaderboard.html)**: Institutional performance rankings across key metrics (Enquiries, NPS, Conversion).

## 🚀 Key Strategic Findings

The analysis reveals three distinct operational realities:

1.  **The Volume Driver (Scale Effect)**: School scale is the strongest predictor of demand ($\rho = 0.83$). Large schools generate their own gravity through market presence and word-of-mouth momentum.
2.  **The Pricing Sensitivity**: Higher fees act as a volume constraint ($\rho = -0.22$) in competitive markets, indicating mass-premium price sensitivity.
3.  **The Quality Paradox (NPS)**: While NPS is critical for retention, it shows only a modest correlation ($\rho = 0.25$) with *immediate* enquiry volume, confirming quality as a long-term reputation play.

## 🛠️ Data Infrastructure

*   **Verified Integrity**: All correlation coefficients and means are hard-grounded in Pearson $r$ calculations computed from the source CSV.
*   **Real-Data Visualization**: Scatter plots and interactive elements use **actual anonymized samples** from the dataset, not synthetic distributions.
*   **Dynamic Significance**: Hypotheses are automatically tiered based on statistical significance ($p$-values) and effect size.

## 💻 Running Locally

To view the interactive reports, serve the directory using a local web server:

```bash
# Using Python
python -m http.server 8080

# Or using Node.js
npx serve .
```

Navigate to `http://localhost:8080` to access the dashboard.

## 📂 Project Structure

*   `School Level Data.csv`: The source dataset.
*   `extract_samples.py`: Script to generate representative data samples for visualizations.
*   `verify_data.py`: Comprehensive audit script to cross-reference HTML claims against CSV truth.
*   `ACTIONABLE_REPORT.md`: Summary of strategic Recommendations based on the analysis.
