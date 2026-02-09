
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.facecolor'] = '#0a0f1a'
plt.rcParams['axes.facecolor'] = '#111827'
plt.rcParams['text.color'] = '#f9fafb'
plt.rcParams['axes.labelcolor'] = '#e5e7eb'
plt.rcParams['xtick.color'] = '#9ca3af'
plt.rcParams['ytick.color'] = '#9ca3af'
plt.rcParams['font.family'] = 'sans-serif'

print("Loading Data...")
df = pd.read_excel('School Level Data.xlsx')

# Metric Calculation
df['StudentFTE'] = pd.to_numeric(df['StudentFTE'], errors='coerce')
df['enquiries_started'] = pd.to_numeric(df['enquiries_started'], errors='coerce')
df = df[df['StudentFTE'] > 20] # Robust filter
df['Rate'] = df['enquiries_started'] / df['StudentFTE']

print(f"Calculated Enquiries/Student for {len(df)} schools.")

# 1. DRIVERS (CORRELATION)
print("Generating Drivers Chart...")
numeric_df = df.select_dtypes(include=[np.number])
# Top correlations with Rate
corr = numeric_df.corr(method='spearman')['Rate'].sort_values()
# Filter out the metric itself and components
corr = corr.drop(['Rate', 'enquiries_started', 'leads_submitted', 'tv_leads_t_plus1'], errors='ignore')
# Remove NaNs
corr = corr.dropna()

top_pos = corr.tail(5)
top_neg = corr.head(5)
top_drivers = pd.concat([top_neg, top_pos])

fig, ax = plt.subplots(figsize=(12, 8))
colors = ['#10b981' if v > 0 else '#ef4444' for v in top_drivers.values]
bars = ax.barh(range(len(top_drivers)), top_drivers.values, color=colors, edgecolor='white', height=0.6)
ax.set_yticks(range(len(top_drivers)))
ax.set_yticklabels(top_drivers.index, fontsize=10)
ax.axvline(0, color='white', alpha=0.5)
ax.set_title("Top Drivers: Enquiries per Student", fontsize=16, color='white', fontweight='bold')
plt.tight_layout()
plt.savefig('demand_drivers.png', facecolor='#0a0f1a')
plt.close()

# 2. REGIONAL ANALYSIS
print("Generating Regional Chart...")
if 'Region' in df.columns:
    region_stats = df.groupby('Region')['Rate'].mean().sort_values()
    fig, ax = plt.subplots(figsize=(12, 7))
    colors = plt.cm.YlOrRd(np.linspace(0.3, 0.9, len(region_stats)))
    bars = ax.barh(range(len(region_stats)), region_stats.values, color=colors, edgecolor='white')
    ax.set_yticks(range(len(region_stats)))
    ax.set_yticklabels(region_stats.index)
    
    # Labels
    for i, v in enumerate(region_stats.values):
        ax.text(v + 0.05, i, f'{v:.2f}', va='center', color='white', fontweight='bold')
        
    ax.set_title("Average Enquiries per Student by Region", fontsize=16, color='white', fontweight='bold')
    plt.tight_layout()
    plt.savefig('regional_enquiries.png', facecolor='#0a0f1a')
    plt.close()

# 3. FEES SCATTER
print("Generating Fees Scatter...")
if 'NAE_Overall_Average_Fee_USD' in df.columns:
    fig, ax = plt.subplots(figsize=(12, 8))
    regions = df['Region'].dropna().unique()
    colors = plt.cm.tab10(np.linspace(0, 1, len(regions)))
    
    for r, c in zip(regions, colors):
        subset = df[df['Region'] == r]
        ax.scatter(subset['NAE_Overall_Average_Fee_USD'], subset['Rate'], label=r, color=c, alpha=0.7, edgecolors='white')
        
    ax.set_xlabel('Average Fee (USD)')
    ax.set_ylabel('Enquiries per Student')
    ax.set_title("Fees vs Enquiry Rate", fontsize=16, color='white', fontweight='bold')
    ax.legend(frameon=True, facecolor='#1f2937')
    plt.tight_layout()
    plt.savefig('fees_vs_enquiries.png', facecolor='#0a0f1a')
    plt.close()
    
# 4. SIZE SCATTER
print("Generating Size Scatter...")
fig, ax = plt.subplots(figsize=(12, 8))
for r, c in zip(regions, colors):
    subset = df[df['Region'] == r]
    ax.scatter(subset['StudentFTE'], subset['Rate'], label=r, color=c, alpha=0.7, edgecolors='white')
ax.set_xlabel('School Size (FTE)')
ax.set_ylabel('Enquiries per Student')
ax.set_title("Size vs Enquiry Rate", fontsize=16, color='white', fontweight='bold')
ax.legend(frameon=True, facecolor='#1f2937')
plt.tight_layout()
plt.savefig('size_vs_enquiries.png', facecolor='#0a0f1a')
plt.close()

# 5. NPS CORRELATION
print("Generating NPS Chart...")
if 'nps_score' in df.columns:
    nps_corr = df['nps_score'].corr(df['Rate'], method='spearman')
    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.barh(['NPS Score'], [nps_corr], color='#10b981' if nps_corr > 0 else '#ef4444', height=0.4)
    ax.set_xlim(-1, 1)
    ax.axvline(0, color='white')
    ax.text(nps_corr + (0.1 if nps_corr>0 else -0.1), 0, f"{nps_corr:.3f}", color='white', fontweight='bold', va='center')
    ax.set_title("NPS vs Enquiry Rate Correlation", fontsize=14, color='white', fontweight='bold')
    plt.tight_layout()
    plt.savefig('nps_correlation.png', facecolor='#0a0f1a')
    plt.close()

print("Done.")
