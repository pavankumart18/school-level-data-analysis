
import pandas as pd
import numpy as np

# Load the data
df = pd.read_excel('School Level Data.xlsx')

# Filter for latest year (assuming 2024 based on previous context)
df_24 = df[df['FiscalYear'] == 2024]

print(f"--- Data Summary for 2024 (n={len(df_24)}) ---")
print(f"Total Student FTE: {df_24['StudentFTE'].sum():,.0f}")
print(f"Total Enquiries: {df_24['enquiries_started'].sum():,.0f}")
print(f"Total Applications: {df_24['App'].sum():,.0f}" if 'App' in df.columns else "App column missing")

# Correlation Matrix (Key Strategic Variables)
cols = ['StudentFTE', 'enquiries_started', 'App', 'NAE_Overall_Average_Fee_USD', 'nps_score', 'Teachers_Attrition_Pct']
existing_cols = [c for c in cols if c in df.columns]

print("\n--- Correlation Matrix (Spearman) ---")
corr = df_24[existing_cols].corr(method='spearman')
print(corr)

# Check the 'Rate' (Enquiries per Student)
df_24 = df_24.copy()
df_24['Rate'] = df_24['enquiries_started'] / df_24['StudentFTE']
print(f"\nGlobal Mean Rate: {df_24['Rate'].mean():.2f}")

# Region Check
if 'Region' in df.columns:
    print("\n--- Mean Rate by Region ---")
    print(df_24.groupby('Region')['Rate'].mean().sort_values(ascending=False))
