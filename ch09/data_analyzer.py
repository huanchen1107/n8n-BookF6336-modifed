import pandas as pd
import sys

def analyze_data(file_path):
    df = pd.read_excel(file_path)
    # 產出簡單統計報告
    summary = df.describe()
    report_path = file_path.replace('.xlsx', '_summary.txt')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("--- Data Analysis Report ---\n")
        f.write(summary.to_string())
    
    print(f"Success: Analysis report generated at {report_path}")

if __name__ == "__main__":
    analyze_data(sys.argv[1])