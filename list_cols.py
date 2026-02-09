
import pandas as pd

try:
    df = pd.read_excel('School Level Data.xlsx', sheet_name=0)
    print("Column List:")
    for col in df.columns:
        print(f"'{col}'")
except Exception as e:
    print(f"Error: {e}")
