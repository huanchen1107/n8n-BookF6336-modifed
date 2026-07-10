# 批次文件 AI 摘要工作流程設定指南
## 一次讀取多份文件（PDF / TXT / DOCX），AI 逐一產生摘要並寫回 Excel

---

## 前置準備

### 目錄結構
```
C:\n8n-data\ch07\
├── PDF\
│   ├── doc001.pdf   ← IT 服務合約
│   ├── doc002.pdf   ← Q3 財務報告
│   ├── doc003.pdf   ← 董事會議記錄
│   ├── doc004.pdf   ← 個人履歷
│   └── doc005.pdf   ← 採購訂單
└── document_summary.xlsx   ← AI 摘要結果寫入此檔
```

### Excel 檔案欄位結構（document_summary.xlsx）

| 欄 | 欄位名稱 | 說明 |
|----|---------|------|
| A | No. | 序號 |
| B | File Name | 原始檔名 |
| C | File Type | 檔案類型（PDF/TXT/DOCX） |
| D | File Path | 完整路徑 |
| E | AI Summary | AI 產生的摘要（由 n8n 寫入） |
| F | Key Topics | AI 萃取的關鍵主題（由 n8n 寫入） |
| G | Status | 處理狀態（Pending → Done / Error） |
| H | Process Time | 處理完成時間（由 n8n 寫入） |

---

## Workflow 架構總覽

```
[Manual Trigger]
       ↓
[Excel AI] ─── 讀取 Excel 取得待處理清單（Status = Pending）
       ↓
[Split in Batches] ─── 每次處理 1 筆，避免超時
       ↓
[Switch] ─── 依 File Type 分流
   ├── PDF  → [Read Binary] → [Extract from File: PDF]
   ├── TXT  → [Read Binary] → [Extract from File: Text]
   └── DOCX → [Read Binary] → [Extract from File: DOCX / Execute Command + python-docx]
       ↓
[Merge Branches] ─── 合併各分支的文字內容
       ↓
[OpenAI] ─── 產生摘要 + 關鍵主題
       ↓
[Code 節點] ─── 解析 AI 回傳 JSON
       ↓
[Excel AI] ─── 更新該行的 Summary、Key Topics、Status、Time
       ↓
[Excel AI（Log）] ─── 寫入 Processing Log 工作表
```

---

## 各節點詳細設定

---

### 節點 1：Manual Trigger
手動觸發，或可改為 Schedule Trigger 設定定時執行。

---

### 節點 2：Excel AI — 讀取待處理清單

**Resource：** Row  
**Operation：** Filter Rows

| 參數 | 值 |
|------|-----|
| Input Mode | File Path |
| File Path | `C:\n8n-data\ch07\document_summary.xlsx` |
| Sheet Name | `Document Summary` |
| Filter Field | `Status` |
| Filter Operator | Equals |
| Filter Value | `Pending` |
| Include Row Number | **開啟**（後續更新列需要用到 `_rowNumber`） |

> 輸出：每筆 Pending 的文件資料各為一個 item，包含 `_rowNumber`、`File Name`、`File Type`、`File Path` 等欄位。

---

### 節點 3：Split in Batches

| 參數 | 值 |
|------|-----|
| Batch Size | `1` |

> 每次只處理一筆，確保 OpenAI 不超時，且 Excel 更新順序正確。

---

### 節點 4：Switch — 依檔案類型分流

**Mode：** Rules

| 條件 | 輸出 Port |
|------|-----------|
| `{{ $json["File Type"] }}` equals `PDF` | Output 0 |
| `{{ $json["File Type"] }}` equals `TXT` | Output 1 |
| `{{ $json["File Type"] }}` equals `DOCX` | Output 2 |

---

### 節點 5a：Read Binary File（PDF 分支）

| 參數 | 值 |
|------|-----|
| Operation | Read File |
| File Path | `{{ $json["File Path"] }}` |
| Property Name | `data` |

### 節點 6a：Extract from File（PDF）

| 參數 | 值 |
|------|-----|
| Operation | Extract from PDF |
| Input Binary Field | `data` |

輸出：`$json.text`

---

### 節點 5b：Read Binary File（TXT 分支）

同上，File Path 使用 `{{ $json["File Path"] }}`

### 節點 6b：Extract from File（Text）

| 參數 | 值 |
|------|-----|
| Operation | Extract from text file |
| Input Binary Field | `data` |

---

### 節點 5c：Execute Command（DOCX 分支）

直接用 python-docx 讀取，輸出 JSON：

```
python C:\n8n-data\scripts\read_docx.py "{{ $json["File Path"] }}"
```

在後續 Code 節點解析 `$json.stdout`：
```javascript
const result = JSON.parse($json.stdout);
return [{ json: { ...$json, text: result.full_text } }];
```

---

### 節點 7：Merge（合併分支）

**節點類型：** Merge  
**Mode：** Combine  
**Combination Mode：** Multiplex

> 將三個分支的輸出合併，確保後續節點都能取到 `text` 欄位。

---

### 節點 8：OpenAI — AI 摘要分析

**Operation：** Message a Model  
**Model：** `gpt-4o-mini`

**System Prompt：**
```
You are a professional document analyst. Analyze the provided document content and return ONLY a JSON object with no explanation, no markdown, no code blocks.

Return format:
{
  "summary": "A concise 2-3 sentence summary in Traditional Chinese",
  "key_topics": "3-5 key topics separated by commas, in Traditional Chinese",
  "doc_type": "The document type (e.g., 合約, 財務報告, 會議記錄, 履歷, 採購單)"
}
```

**User Message（Expression 模式）：**
```
Please analyze this document:

File: {{ $json["File Name"] }}
Type: {{ $json["File Type"] }}

Content:
{{ $json.text.slice(0, 3000) }}
```

