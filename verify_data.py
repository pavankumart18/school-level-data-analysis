import csv
from collections import defaultdict
import statistics

with open("School Level Data.csv", "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

def num(v):
    if v is None or v == "":
        return None
    try:
        return float(str(v).replace(",", ""))
    except:
        return None

def pearson_r(x, y):
    pairs = [(a, b) for a, b in zip(x, y) if a is not None and b is not None]
    if len(pairs) < 3:
        return None, 0
    xs, ys = zip(*pairs)
    n = len(xs)
    mx, my = sum(xs)/n, sum(ys)/n
    sx = (sum((xi-mx)**2 for xi in xs))**0.5
    sy = (sum((yi-my)**2 for yi in ys))**0.5
    if sx == 0 or sy == 0:
        return 0, n
    return sum((xi-mx)*(yi-my) for xi, yi in zip(xs, ys)) / (sx * sy), n

# Pre-compute all needed columns
all_enq = [num(r.get("enquiries_started")) for r in rows]
all_fte = [num(r.get("StudentFTE")) for r in rows]
all_cap = [num(r.get("CapacityFTE")) for r in rows]
all_fees = [num(r.get("NAE_Overall_Average_Fee_USD")) for r in rows]
all_nps = [num(r.get("nps_score")) for r in rows]
all_nps_resp = [num(r.get("nps_responses_count")) for r in rows]
all_leads = [num(r.get("leads_submitted")) for r in rows]
all_attr = [num(r.get("Teachers_Attrition_Pct")) for r in rows]
all_mac_attr = [num(r.get("MAC_Attrition_Pct")) for r in rows]
all_tenure = [num(r.get("Average_Principal_Tenure")) for r in rows]
all_engage = [num(r.get("Employee_Engagement_Score")) for r in rows]
all_age = [num(r.get("school_age")) for r in rows]
all_acad = [num(r.get("Academic_Performance_Index")) for r in rows]
all_maint = [num(r.get("Mainentance_Capex_sum")) for r in rows]
all_expat = [num(r.get("Student_Expat_Pct")) for r in rows]
all_desktop = [num(r.get("Device_desktop")) for r in rows]
all_nps_princ = [num(r.get("nps_principal_quality_score")) for r in rows]
all_nps_edu = [num(r.get("nps_education_quality_score")) for r in rows]
all_hnwi = [num(r.get("hnwi_number_of_millionaires")) for r in rows]
all_cvr_yoy = [num(r.get("Enquiries - Enrolled CVR YoY")) for r in rows]

# Enquiry rate (enquiries per student)
all_rate = []
for i in range(len(rows)):
    enq = all_enq[i]
    fte = all_fte[i]
    if enq is not None and fte is not None and fte > 0:
        all_rate.append(enq / fte)
    else:
        all_rate.append(None)

# Utilization
all_util = []
for i in range(len(rows)):
    fte = all_fte[i]
    cap = all_cap[i]
    if fte and cap and cap > 0:
        all_util.append(fte / cap * 100)
    else:
        all_util.append(None)

out = []
out.append("=" * 75)
out.append("  HYPOTHESIS.HTML — COMPREHENSIVE DATA VERIFICATION")
out.append("  20 Hypotheses + Region Data + Curriculum Chart")
out.append("=" * 75)

# =============================================
# HYPOTHESIS VERIFICATION
# =============================================
# Map each hypothesis to its actual data columns
# The hypotheses use "Rate" (enquiries/student) or raw enquiry volume

hypotheses = [
    # Operational
    ("H1", "Scale Effect", "ρ", 0.83, all_fte, all_enq, "StudentFTE vs Enquiries"),
    ("H2", "Growth Strain", "ρ", -0.47, all_attr, all_enq, "Teacher Attrition vs Enquiries"),
    ("H3", "Leader Stability", "ρ", 0.20, all_tenure, all_rate, "Principal Tenure vs Rate"),
    ("H4", "Retention Momentum", "ρ", 0.14, all_cvr_yoy, all_rate, "CVR YoY vs Rate"),
    
    # Curriculum
    ("H5", "IB Quality Magnet", "ρ", 0.32, None, None, "IB NPS - use nps_education_quality"),
    ("H6", "IGCSE Volume Engine", "ρ", 0.10, None, None, "IGCSE +112% - categorical"),
    ("H7", "A-Level Core", "ρ", 0.09, None, None, "A-Levels +6% - categorical"),
    ("H8", "Multi-Program Lift", "ρ", 0.09, None, None, "Multi-curricula - categorical"),
    
    # Market
    ("H9", "Lead Velocity", "ρ", 0.94, all_leads, all_enq, "Leads vs Enquiries"),
    ("H10", "Regional Bias", "H", 0.68, None, None, "Regional H-test"),
    ("H11", "Wealth Density", "ρ", 0.21, all_hnwi, all_rate, "HNWI vs Rate"),
    ("H12", "Fee Sensitivity", "ρ", -0.22, all_fees, all_enq, "Fees vs Enquiries"),
    
    # Quality
    ("H13", "Engagement Signal", "ρ", 0.74, all_nps_resp, all_enq, "NPS Response Count vs Enquiries"),
    ("H14", "Principal Quality", "ρ", 0.12, all_nps_princ, all_rate, "Principal NPS vs Rate"),
    ("H15", "Intent Channel", "ρ", 0.22, all_desktop, all_rate, "Desktop % vs Rate"),
    ("H16", "Relocation Driver", "ρ", 0.26, all_expat, all_rate, "Expat % vs Rate"),
    
    # Rejected
    ("H17", "The NPS Paradox", "ρ", 0.12, all_nps, all_rate, "NPS vs Rate"),
    ("H18", "Academic Performance", "ρ", -0.01, all_acad, all_rate, "Academic Index vs Rate"),
    ("H19", "Maintenance Capex", "ρ", 0.06, all_maint, all_rate, "Maint Capex vs Rate"),
    ("H20", "School Age", "ρ", 0.06, all_age, all_rate, "School Age vs Rate"),
]

out.append("\n" + "-" * 75)
out.append(f"  {'ID':<5} {'Name':<25} {'Claimed':>8} {'Actual':>8} {'n':>5} {'Verdict'}")
out.append("-" * 75)

mismatches = []

for hid, name, htype, claimed, x_data, y_data, desc in hypotheses:
    if x_data is not None and y_data is not None:
        actual, n = pearson_r(x_data, y_data)
        if actual is not None:
            delta = abs(actual - claimed)
            ok = delta < 0.08
            verdict = "✅" if ok else f"⚠️  Δ={delta:.2f}"
            out.append(f"  {hid:<5} {name:<25} {claimed:>+8.2f} {actual:>+8.2f} {n:>5} {verdict}  [{desc}]")
            if not ok:
                mismatches.append((hid, name, claimed, actual, delta, desc))
        else:
            out.append(f"  {hid:<5} {name:<25} {claimed:>+8.2f} {'N/A':>8} {'?':>5} ⚠️  No data  [{desc}]")
    else:
        out.append(f"  {hid:<5} {name:<25} {claimed:>+8.2f} {'---':>8} {'':>5} ℹ️  Categorical  [{desc}]")

# =============================================
# SPECIAL VERIFICATIONS
# =============================================

# H5: IB vs NPS
out.append("\n" + "=" * 75)
out.append("  SPECIAL: Curriculum & Categorical Hypotheses")
out.append("=" * 75)

# IB quality: check Curricula_Offered_IB (continuous) vs nps_score
ib_col = [num(r.get("Curricula_Offered_IB")) for r in rows]
r_ib_nps, n_ib = pearson_r(ib_col, all_nps)
out.append(f"\n  H5 IB Quality Magnet (claimed ρ=0.32):")
out.append(f"    Curricula_Offered_IB (continuous) vs NPS: r = {r_ib_nps:+.2f} (n={n_ib})" if r_ib_nps else "    insufficient data")
r_edu_nps, n_edu = pearson_r(all_nps_edu, all_nps)
out.append(f"    nps_education_quality vs nps_score: r = {r_edu_nps:+.2f} (n={n_edu})" if r_edu_nps else "    insufficient")

# Curriculum grouping: rate by Prevailing_Curriculum
out.append(f"\n  H6/H7 Curriculum Rates (claimed IGCSE=+112%, A-Levels=+6%):")
curr_rates = defaultdict(list)
curr_enq = defaultdict(list)
for i, r in enumerate(rows):
    curr = r.get("Prevailing_Curriculum", "").strip()
    rate = all_rate[i]
    enq = all_enq[i]
    if curr and rate is not None:
        curr_rates[curr].append(rate)
    if curr and enq is not None:
        curr_enq[curr].append(enq)

overall_enq = statistics.mean([x for x in all_enq if x is not None])
for curr in sorted(curr_enq, key=lambda c: -statistics.mean(curr_enq[c])):
    avg_enq = statistics.mean(curr_enq[curr])
    avg_rate = statistics.mean(curr_rates[curr]) if curr in curr_rates else 0
    pct = ((avg_enq - overall_enq) / overall_enq) * 100
    out.append(f"    {curr}: avg_enq={avg_enq:.0f} ({pct:+.0f}% vs overall), avg_rate={avg_rate:.2f}")

# H8: Multi-program
curr_count = [num(r.get("Curricula_Offered_count")) for r in rows]
r_multi, n_multi = pearson_r(curr_count, all_rate)
out.append(f"\n  H8 Multi-Program Lift (claimed ρ=0.09): actual r = {r_multi:+.2f} (n={n_multi})" if r_multi else "\n  H8: insufficient data")

# =============================================
# REGION CHART DATA
# =============================================
out.append("\n" + "=" * 75)
out.append("  REGION CHART VERIFICATION")
out.append("=" * 75)
out.append("  Claimed: ME=0.68, CB=0.62, Americas=0.61, Europe=0.59, SEA&I=0.56, Chi-Int=0.50")

region_rates = defaultdict(list)
for i, r in enumerate(rows):
    reg = r.get("Region", "").strip()
    rate = all_rate[i]
    if reg and rate is not None:
        region_rates[reg].append(rate)

for reg, rates in sorted(region_rates.items(), key=lambda x: -statistics.mean(x[1])):
    avg = statistics.mean(rates)
    out.append(f"    {reg}: avg rate = {avg:.2f} (n={len(rates)})")

# =============================================
# CURRICULUM CHART DATA (lines 1105-1110)
# =============================================
out.append("\n" + "=" * 75)
out.append("  CURRICULUM CHART VERIFICATION")
out.append("=" * 75)
out.append("  Claimed: IGCSE=0.81, IB=0.61, A-Levels=0.56, AP=0.56")
for curr in sorted(curr_rates, key=lambda c: -statistics.mean(curr_rates[c])):
    avg_rate = statistics.mean(curr_rates[curr])
    out.append(f"    {curr}: avg rate = {avg_rate:.2f} (n={len(curr_rates[curr])})")

# =============================================
# RECOMMENDATIONS TABLE (lines 862-893)
# =============================================
out.append("\n" + "=" * 75)
out.append("  RECOMMENDATIONS TABLE VERIFICATION")
out.append("=" * 75)
out.append("  1. H16: ρ=0.51 (Mobilize Parent Ambassadors)")
r_expat, n_expat = pearson_r(all_expat, all_rate)
out.append(f"     Expat% vs Rate: actual r = {r_expat:+.2f} (n={n_expat})" if r_expat else "     insufficient")
out.append(f"     BUT H16 card says ρ=0.26. Table says ρ=0.51. INCONSISTENCY?")

out.append(f"  2. H6/H7: +33-37% lift")
out.append(f"     IGCSE +112%, A-Levels +6% from card data. '33-37%' doesn't match either.")

out.append(f"  3. H2: ρ=-0.47 (Fix Teacher Retention)")
all_stability = [100 - x if x is not None else None for x in all_attr]
r_stab, n_stab = pearson_r(all_stability, all_rate)
out.append(f"     Teacher Stability (100-Attrition) vs Rate: r = {r_stab:+.2f} (n={n_stab})" if r_stab else "     insufficient")

out.append(f"  4. H5: 3× regional premium")
if region_rates:
    sorted_regs = sorted(region_rates.items(), key=lambda x: -statistics.mean(x[1]))
    top_reg = sorted_regs[0]
    bottom_reg = sorted_regs[-1]
    ratio = statistics.mean(top_reg[1]) / statistics.mean(bottom_reg[1])
    out.append(f"     Top region ({top_reg[0]}): {statistics.mean(top_reg[1]):.2f}")
    out.append(f"     Bottom region ({bottom_reg[0]}): {statistics.mean(bottom_reg[1]):.2f}")
    out.append(f"     Ratio: {ratio:.1f}×")

out.append(f"  5. H2: ρ=0.42 (Embrace Capacity Scarcity)")
r_util, n_util = pearson_r(all_util, all_rate)
out.append(f"     Utilization vs Rate: r = {r_util:+.2f} (n={n_util})" if r_util else "     insufficient")

# =============================================
# SUMMARY
# =============================================
out.append("\n" + "=" * 75)
out.append("  MISMATCHES SUMMARY")
out.append("=" * 75)
if mismatches:
    for hid, name, claimed, actual, delta, desc in mismatches:
        out.append(f"  ⚠️  {hid} {name}: claimed={claimed:+.2f}, actual={actual:+.2f}, Δ={delta:.2f}")
        out.append(f"      [{desc}]")
else:
    out.append("  ✅ All directly verifiable hypotheses match!")

with open("hypothesis_verification.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))

print("Done! See hypothesis_verification.txt")
