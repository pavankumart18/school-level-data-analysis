"""
Filter dataset to keep only 80 schools with the most complete data.
Schools are ranked by the number of non-null values in key metrics.
"""
import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('School Level Data.csv')
print(f"Original: {len(df)} rows, {df['School'].nunique()} unique schools")

# Key metrics to consider for completeness
key_metrics = [
    'StudentFTE', 'CapacityFTE', 'NAE_Overall_Average_Fee_USD',
    'leads_submitted', 'enquiries_started', 'nps_score',
    'nps_responses_count', 'Teachers_Attrition_Pct'
]

# Count non-null values per school across all years
school_completeness = df.groupby('School').apply(
    lambda x: x[key_metrics].notna().sum().sum()
).reset_index()
school_completeness.columns = ['School', 'completeness_score']

# Sort by completeness and get top 80 schools
school_completeness = school_completeness.sort_values('completeness_score', ascending=False)
top_80_schools = school_completeness.head(80)['School'].tolist()

print(f"\nTop 80 schools by data completeness:")
print(f"  Min completeness score: {school_completeness.head(80)['completeness_score'].min()}")
print(f"  Max completeness score: {school_completeness.head(80)['completeness_score'].max()}")

# Filter to keep only records from top 80 schools
df_filtered = df[df['School'].isin(top_80_schools)]

print(f"\nFiltered: {len(df_filtered)} rows, {df_filtered['School'].nunique()} unique schools")

# Show which schools were removed
removed_schools = [s for s in df['School'].unique() if s not in top_80_schools]
print(f"\nRemoved {len(removed_schools)} schools:")
for school in removed_schools:
    score = school_completeness[school_completeness['School'] == school]['completeness_score'].values[0]
    print(f"  {school}: completeness score = {score}")

# Save filtered data
df_filtered.to_csv('School Level Data.csv', index=False)
df_filtered.to_excel('School Level Data.xlsx', index=False)

print(f"\n✓ Saved filtered data to CSV and Excel")
print(f"✓ {df_filtered['School'].nunique()} schools, {len(df_filtered)} total records")
