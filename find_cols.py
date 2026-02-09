
import pandas as pd

df = pd.read_excel('School Level Data.xlsx')
matches = [c for c in df.columns if 'nquir' in c or 'FTE' in c or 'Student' in c]
print("--- Found Columns ---")
for m in matches:
    print(m)
