
import pandas as pd
import os

# Input and output paths
input_file = "School Level Data.xlsx"
output_file = "School Level Data.csv"

if os.path.exists(input_file):
    try:
        # Read Excel file
        df = pd.read_excel(input_file)
        
        # Save as CSV
        df.to_csv(output_file, index=False)
        print(f"Successfully converted '{input_file}' to '{output_file}'")
    except Exception as e:
        print(f"Error converting file: {e}")
else:
    print(f"Error: Input file '{input_file}' not found.")
