import pandas as pd
import sys
import os

def convert_csv_to_excel(csv_path, excel_path):
    df = pd.read_csv(csv_path)
    os.makedirs(os.path.dirname(excel_path), exist_ok=True)
    df.to_excel(excel_path, index=False, engine='openpyxl')
    print(f"Converted: {excel_path}")

if __name__ == "__main__":
    convert_csv_to_excel(sys.argv[1], sys.argv[2])