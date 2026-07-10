import pandas as pd
import sys
import os

def clean_data(input_path, output_path):
    # 讀取 Excel 或 CSV
    if input_path.endswith('.csv'):
        df = pd.read_csv(input_path)
    else:
        df = pd.read_excel(input_path)
    
    # 執行簡單清理：移除空值、去除空格
    df = df.dropna().apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    
    # 確保輸出目錄存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 儲存結果
    df.to_excel(output_path, index=False)
    print(f"Success: Cleaned file saved to {output_path}")

if __name__ == "__main__":
    clean_data(sys.argv[1], sys.argv[2])