import csv
import json
import random

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

# Seed for reproducibility if needed, but we just want legit data
all_samples = []

for r in rows:
    enq = num(r.get("enquiries_started"))
    fte = num(r.get("StudentFTE"))
    cap = num(r.get("CapacityFTE"))
    fees = num(r.get("NAE_Overall_Average_Fee_USD"))
    nps = num(r.get("nps_score"))
    attr = num(r.get("Teachers_Attrition_Pct"))
    age = num(r.get("school_age"))
    region = r.get("Region", "Unknown")
    
    if all(x is not None for x in [enq, fte, cap, fees, nps, attr, age]):
        all_samples.append({
            "enq": enq,
            "fte": fte,
            "cap": cap,
            "util": (fte / cap * 100) if cap > 0 else 0,
            "rate": (enq / fte) if fte > 0 else 0,
            "fees": fees,
            "nps": nps,
            "attr": attr,
            "age": age,
            "region": region
        })

# Take 100 actual data points
sample_data = random.sample(all_samples, min(100, len(all_samples)))

print("JSON_START")
print(json.dumps(sample_data))
print("JSON_END")
