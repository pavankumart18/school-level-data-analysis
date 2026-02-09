
import pandas as pd
import numpy as np

# Load Data
try:
    xl = pd.ExcelFile('School Level Data.xlsx')
    df = pd.read_excel(xl, sheet_name=0)
except Exception as e:
    print(f"Error loading Excel: {e}")
    exit()

t_col = 'enquiries_started'
s_col = 'StudentFTE'

if t_col not in df.columns or s_col not in df.columns:
    print(f"Missing columns: {t_col} or {s_col}")
    exit()

# Handle numeric
df[t_col] = pd.to_numeric(df[t_col], errors='coerce')
df[s_col] = pd.to_numeric(df[s_col], errors='coerce')

# Filter
df = df.dropna(subset=[t_col, s_col])
df = df[df[s_col] > 10] # Filter very small schools

# Calculate Rate
df['Rate'] = df[t_col] / df[s_col]

print(f"Calculated Rate for {len(df)} schools.")
print(f"Mean Rate: {df['Rate'].mean():.4f}")

# Select numeric
numeric_df = df.select_dtypes(include=[np.number])

# Spearman Correlation with Rate
corr = numeric_df.corr(method='spearman')['Rate'].sort_values(ascending=False)

print("\n--- TOP POSITIVE DRIVERS of Enquiry/Student ---")
print(corr.head(15))

print("\n--- TOP NEGATIVE DRIVERS of Enquiry/Student ---")
print(corr.tail(15))

# Check Categorical Drivers
cat_cols = ['Region', 'Level', 'Type'] # Guessing names, checking actuals
for c in df.columns:
    if df[c].dtype == 'object' and df[c].nunique() < 15:
        print(f"\n--- {c} Mean Rate ---")
        print(df.groupby(c)['Rate'].mean().sort_values(ascending=False))
