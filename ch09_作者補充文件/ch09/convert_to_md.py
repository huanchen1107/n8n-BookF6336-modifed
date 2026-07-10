import sys
import os
from markitdown import MarkItDown

def main():
    # 檢查是否提供了檔案路徑參數
    if len(sys.argv) < 2:
        print("Error: Please provide a file path.")
        sys.exit(1)

    file_path = sys.argv[1]

    # 檢查檔案是否存在
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        sys.exit(1)

    try:
        # 初始化 MarkItDown
        md = MarkItDown()
        
        # 進行轉換
        result = md.convert(file_path)
        
        # 將轉換後的 Markdown 內容輸出 (n8n 會接收這裡的輸出)
        print(result.text_content)
        
    except Exception as e:
        print(f"Error during conversion: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()