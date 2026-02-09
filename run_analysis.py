"""
Comprehensive EDA Analysis for Nord Anglia Education School Data
Generates visualizations and deep insights programmatically
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Set style for beautiful visualizations
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.facecolor'] = '#0a0f1a'
plt.rcParams['axes.facecolor'] = '#111827'
plt.rcParams['text.color'] = '#f9fafb'
plt.rcParams['axes.labelcolor'] = '#e5e7eb'
plt.rcParams['xtick.color'] = '#9ca3af'
plt.rcParams['ytick.color'] = '#9ca3af'
plt.rcParams['axes.edgecolor'] = '#374151'
plt.rcParams['grid.color'] = '#374151'
plt.rcParams['grid.alpha'] = 0.3
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 11

# Load data
print("="*70)
print("NORD ANGLIA EDUCATION - COMPREHENSIVE EDA ANALYSIS")
print("="*70)

df = pd.read_excel('School Level Data.xlsx')
print(f"\n✓ Loaded {len(df)} observations with {len(df.columns)} variables")
print(f"✓ Schools: {df['School'].nunique()}")
print(f"✓ Fiscal Years: {sorted(df['FiscalYear'].unique())}")

# ============================================================================
# 1. BASIC STATISTICS
# ============================================================================
print("\n" + "="*70)
print("1. BASIC STATISTICS")
print("="*70)

# Key metrics
schools = df['School'].nunique()
total_students = df['StudentFTE'].sum()
total_enquiries = df['enquiries_started'].sum()
total_leads = df['leads_submitted'].sum()

print(f"\nOverall Network Statistics:")
print(f"  Total Schools: {schools}")
print(f"  Total Observations: {len(df)}")
print(f"  Total Students (FTE): {total_students:,.0f}")
print(f"  Total Enquiries: {total_enquiries:,.0f}")
print(f"  Total Leads: {total_leads:,.0f}")

# Check for Revenue column
if 'Revenue' in df.columns:
    total_revenue = df['Revenue'].sum()
    print(f"  Total Revenue: ${total_revenue:,.0f}")

# FY2025 specific
fy25 = df[df['FiscalYear'] == 'FY2025']
if len(fy25) > 0:
    print(f"\nFY2025 Snapshot:")
    print(f"  Active Schools: {fy25['School'].nunique()}")
    print(f"  Students: {fy25['StudentFTE'].sum():,.0f}")
    print(f"  Enquiries: {fy25['enquiries_started'].sum():,.0f}")

# ============================================================================
# 2. CORRELATION ANALYSIS
# ============================================================================
print("\n" + "="*70)
print("2. CORRELATION ANALYSIS - What Drives Enquiries?")
print("="*70)

# Key numeric columns for correlation
potential_cols = [
    'enquiries_started', 'leads_submitted', 'StudentFTE', 'CapacityFTE',
    'NAE_Overall_Average_Fee_USD', 'Revenue', 'nps_score', 'nps_response_count',
    'Teachers_Attrition_Pct', 'MAC_Attrition_Pct', 'Employee_Engagement_Score',
    'Student_Expat_Pct', 'Academic_Performance_Index', 'school_age',
    'Overall_Gap_Median', 'Avg_Principal_Tenure'
]

# Filter to existing columns
numeric_cols = [c for c in potential_cols if c in df.columns]
print(f"\nAnalyzing {len(numeric_cols)} numeric variables...")

corr_df = df[numeric_cols].dropna()
print(f"Valid observations for correlation: {len(corr_df)}")

# Calculate correlations with enquiries
if 'enquiries_started' in corr_df.columns and len(corr_df) > 10:
    corr_with_enquiries = corr_df.corr()['enquiries_started'].drop('enquiries_started').sort_values(ascending=False)
    
    print("\nTop Correlations with enquiries_started:")
    for col, corr in corr_with_enquiries.items():
        direction = "+" if corr > 0 else ""
        significance = "***" if abs(corr) > 0.3 else "**" if abs(corr) > 0.2 else "*" if abs(corr) > 0.1 else ""
        print(f"  {col}: {direction}{corr:.3f} {significance}")
else:
    print("Insufficient data for correlation analysis")
    corr_with_enquiries = pd.Series()

# ============================================================================
# 3. GENERATE CORRELATION MATRIX HEATMAP
# ============================================================================
print("\n" + "="*70)
print("3. GENERATING VISUALIZATIONS")
print("="*70)

# Use top 10 columns for correlation matrix
top_cols = ['enquiries_started', 'leads_submitted', 'StudentFTE', 'CapacityFTE', 
            'NAE_Overall_Average_Fee_USD', 'Revenue', 'nps_score']
available_cols = [c for c in top_cols if c in df.columns]

if len(available_cols) >= 4:
    fig, ax = plt.subplots(figsize=(12, 10))
    
    corr_matrix = df[available_cols].corr()
    
    # Shorten column names for display
    short_names = {
        'enquiries_started': 'Enquiries',
        'leads_submitted': 'Leads',
        'StudentFTE': 'Students',
        'CapacityFTE': 'Capacity',
        'NAE_Overall_Average_Fee_USD': 'Fees',
        'Revenue': 'Revenue',
        'nps_score': 'NPS'
    }
    corr_matrix = corr_matrix.rename(columns=short_names, index=short_names)
    
    cmap = sns.diverging_palette(250, 15, s=75, l=40, as_cmap=True)
    
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap=cmap,
                center=0, vmin=-1, vmax=1, square=True, linewidths=1,
                cbar_kws={'label': 'Correlation Coefficient', 'shrink': 0.8},
                annot_kws={'size': 12, 'weight': 'bold'})
    
    plt.title('Correlation Matrix: Key Performance Metrics', fontsize=16, 
              color='white', pad=20, fontweight='bold')
    plt.tight_layout()
    plt.savefig('correlation_matrix.png', dpi=150, bbox_inches='tight', facecolor='#0a0f1a')
    plt.close()
    print("  ✓ Saved: correlation_matrix.png")
else:
    print("  ✗ Not enough columns for correlation matrix")

# ============================================================================
# 4. REGIONAL ANALYSIS
# ============================================================================
if 'Region' in df.columns:
    fig, ax = plt.subplots(figsize=(12, 7))
    
    region_stats = df.groupby('Region').agg({
        'enquiries_started': 'mean',
        'School': 'nunique'
    }).sort_values('enquiries_started', ascending=True)
    
    # Create gradient colors
    colors = plt.cm.YlOrRd(np.linspace(0.3, 0.9, len(region_stats)))
    
    bars = ax.barh(range(len(region_stats)), region_stats['enquiries_started'], 
                   color=colors, edgecolor='white', linewidth=1, height=0.7)
    
    ax.set_yticks(range(len(region_stats)))
    ax.set_yticklabels(region_stats.index)
    
    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, region_stats['enquiries_started'])):
        ax.text(val + 30, i, f'{val:,.0f}', 
                va='center', fontsize=11, color='white', fontweight='bold')
    
    ax.set_xlabel('Average Enquiries per School-Year', fontsize=12)
    ax.set_title('Average Enquiries by Region', fontsize=16, color='white', 
                 pad=20, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='x')
    ax.set_xlim(0, region_stats['enquiries_started'].max() * 1.2)
    
    plt.tight_layout()
    plt.savefig('regional_enquiries.png', dpi=150, bbox_inches='tight', facecolor='#0a0f1a')
    plt.close()
    print("  ✓ Saved: regional_enquiries.png")
    
    # Print regional stats
    print("\nRegional Analysis:")
    for region, row in region_stats.sort_values('enquiries_started', ascending=False).iterrows():
        print(f"  {region}: {row['enquiries_started']:,.0f} avg enquiries ({row['School']} schools)")

# ============================================================================
# 5. NPS ANALYSIS (if available)
# ============================================================================
# Check for NPS columns
nps_cols = [c for c in df.columns if 'nps' in c.lower()]
print(f"\nNPS columns found: {nps_cols}")

if 'nps_score' in df.columns:
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # NPS correlations
    nps_data = [
        ('NPS Response Count', df['nps_response_count'].corr(df['enquiries_started']) if 'nps_response_count' in df.columns else np.nan),
        ('NPS Score', df['nps_score'].corr(df['enquiries_started']))
    ]
    nps_data = [(n, v) for n, v in nps_data if not np.isnan(v)]
    
    if nps_data:
        names = [x[0] for x in nps_data]
        values = [x[1] for x in nps_data]
        colors = ['#10b981' if v > 0 else '#ef4444' for v in values]
        
        bars = ax.barh(names, values, color=colors, edgecolor='white', linewidth=1, height=0.5)
        ax.axvline(x=0, color='white', linewidth=1, alpha=0.5)
        
        for bar, val in zip(bars, values):
            offset = 0.02 if val >= 0 else -0.02
            ax.text(val + offset, bar.get_y() + bar.get_height()/2, 
                    f'{val:+.2f}', va='center', fontsize=12, color='white', fontweight='bold')
        
        ax.set_xlabel('Correlation with Enquiries', fontsize=12)
        ax.set_title('NPS vs Enquiries Correlation', fontsize=16, color='white', pad=20, fontweight='bold')
        ax.set_xlim(-0.5, 0.5)
        ax.grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        plt.savefig('nps_correlation.png', dpi=150, bbox_inches='tight', facecolor='#0a0f1a')
        plt.close()
        print("  ✓ Saved: nps_correlation.png")

# ============================================================================
# 6. DEMAND DRIVERS CHART
# ============================================================================
if len(corr_with_enquiries) > 0:
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Get top 10 drivers
    top_drivers = corr_with_enquiries.head(10).sort_values()
    
    colors = ['#10b981' if v > 0 else '#ef4444' for v in top_drivers.values]
    
    bars = ax.barh(range(len(top_drivers)), top_drivers.values, 
                   color=colors, edgecolor='white', linewidth=1, height=0.6)
    
    ax.set_yticks(range(len(top_drivers)))
    ax.set_yticklabels(top_drivers.index, fontsize=10)
    
    # Value labels
    for i, (bar, val) in enumerate(zip(bars, top_drivers.values)):
        offset = 0.02 if val > 0 else -0.02
        align = 'left' if val > 0 else 'right'
        ax.text(val + offset, i, f'{val:+.2f}', 
                va='center', ha=align, fontsize=11, color='white', fontweight='bold')
    
    ax.axvline(x=0, color='white', linewidth=1, alpha=0.5)
    ax.set_xlabel('Correlation Coefficient (r)', fontsize=12)
    ax.set_title('Top Drivers of School Enquiries', fontsize=16, color='white', pad=20, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    plt.savefig('demand_drivers.png', dpi=150, bbox_inches='tight', facecolor='#0a0f1a')
    plt.close()
    print("  ✓ Saved: demand_drivers.png")

# ============================================================================
# 7. UTILIZATION ANALYSIS
# ============================================================================
if 'StudentFTE' in df.columns and 'CapacityFTE' in df.columns:
    df['utilization'] = df['StudentFTE'] / df['CapacityFTE'] * 100
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    util_data = df['utilization'].dropna()
    util_data = util_data[util_data < 300]  # Filter extreme outliers
    
    ax.hist(util_data, bins=30, color='#c9a227', edgecolor='white', linewidth=0.5, alpha=0.9)
    ax.axvline(x=100, color='#ef4444', linewidth=2, linestyle='--', label=f'100% Capacity')
    ax.axvline(x=util_data.mean(), color='#10b981', linewidth=2, label=f'Mean: {util_data.mean():.0f}%')
    
    ax.set_xlabel('Utilization (%)', fontsize=12)
    ax.set_ylabel('Number of School-Years', fontsize=12)
    ax.set_title('School Capacity Utilization Distribution', fontsize=16, color='white', pad=20, fontweight='bold')
    ax.legend(framealpha=0.9, facecolor='#1f2937', edgecolor='#374151')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('utilization_distribution.png', dpi=150, bbox_inches='tight', facecolor='#0a0f1a')
    plt.close()
    print("  ✓ Saved: utilization_distribution.png")
    
    # Outliers
    over_capacity = df[df['utilization'] > 100].groupby('School').agg({
        'utilization': 'max',
        'Region': 'first'
    }).sort_values('utilization', ascending=False)
    
    print(f"\nOver-Capacity Schools (>100% Utilization): {len(over_capacity)}")
    for school, row in over_capacity.head(5).iterrows():
        print(f"  {school}: {row['utilization']:.0f}% ({row['Region']})")

# ============================================================================
# 8. ENQUIRIES TREND
# ============================================================================
if 'FiscalYear' in df.columns:
    fig, ax = plt.subplots(figsize=(12, 6))
    
    yearly = df.groupby('FiscalYear')['enquiries_started'].sum().sort_index()
    
    ax.plot(range(len(yearly)), yearly.values, marker='o', markersize=12, linewidth=3, 
            color='#c9a227', markerfacecolor='#c9a227', markeredgecolor='white', markeredgewidth=2)
    ax.fill_between(range(len(yearly)), yearly.values, alpha=0.2, color='#c9a227')
    
    ax.set_xticks(range(len(yearly)))
    ax.set_xticklabels(yearly.index, fontsize=10)
    
    # Add value labels
    for i, val in enumerate(yearly.values):
        ax.annotate(f'{val/1000:.0f}K', (i, val), textcoords="offset points", 
                    xytext=(0, 15), ha='center', fontsize=11, color='white', fontweight='bold')
    
    ax.set_xlabel('Fiscal Year', fontsize=12)
    ax.set_ylabel('Total Enquiries', fontsize=12)
    ax.set_title('Enquiries Trend Over Time', fontsize=16, color='white', pad=20, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('enquiries_trend.png', dpi=150, bbox_inches='tight', facecolor='#0a0f1a')
    plt.close()
    print("  ✓ Saved: enquiries_trend.png")
    
    # YoY change
    print("\nYear-over-Year Enquiries:")
    for i, (year, val) in enumerate(yearly.items()):
        if i > 0:
            prev = yearly.iloc[i-1]
            change = (val - prev) / prev * 100
            print(f"  {year}: {val:,.0f} ({change:+.1f}% YoY)")
        else:
            print(f"  {year}: {val:,.0f}")

# ============================================================================
# 9. SCATTER: FEES vs ENQUIRIES
# ============================================================================
if 'NAE_Overall_Average_Fee_USD' in df.columns and 'Region' in df.columns:
    fig, ax = plt.subplots(figsize=(12, 8))
    
    scatter_df = df[['NAE_Overall_Average_Fee_USD', 'enquiries_started', 'Region']].dropna()
    
    regions = scatter_df['Region'].unique()
    colors = plt.cm.tab10(np.linspace(0, 1, len(regions)))
    
    for region, color in zip(regions, colors):
        region_data = scatter_df[scatter_df['Region'] == region]
        ax.scatter(region_data['NAE_Overall_Average_Fee_USD'], 
                   region_data['enquiries_started'],
                   label=region, alpha=0.7, s=80, c=[color], 
                   edgecolors='white', linewidth=0.5)
    
    ax.set_xlabel('Average Fee (USD)', fontsize=12)
    ax.set_ylabel('Enquiries Started', fontsize=12)
    ax.set_title('Fees vs Enquiries by Region', fontsize=16, color='white', pad=20, fontweight='bold')
    ax.legend(title='Region', loc='upper right', framealpha=0.9, 
              facecolor='#1f2937', edgecolor='#374151', fontsize=9)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('fees_vs_enquiries.png', dpi=150, bbox_inches='tight', facecolor='#0a0f1a')
    plt.close()
    print("  ✓ Saved: fees_vs_enquiries.png")

# ============================================================================
# 10. SCATTER: SIZE vs ENQUIRIES
# ============================================================================
if 'StudentFTE' in df.columns and 'Region' in df.columns:
    fig, ax = plt.subplots(figsize=(12, 8))
    
    scatter_df = df[['StudentFTE', 'enquiries_started', 'Region']].dropna()
    
    for region, color in zip(regions, colors):
        region_data = scatter_df[scatter_df['Region'] == region]
        ax.scatter(region_data['StudentFTE'], 
                   region_data['enquiries_started'],
                   label=region, alpha=0.7, s=80, c=[color], 
                   edgecolors='white', linewidth=0.5)
    
    ax.set_xlabel('Student FTE (School Size)', fontsize=12)
    ax.set_ylabel('Enquiries Started', fontsize=12)
    ax.set_title('School Size vs Enquiries by Region', fontsize=16, color='white', pad=20, fontweight='bold')
    ax.legend(title='Region', loc='upper left', framealpha=0.9, 
              facecolor='#1f2937', edgecolor='#374151', fontsize=9)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('size_vs_enquiries.png', dpi=150, bbox_inches='tight', facecolor='#0a0f1a')
    plt.close()
    print("  ✓ Saved: size_vs_enquiries.png")

# ============================================================================
# 11. SUMMARY STATISTICS
# ============================================================================
print("\n" + "="*70)
print("4. KEY METRICS SUMMARY")
print("="*70)

summary_cols = ['NAE_Overall_Average_Fee_USD', 'StudentFTE', 'CapacityFTE', 'enquiries_started', 'leads_submitted']
available_summary = [c for c in summary_cols if c in df.columns]

print("\n{:<30} {:>12} {:>12} {:>12} {:>12}".format("Metric", "Mean", "Median", "Min", "Max"))
print("-" * 80)

for col in available_summary:
    data = df[col].dropna()
    print("{:<30} {:>12,.1f} {:>12,.1f} {:>12,.1f} {:>12,.1f}".format(
        col[:30], data.mean(), data.median(), data.min(), data.max()))

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "="*70)
print("✓ ANALYSIS COMPLETE - ALL VISUALIZATIONS GENERATED")
print("="*70)
print("\nGenerated Files:")
import os
for f in os.listdir('.'):
    if f.endswith('.png') and not f.startswith('Code_'):
        print(f"  • {f}")
print("\n" + "="*70)
