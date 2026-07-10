import pandas as pd
import sys

def validate(file_path):
    df = pd.read_excel(file_path)
    # 檢查是否有欄位為空
    if df.isnull().values.any():
        print("Warning: Data contains empty values!")
    else:
        print("Validation: All data is present.")

if __name__ == "__main__":
    validate(sys.argv[1])