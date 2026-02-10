"""
Generate aligned data values from CSV for use in HTML dashboards.
This script calculates actual statistics from the randomized CSV
and outputs JavaScript arrays that can be pasted into the HTML files.
"""
import pandas as pd
import numpy as np
from scipy import stats

# Load data
df = pd.read_csv('School Level Data.csv')
print("Loaded", len(df), "rows")
print()

# Calculate Rate (key metric for hypothesis testing)
df['rate'] = df['enquiries_started'] / df['StudentFTE']
df['utilization'] = (df['StudentFTE'] / df['CapacityFTE']) * 100

print("=" * 70)
print("COPY THESE VALUES INTO index.html")
print("=" * 70)
print()

# 1. Trend Data
print("// trendData - Total StudentFTE by year")
print("const trendData = [")
trend = df.groupby('FiscalYear')['StudentFTE'].sum().sort_index()
for yr, val in trend.items():
    if pd.notna(yr):
        print(f'    {{ year: "FY{int(yr)}", value: {int(val)} }},')
print("];")
print()

# 2. Regional Data
print("// regionsData - Average rate by region")
print("const regionsData = [")
regional = df.groupby('Region')['rate'].mean().sort_values(ascending=False)
for reg, val in regional.items():
    if pd.notna(val) and val > 0:
        print(f'    {{ name: "{reg}", value: {val:.2f} }},')
print("];")
print()

# 3. Correlation Data (drivers)
print("// driversData - Correlation with enquiries_started")
print("const driversData = [")
correlations = []
metrics = [
    ('leads_submitted', 'Leads Intensity'),
    ('NAE_Overall_Average_Fee_USD', 'Fees (Average)'),
    ('StudentFTE', 'Student FTE (Size)'),
    ('nps_score', 'NPS Score'),
    ('nps_responses_count', 'NPS Response Count'),
    ('Teachers_Attrition_Pct', 'Teacher Attrition')
]
for col, name in metrics:
    valid = df[[col, 'enquiries_started']].dropna()
    if len(valid) > 10:
        rho, p = stats.spearmanr(valid[col], valid['enquiries_started'])
        correlations.append((name, rho))

# Sort by absolute value
correlations.sort(key=lambda x: abs(x[1]), reverse=True)
for name, rho in correlations:
    print(f'    {{ name: "{name}", r: {rho:.2f} }},')
print("];")
print()

# 4. Utilization Distribution
print("// utilizationData - Histogram of utilization rates")
print("const utilizationData = [")
bins = [(10, 20), (20, 30), (30, 40), (40, 50), (50, 60), (60, 70), 
        (70, 80), (80, 90), (90, 100), (100, 110), (110, 200)]
labels = ['10-20%', '20-30%', '30-40%', '40-50%', '50-60%', '60-70%', 
          '70-80%', '80-90%', '90-100%', '100-110%', '110%+']
for (low, high), label in zip(bins, labels):
    count = ((df['utilization'] >= low) & (df['utilization'] < high)).sum()
    print(f'    {{ bin: "{label}", count: {count} }},')
print("];")
print()

print("=" * 70)
print("COPY THESE VALUES INTO hypothesis.html")
print("=" * 70)
print()

# Hypothesis data with correlations
print("// regions array")
print("const regions = [")
for reg, val in regional.items():
    if pd.notna(val) and val > 0:
        safe_reg = reg.replace("&", "&amp;")
        print(f'    {{ name: "{safe_reg}", value: {val:.2f} }},')
print("];")
print()

print("=" * 70)
print("SUMMARY OF ACTUAL VALUES FROM CSV")
print("=" * 70)
print()
print("Total schools:", df['School'].nunique())
print("Total records:", len(df))
print("Years:", sorted(df['FiscalYear'].dropna().unique()))
print()
print("Correlations with enquiries_started:")
for name, rho in correlations:
    print(f"  {name}: rho = {rho:.3f}")
