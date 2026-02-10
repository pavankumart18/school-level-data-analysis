"""
Randomize school metrics data in the Excel file.
"""
import pandas as pd
import numpy as np

print("Starting randomization...")

# Set random seed
np.random.seed(2026)

# Load Excel file
df = pd.read_excel('School Level Data.xlsx')
print(f"Loaded {len(df)} rows, {len(df.columns)} columns")

# Columns to preserve
preserve = ['School', 'FiscalYear', 'City', 'Country', 'Region', 'Subregion', 
            'RegionCode', 'SubRegionCode']

# Get numeric columns to randomize
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
numeric_cols = [c for c in numeric_cols if c not in preserve]
print(f"Randomizing {len(numeric_cols)} numeric columns...")

# Randomize each column
for col in numeric_cols:
    valid_count = df[col].notna().sum()
    if valid_count == 0:
        continue
    
    col_mean = df[col].mean()
    col_std = df[col].std()
    if pd.isna(col_std) or col_std == 0:
        col_std = abs(col_mean) * 0.3 if col_mean != 0 else 1
    
    # Generate random values
    new_vals = np.random.normal(col_mean, col_std, len(df))
    
    # Keep values positive if original was positive
    if df[col].min() >= 0:
        new_vals = np.abs(new_vals)
    
    # Clip to reasonable range
    new_vals = np.clip(new_vals, df[col].min() * 0.5 if df[col].min() >= 0 else df[col].min() * 1.5, 
                       df[col].max() * 1.5)
    
    # Preserve NaN positions
    nan_mask = df[col].isna()
    df[col] = new_vals
    df.loc[nan_mask, col] = np.nan

# Round integer-like columns
int_cols = ['StudentFTE', 'CapacityFTE', 'leads_submitted', 'enquiries_started', 
            'nps_responses_count', 'EmployeeHeadCountCurrent', 'school_age']
for c in int_cols:
    if c in df.columns:
        df[c] = df[c].round(0)

# Save to both formats
print("Saving to Excel...")
df.to_excel('School Level Data.xlsx', index=False)
print("Saving to CSV...")
df.to_csv('School Level Data.csv', index=False)

print("\n✓ Randomization complete!")
print(f"Sample data:")
print(df[['School', 'City', 'Region', 'StudentFTE', 'nps_score']].head(5))
