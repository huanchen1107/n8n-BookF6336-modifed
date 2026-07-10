import sys
import json
import pdfplumber

def read_pdf(file_path):
    result = {
        "pages": [],
        "tables": [],
        "full_text": ""
    }

    all_text = []

    with pdfplumber.open(file_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):

            # 讀取文字
            text = page.extract_text()
            if text:
                text = text.strip()
                result["pages"].append({
                    "page": page_num,
                    "text": text
                })
                all_text.append(f"[第 {page_num} 頁]\n{text}")

            # 讀取表格
            tables = page.extract_tables()
            for table_idx, table in enumerate(tables):
                result["tables"].append({
                    "page": page_num,
                    "table_index": table_idx + 1,
                    "data": table
                })

    result["full_text"] = '\n\n'.join(all_text)

    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "請提供 PDF 檔案路徑"}, ensure_ascii=False))
        sys.exit(1)
    read_pdf(sys.argv[1])