---

### 節點 9：Code 節點 — 解析 AI 回傳

```javascript
// 取得 AI 回傳內容
const content = $input.item.json.message.content.trim();

// 清理可能的 markdown code block
const cleaned = content
  .replace(/```json\n?/g, '')
  .replace(/```\n?/g, '')
  .trim();

// 解析 JSON
let aiResult;
try {
  aiResult = JSON.parse(cleaned);
} catch(e) {
  aiResult = {
    summary: content.slice(0, 500),
    key_topics: "解析失敗",
    doc_type: "Unknown"
  };
}

// 取得當前時間
const now = new Date();
const processTime = now.toISOString().replace('T', ' ').slice(0, 19);

return [{
  json: {
    _rowNumber:   $input.item.json._rowNumber,
    fileName:     $input.item.json["File Name"],
    filePath:     $input.item.json["File Path"],
    fileType:     $input.item.json["File Type"],
    aiSummary:    aiResult.summary || '',
    keyTopics:    aiResult.key_topics || '',
    docType:      aiResult.doc_type || '',
    processTime:  processTime,
    status:       'Done'
  }
}];
```

---

### 節點 10：Excel AI — 更新摘要結果

**Resource：** Row  
**Operation：** Update Row

| 參數 | 值 |
|------|-----|
| Input Mode | File Path |
| File Path | `C:\n8n-data\ch07\document_summary.xlsx` |
| Sheet Name | `Document Summary` |
| Row Number | `{{ $json._rowNumber }}` |
| Update Data | 見下方 JSON |

**Update Data（Expression 模式）：**
```json
{
  "AI Summary": "{{ $json.aiSummary }}",
  "Key Topics": "{{ $json.keyTopics }}",
  "Status": "{{ $json.status }}",
  "Process Time": "{{ $json.processTime }}"
}
```

---

### 節點 11：Excel AI — 寫入 Processing Log

**Resource：** Row  
**Operation：** Append Row

| 參數 | 值 |
|------|-----|
| Input Mode | File Path |
| File Path | `C:\n8n-data\ch07\document_summary.xlsx` |
| Sheet Name | `Processing Log` |
| Row Data | 見下方 JSON |

**Row Data（Expression 模式）：**
```json
{
  "Timestamp": "{{ $json.processTime }}",
  "File Name": "{{ $json.fileName }}",
  "Result": "{{ $json.status }}",
  "Error Message": ""
}
```

---

## 錯誤處理：加入 Error 分支

在 OpenAI 節點和 Excel AI 更新節點之間，建議加入錯誤分支：

在 **節點 10（Excel AI 更新）** 的 Settings → **Continue on Error** 開啟，
並在後面接一個 **IF 節點** 判斷是否有錯誤：

```javascript
// IF 條件
{{ $json.error !== undefined }}
```

**Error 分支 → Excel AI 更新 Status 為 Error：**
```json
{
  "Status": "Error",
  "Process Time": "{{ $now.toISO() }}"
}
```

---

## 執行結果預覽

執行後 `document_summary.xlsx` 的 Document Summary 工作表：

| No. | File Name | File Type | File Path | AI Summary | Key Topics | Status | Process Time |
|-----|-----------|-----------|-----------|------------|------------|--------|--------------|
| 1 | doc001.pdf | PDF | C:\...\doc001.pdf | 本文件為 2024 年 IT 服務合約，由台灣科技公司委託 Smart Solutions Inc. 提供軟體開發及雲端整合服務，合約總金額為 846,000 元，有效期 12 個月。 | 服務合約, IT 顧問, 軟體開發, 雲端整合, 付款條款 | Done | 2024-11-20 14:30:22 |
| 2 | doc002.pdf | PDF | C:\...\doc002.pdf | 2024 年第三季財務報告顯示總營收達 1,280 萬元，年增 23%，淨利率提升至 18.5%，主要受惠於企業客戶擴增與營運效率提升。 | 財務報告, Q3 2024, 營收成長, 雲端服務, 企業客戶 | Done | 2024-11-20 14:30:45 |

---

## 支援多種檔案類型

工作流程支援以下格式，只需在 Excel 清單中的 **File Type** 欄位填入對應類型：

| File Type 值 | 適用格式 | 讀取方式 |
|-------------|---------|---------|
| `PDF` | .pdf | Extract from File → PDF |
| `TXT` | .txt, .csv, .log | Extract from File → Text |
| `DOCX` | .docx | Execute Command + python-docx |

若要新增 TXT 或 DOCX 測試檔案，只需在 Excel 的 `document_summary.xlsx` 新增一行，填入對應的 File Type 和 File Path，Status 設為 `Pending`，重新執行 Workflow 即可自動處理。

---

## 常見問題

**Q：Excel AI 的 Update Row 需要什麼格式的 Row Number？**  
A：需要數字型的列號（從 1 開始，第 1 列為標題列，所以資料從第 2 列開始）。記得在 Filter Rows 時開啟 **Include Row Number**，才能取得 `_rowNumber`。

**Q：如何重新處理已完成的文件？**  
A：將 Excel 中該行的 Status 改回 `Pending`，清空 AI Summary 和 Key Topics，重新執行 Workflow。

**Q：一次可以處理多少份文件？**  
A：理論上無限制。Split in Batches 設為 1 確保穩定性；若文件量大（50+），建議改用 Schedule Trigger 分批定時執行。

**Q：OpenAI Token 費用估算？**  
A：每份 PDF 約送出 ~1000 tokens，回傳 ~300 tokens。使用 `gpt-4o-mini` 約每份文件 < NTD 0.1 元。
