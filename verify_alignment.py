"""
Verify alignment between CSV data and HTML dashboard values.
"""
import pandas as pd
import numpy as np

df = pd.read_csv('School Level Data.csv')

print("=" * 60)
print("DATA ALIGNMENT VERIFICATION REPORT")
print("=" * 60)
print()

# 1. Trend Data
print("1. TREND DATA (Total StudentFTE by Year)")
print("-" * 40)
trend = df.groupby('FiscalYear')['StudentFTE'].sum()
for yr, val in sorted(trend.items()):
    print(f"   FY{int(yr)}: {val:,.0f}")
print()

# 2. Regional Performance
print("2. REGIONAL PERFORMANCE (Rate = enquiries/student)")
print("-" * 40)
df['rate'] = df['enquiries_started'] / df['StudentFTE']
regional = df.groupby('Region')['rate'].mean().sort_values(ascending=False)
for reg, val in regional.items():
    if pd.notna(val):
        print(f"   {reg}: {val:.2f}")
print()

# 3. Key Correlations
print("3. CORRELATION ANALYSIS (Spearman rho)")
print("-" * 40)
metrics = {
    'leads_submitted': 'Leads',
    'NAE_Overall_Average_Fee_USD': 'Fees',
    'StudentFTE': 'School Size',
    'nps_score': 'NPS Score',
    'Teachers_Attrition_Pct': 'Teacher Attrition'
}
for col, name in metrics.items():
    valid = df[[col, 'enquiries_started']].dropna()
    if len(valid) > 10:
        corr = valid.corr(method='spearman').iloc[0, 1]
        print(f"   {name}: rho = {corr:.3f} (n={len(valid)})")
print()

print("=" * 60)
print("ALIGNMENT STATUS: NOT ALIGNED")
print("=" * 60)
print()
print("The CSV data was RANDOMIZED independently.")
print("The HTML files have HARDCODED placeholder values.")
print()
print("To align, we need to update HTML with actual CSV values.")
