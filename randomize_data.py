
import pandas as pd
import numpy as np

# Set seed for reproducibility
np.random.seed(42)

# Load existing filtered data (80 schools)
df_orig = pd.read_csv('School Level Data.csv')
print(f"Loaded {len(df_orig)} rows from 80 schools.")

# Create a copy
df = df_orig.copy()

# Define Regional Base Parameters (Size, Fee Base, Growth Factor)
regional_params = {
    'The Americas': {'size': 900, 'fee': 35000, 'growth': 1.2},
    'Europe': {'size': 800, 'fee': 30000, 'growth': 1.0},
    'China Bilingual': {'size': 1200, 'fee': 25000, 'growth': 1.5},
    'China International': {'size': 1000, 'fee': 32000, 'growth': 1.1},
    'South East Asia & India': {'size': 1100, 'fee': 22000, 'growth': 1.3},
    'Middle East': {'size': 1500, 'fee': 20000, 'growth': 1.4}
}

# Generate Hidden Latent Variables per SCHOOL (fixed across years)
schools = df['School'].unique()
school_latent = {}
for school in schools:
    # Aggressiveness: 0 to 1 (focus on growth vs boutique)
    agg = np.random.beta(2, 2) 
    # Quality: 0 to 1 (academic excellence/care)
    qual = np.random.beta(3, 2) 
    school_latent[school] = {'agg': agg, 'qual': qual}

# Apply Logic Row by Row
for idx, row in df.iterrows():
    region = row['Region']
    school = row['School']
    params = regional_params.get(region, {'size': 800, 'fee': 25000, 'growth': 1.0})
    
    latent = school_latent.get(school, {'agg': 0.5, 'qual': 0.5})
    agg = latent['agg']
    qual = latent['qual']
    
    # 1. StudentFTE (Size): Driven by region + aggressiveness
    # Add yearly growth trend (small)
    year_factor = 1 + (row['FiscalYear'] - 2020) * 0.05 * params['growth']
    base_size = params['size'] * (0.8 + 0.6 * agg) 
    fte = base_size * year_factor * np.random.normal(1, 0.05)
    fte = max(100, fte)
    
    # 2. Capacity: Always > FTE
    cap_util = 0.7 + (0.4 * agg) # Aggressive schools run hotter (higher util)
    cap = fte / cap_util * np.random.normal(1, 0.02)
    
    # 3. Fees: Driven by Region + Quality
    base_fee = params['fee']
    fee = base_fee * (0.8 + 0.5 * qual) * np.random.normal(1, 0.05)
    
    # 4. NPS: Driven ONLY by Quality (Strong Positive) and mildly utilization (Negative)
    # This ensures "Quality" actually matches NPS
    nps_base = 10 + (qual * 60) # 10 to 70 range
    util_penalty = max(0, (cap_util - 0.9) * 20) # Penalty if over 90% utilized
    nps = nps_base - util_penalty + np.random.normal(0, 5)
    
    # 5. Teacher Attrition: High Attrition in Aggressive schools, Low in High Quality
    attrition = 10 + (20 * agg) - (10 * qual) + np.random.normal(0, 3)
    attrition = np.clip(attrition, 2, 40)
    
    # 6. Leads: Driven by Size (Scale) and Fee (Lower fee = more leads usually, but high demand curve)
    # Let's say Leads ~ Size * Aggressiveness * 1.2
    leads = (fte * 1.2) * (0.5 + 1.5 * agg) * np.random.normal(1, 0.1)
    
    # 7. Enquiries: Conversion from Leads based on Quality and NPS
    conv_rate = 0.2 + (0.3 * qual) # High quality converts better
    enquiries = leads * conv_rate * np.random.normal(1, 0.05)
    
    # Assign to dataframe
    df.at[idx, 'StudentFTE'] = int(fte)
    df.at[idx, 'CapacityFTE'] = int(cap)
    df.at[idx, 'NAE_Overall_Average_Fee_USD'] = int(fee)
    df.at[idx, 'nps_score'] = round(nps, 1)
    df.at[idx, 'nps_responses_count'] = int(fte * 0.2 * qual) # More responses in good schools
    df.at[idx, 'Teachers_Attrition_Pct'] = round(attrition, 1)
    df.at[idx, 'leads_submitted'] = int(leads)
    df.at[idx, 'enquiries_started'] = int(enquiries)

# Save
df.to_csv('School Level Data.csv', index=False)
df.to_excel('School Level Data.xlsx', index=False)

# Calculate Totals for Hero Section
total_students = df[df['FiscalYear'] == 2025]['StudentFTE'].sum() 
# Using 2025 as "current" for display, or sum of all years? 
# Usually Hero stats "Students" refers to current enrollment.
# Let's assume FY2025 is the latest complete year in this dataset context.

total_revenue = (df[df['FiscalYear'] == 2025]['StudentFTE'] * df[df['FiscalYear'] == 2025]['NAE_Overall_Average_Fee_USD']).sum()
total_enquiries = df[df['FiscalYear'] == 2025]['enquiries_started'].sum()

print("\n=== DATA GENERATED & SAVED ===")
print("Correlation Matrix Preview:")
cols = ['enquiries_started', 'leads_submitted', 'StudentFTE', 'CapacityFTE', 'NAE_Overall_Average_Fee_USD', 'nps_score']
print(df[cols].corr().round(2))

print("\n=== HERO STATS (FY2025) ===")
print(f"Schools: {df['School'].nunique()}")
print(f"Students: {int(total_students):,}")
print(f"Revenue: ${total_revenue/1e9:.2f}B")
print(f"Enquiries: {int(total_enquiries):,}")
