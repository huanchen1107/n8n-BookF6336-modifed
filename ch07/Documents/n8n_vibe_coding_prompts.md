# n8n Code 節點 AI 提示詞指南（Vibe Coding）

> 本指南提供結構化的提示詞模板，協助你使用生成式 AI 快速產生 n8n Code 節點所需的程式碼

---

## 目錄
1. [提示詞基本結構](#提示詞基本結構)
2. [n8n 環境說明模板](#n8n-環境說明模板)
3. [JavaScript 節點提示詞](#javascript-節點提示詞)
4. [Python 節點提示詞](#python-節點提示詞)
5. [常見應用場景提示詞庫](#常見應用場景提示詞庫)
6. [除錯與優化提示詞](#除錯與優化提示詞)

---

## 提示詞基本結構

### 標準提示詞框架

```
【環境說明】
我正在使用 n8n 自動化平台，需要在 Code 節點中撰寫程式碼。

【n8n Code 節點特性】
- 語言：[JavaScript / Python]
- 可用的全域物件：$input, $json, $binary, $node, $workflow, $env
- 輸入資料格式：[描述輸入資料的結構]
- 期望輸出格式：[描述期望的輸出結構]

【任務描述】
[清楚描述你要完成的任務]

【具體需求】
1. [需求項目 1]
2. [需求項目 2]
3. [需求項目 3]

【輸入範例】（如果有的話）
[提供實際的輸入資料範例]

【期望輸出範例】（如果有的話）
[提供期望的輸出資料範例]

【額外限制】
- [例如：不使用外部套件]
- [例如：需要錯誤處理]
- [例如：效能要求]
```

---

## n8n 環境說明模板

### JavaScript Code 節點環境模板

```markdown
### n8n JavaScript Code 節點環境說明

**可用的全域物件：**
- `$input.all()` - 取得所有輸入項目的陣列
- `$input.first()` - 取得第一個輸入項目
- `$input.item` - 當前處理的項目（在 Run Once for Each Item 模式）
- `$json` - 當前項目的 JSON 資料
- `$binary` - 當前項目的二進位資料

**資料結構：**
每個項目包含：
```javascript
{
  json: { /* JSON 資料 */ },
  binary: {
    data: Buffer,      // 二進位資料
    mimeType: string,  // MIME 類型
    fileName: string   // 檔案名稱
  }
}
```

**返回格式：**
必須返回陣列，每個元素是一個包含 json 和/或 binary 的物件：
```javascript
return [
  {
    json: { /* 資料 */ },
    binary: { /* 二進位資料 */ }
  }
];
```

**可用的 Node.js 模組：**
- 內建模組：fs, path, crypto, buffer 等
- 已安裝的 npm 套件（需事先在 n8n 環境安裝）

**不可使用：**
- localStorage / sessionStorage
- window / document（非瀏覽器環境）
```

### Python Code 節點環境模板

```markdown
### n8n Python Code 節點環境說明

**可用的全域物件：**
- `items` - 輸入項目的列表
- 每個項目的結構：
  ```python
  {
    'json': {},      # JSON 資料
    'binary': {}     # 二進位資料
  }
  ```

**存取資料：**
```python
# 取得第一個項目的 JSON 資料
first_item = items[0]['json']

# 取得二進位資料
binary_data = items[0]['binary']['data']
```

**返回格式：**
必須返回列表：
```python
return [
  {
    'json': { /* 資料 */ },
    'binary': { /* 二進位資料 */ }
  }
]
```

**可用的 Python 模組：**
- 標準庫：json, re, datetime, base64, hashlib 等
- 已安裝的第三方套件（需事先在 n8n 環境安裝）
```

---

## JavaScript 節點提示詞

### 1. 資料格式轉換

#### CSV 轉 JSON

```
我正在使用 n8n 的 JavaScript Code 節點，需要將 CSV 檔案轉換為 JSON 格式。

【輸入資料】
- 來源：$input.first().binary.data（Buffer 格式的 CSV 檔案）
- CSV 格式：第一行是標題，後續是資料行
- 編碼：UTF-8

【任務需求】
1. 讀取 CSV 內容並解析
2. 將第一行作為欄位名稱（header）
3. 將每一行資料轉換為 JSON 物件
4. 處理可能的空白字元和空行
5. 返回 JSON 陣列

【輸入範例】
```
姓名,年齡,Email
張三,25,zhang@example.com
李四,30,li@example.com
```

【期望輸出】
```json
[
  {"姓名": "張三", "年齡": "25", "Email": "zhang@example.com"},
  {"姓名": "李四", "年齡": "30", "Email": "li@example.com"}
]
```

【注意事項】
- 不使用外部 CSV 解析套件（使用原生字串處理）
- 需要處理欄位中可能包含逗號的情況（用引號包圍）
- 加入錯誤處理
```

#### JSON 轉 Excel

```
我需要在 n8n JavaScript Code 節點中，將 JSON 資料轉換為 Excel 檔案。

【環境】
- 已安裝套件：xlsx
- 輸入：$input.first().json.data（JSON 陣列）
- 輸出：Excel 檔案的 Buffer

【任務需求】
1. 使用 xlsx 套件將 JSON 轉為 Excel
2. 設定工作表名稱為 "Data"
3. 自動調整欄位寬度
4. 第一行設為標題（粗體）
5. 返回 Excel 檔案的 Buffer

【輸入範例】
```json
[
  {"產品": "筆記型電腦", "價格": 30000, "庫存": 15},
  {"產品": "滑鼠", "價格": 500, "庫存": 100}
]
```

【輸出要求】
返回包含 binary 資料的物件：
- mimeType: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
- fileName: 'output.xlsx'
```

### 2. 資料處理與清理

#### 資料去重

```
在 n8n JavaScript Code 節點中，我需要對資料進行去重處理。

【輸入資料】
- 來源：$input.all()（多個項目的陣列）
- 每個項目包含 json 物件，其中有 id 欄位

【任務需求】
1. 根據 id 欄位進行去重
2. 如果有重複的 id，保留第一次出現的記錄
3. 統計去重前後的數量
4. 返回去重後的資料陣列

【範例輸入】
```javascript
[
  {json: {id: 1, name: "A"}},
  {json: {id: 2, name: "B"}},
  {json: {id: 1, name: "C"}},  // 重複
  {json: {id: 3, name: "D"}}
]
```

【期望輸出】
返回去重後的陣列，並在第一個項目的 json 中加入統計資訊：
```javascript
{
  json: {
    deduplicatedData: [...],
    statistics: {
      originalCount: 4,
      deduplicatedCount: 3,
      removedCount: 1
    }
  }
}
```
```

#### 資料驗證

```
我需要在 n8n JavaScript Code 節點中驗證資料的完整性和格式。

【輸入資料】
來源：$input.first().json.records（物件陣列）

【驗證規則】
1. 必填欄位：name, email, phone
2. Email 格式驗證（正規表達式）
3. 電話格式驗證（台灣手機號碼：09 開頭 10 碼）
4. 年齡範圍：0-120

【任務需求】
1. 遍歷所有記錄進行驗證
2. 將記錄分為 valid 和 invalid 兩類
3. 對於無效記錄，列出所有錯誤訊息
4. 返回驗證報告

【輸出格式】
```javascript
{
  json: {
    summary: {
      total: 10,
      valid: 8,
      invalid: 2,
      validRate: "80%"
    },
    validRecords: [...],
    invalidRecords: [
      {
        record: {...},
        errors: ["Email 格式錯誤", "電話格式錯誤"]
      }
    ]
  }
}
```
```

### 3. 檔案處理

#### 批量重命名檔案

```
在 n8n JavaScript Code 節點中，我需要批量重命名檔案。

【輸入資料】
- 來源：$input.all()
- 每個項目包含檔案路徑：item.json.filePath

【重命名規則】
1. 格式：YYYY-MM-DD_原始檔名.副檔名
2. 日期使用當前日期
3. 移除檔名中的空格，替換為底線
4. 轉換為小寫

【任務需求】
1. 使用 Node.js fs 模組執行重命名
2. 檢查新檔名是否已存在，若存在則加上編號 (1), (2)...
3. 記錄重命名成功和失敗的檔案
4. 返回處理結果

【範例】
輸入：`/path/to/My Document.pdf`
輸出：`/path/to/2025-11-08_my_document.pdf`

【輸出格式】
返回包含處理結果的物件，包括成功、失敗列表
```

#### 圖片壓縮

```
我需要在 n8n JavaScript Code 節點中使用 sharp 套件壓縮圖片。

【環境】
- 已安裝：sharp
- 輸入：$input.all()，每個項目的 binary.data 是圖片 Buffer

【任務需求】
1. 壓縮為 JPEG 格式，品質 80%
2. 如果圖片寬度超過 1920px，等比例縮放
3. 啟用漸進式 JPEG
4. 計算並記錄壓縮率
5. 保留原始檔名，但改為 .jpg 副檔名

【輸出格式】
返回壓縮後的圖片 Buffer，並在 json 中記錄：
- originalSize（原始大小，bytes）
- compressedSize（壓縮後大小，bytes）
- compressionRatio（壓縮率，百分比）
- originalWidth, originalHeight
- newWidth, newHeight

【效能要求】
- 需要處理的圖片數量可能很多，使用 async/await 確保穩定性
```

### 4. 文字處理

#### Markdown 轉 HTML

```
在 n8n JavaScript Code 節點中，我需要將 Markdown 轉換為 HTML。

【環境】
- 可選套件：marked（如果已安裝）
- 如果未安裝，請使用簡易版本的 Markdown 解析

【輸入資料】
- 來源：$input.first().binary.data（Buffer 格式的 Markdown 檔案）
- 編碼：UTF-8

【任務需求】
1. 解析 Markdown 語法：
   - 標題 (# ## ###)
   - 粗體 (**text** 或 __text__)
   - 斜體 (*text* 或 _text_)
   - 連結 [text](url)
   - 圖片 ![alt](url)
   - 程式碼區塊 ```language\ncode\n```
   - 行內程式碼 `code`
   - 清單 (- 或 1.)
2. 加入基本 CSS 樣式
3. 產生完整的 HTML 文件結構

【輸出格式】
返回 HTML 檔案的 Buffer：
- mimeType: 'text/html'
- fileName: 原始檔名.html

【CSS 樣式要求】
- 使用 sans-serif 字體
- 最大寬度 800px，置中
- 程式碼區塊使用淺灰背景
- 響應式設計
```

#### 文字搜尋與替換

```
我需要在 n8n JavaScript Code 節點中進行批量文字搜尋與替換。

【輸入資料】
- 檔案內容：$input.all()，每個項目的 binary.data 是文字檔案
- 替換規則：$input.first().json.rules（陣列）

【替換規則格式】
```javascript
[
  {search: "old_text", replace: "new_text", caseSensitive: true},
  {search: "pattern", replace: "replacement", regex: true}
]
```

【任務需求】
1. 支援一般文字替換
2. 支援正規表達式替換
3. 支援大小寫敏感/不敏感
4. 統計每個規則的替換次數
5. 保留原始檔案編碼（UTF-8）

【輸出格式】
返回處理後的文字檔案，並在 json 中記錄：
- fileName
- totalReplacements（總替換次數）
- replacementDetails（每個規則的替換次數）
```

### 5. 資料分析

#### 統計分析

```
在 n8n JavaScript Code 節點中，我需要對數值資料進行統計分析。

【輸入資料】
- 來源：$input.first().json.data（數值陣列）
- 或：$input.all()，從每個項目的特定欄位提取數值

【分析項目】
1. 基本統計：
   - 總數（count）
   - 總和（sum）
   - 平均值（mean）
   - 中位數（median）
   - 眾數（mode）
2. 離散程度：
   - 最小值（min）
   - 最大值（max）
   - 範圍（range）
   - 標準差（standard deviation）
   - 四分位數（Q1, Q2, Q3）
3. 其他：
   - 異常值檢測（使用 IQR 方法）

【任務需求】
1. 計算所有統計指標
2. 識別並列出異常值
3. 四捨五入到小數點後 2 位

【輸出格式】
```javascript
{
  json: {
    statistics: {
      count: 100,
      sum: 5000,
      mean: 50.00,
      median: 48.50,
      // ... 其他統計值
    },
    outliers: [120, 135],  // 異常值列表
    dataRange: "10 - 100"
  }
}
```
```

#### 資料分組與聚合

```
我需要在 n8n JavaScript Code 節點中對資料進行分組和聚合。

【輸入資料】
- 來源：$input.first().json.records（物件陣列）

【任務需求】
1. 根據指定欄位分組（例如：category）
2. 對每組進行聚合計算：
   - 計數（count）
   - 總和（sum）
   - 平均值（average）
   - 最大值（max）
   - 最小值（min）
3. 可以使用 lodash（如果已安裝）
4. 排序結果（依計數或其他指標）

【範例輸入】
```javascript
[
  {category: "電子", price: 1000, quantity: 5},
  {category: "電子", price: 500, quantity: 10},
  {category: "食品", price: 100, quantity: 20}
]
```

【期望輸出】
```javascript
{
  json: {
    groupedData: {
      "電子": {
        count: 2,
        totalPrice: 1500,
        avgPrice: 750,
        totalQuantity: 15
      },
      "食品": {
        count: 1,
        totalPrice: 100,
        avgPrice: 100,
        totalQuantity: 20
      }
    }
  }
}
```
```

---

## Python 節點提示詞

### 1. 資料處理

#### Pandas 資料清理

```
我正在使用 n8n 的 Python Code 節點，需要用 pandas 清理資料。

【環境】
- Python 3.x
- 已安裝：pandas, numpy
- 輸入：items[0]['json']['data']（字典列表）

【任務需求】
1. 將輸入轉換為 pandas DataFrame
2. 資料清理步驟：
   - 移除完全重複的行
   - 處理缺失值（數值欄位填 0，文字欄位填 "N/A"）
   - 移除空白字元（strip）
   - 轉換日期格式為 YYYY-MM-DD
   - 標準化欄位名稱（小寫、底線）
3. 轉換回字典列表並返回

【輸入範例】
```python
[
  {"Name": " John ", "Age": 25, "Date": "2024/01/15"},
  {"Name": "Jane", "Age": None, "Date": "2024-02-20"},
  {"Name": " John ", "Age": 25, "Date": "2024/01/15"}  # 重複
]
```

【期望輸出】
返回清理後的資料，包含統計資訊：
- 清理後的記錄數
- 移除的重複行數
- 處理的缺失值數量
```

#### 正規表達式批量處理

```
在 n8n Python Code 節點中，我需要使用正規表達式處理文字資料。

【輸入資料】
- 來源：items（列表）
- 每個項目的 json['text'] 包含需要處理的文字

【任務需求】
1. 提取所有 Email 地址
2. 提取所有電話號碼（台灣格式：02-1234-5678 或 0912-345-678）
3. 提取所有 URL
4. 提取所有日期（YYYY-MM-DD, YYYY/MM/DD, DD-MM-YYYY）
5. 遮罩敏感資訊（Email 顯示前 3 碼，電話顯示後 4 碼）

【輸出格式】
```python
{
  'json': {
    'extracted': {
      'emails': ['user@example.com', ...],
      'phones': ['0912-345-678', ...],
      'urls': ['https://example.com', ...],
      'dates': ['2024-01-15', ...]
    },
    'maskedText': '聯絡我：use***@example.com 或 ****-345-678'
  }
}
```

【注意事項】
- 使用 Python re 模組
- 確保正規表達式的效能
```

### 2. 檔案處理

#### Excel 多工作表處理

```
我需要在 n8n Python Code 節點中處理多工作表的 Excel 檔案。

【環境】
- 已安裝：pandas, openpyxl
- 輸入：items[0]['binary']['data']（Excel 檔案的 bytes）

【任務需求】
1. 讀取所有工作表
2. 對每個工作表：
   - 提取第一列作為欄位名稱
   - 過濾空行
   - 計算每個工作表的記錄數
3. 合併所有工作表的資料（加入來源工作表名稱欄位）
4. 生成摘要報告

【輸出格式】
```python
{
  'json': {
    'summary': {
      'totalSheets': 3,
      'sheetNames': ['Sheet1', 'Sheet2', 'Sheet3'],
      'totalRecords': 150
    },
    'combinedData': [...]  # 所有資料
  }
}
```
```

#### PDF 文字提取與分析

```
在 n8n Python Code 節點中，我需要提取 PDF 文字並進行分析。

【環境】
- 已安裝：PyPDF2 或 pdfplumber
- 輸入：items[0]['binary']['data']（PDF 檔案的 bytes）

【任務需求】
1. 提取所有頁面的文字內容
2. 文字分析：
   - 總字數（中英文分別計算）
   - 總頁數
   - 提取所有標題（假設字體較大或有特定格式）
   - 提取關鍵字（高頻詞彙，排除停用詞）
3. 建立目錄（如果有）
4. 提取表格資料（如果有）

【輸出格式】
```python
{
  'json': {
    'metadata': {
      'totalPages': 10,
      'totalWords': 5000,
      'chineseChars': 3000,
      'englishWords': 500
    },
    'content': '...',  # 完整文字
    'tableOfContents': [...],
    'keywords': ['關鍵字1', '關鍵字2', ...],
    'tables': [...]  # 表格資料
  }
}
```
```

### 3. 資料分析與機器學習

#### 時間序列分析

```
我需要在 n8n Python Code 節點中進行時間序列資料分析。

【環境】
- 已安裝：pandas, numpy, scipy
- 輸入：items[0]['json']['timeSeries']（時間序列資料）

【資料格式】
```python
[
  {"date": "2024-01-01", "value": 100},
  {"date": "2024-01-02", "value": 105},
  ...
]
```

【任務需求】
1. 計算移動平均（7天、30天）
2. 檢測趨勢（上升/下降/持平）
3. 計算變化率（日變化、週變化）
4. 識別異常值（使用 Z-score 方法）
5. 預測未來 7 天的趨勢（簡單線性迴歸）

【輸出格式】
包含分析結果和視覺化資料（供後續節點繪圖使用）
```

#### 文字相似度比較

```
在 n8n Python Code 節點中，我需要比較多個文字的相似度。

【環境】
- 可用套件：difflib（標準庫）或 sklearn（如果已安裝）
- 輸入：items（列表），每個項目包含 json['text']

【任務需求】
1. 計算所有文字兩兩之間的相似度（使用餘弦相似度或 Levenshtein 距離）
2. 找出最相似的文字對
3. 進行文字分群（相似度 > 80% 的歸為一組）
4. 提取每組的代表性關鍵字

【輸出格式】
```python
{
  'json': {
    'similarityMatrix': [[1.0, 0.85, 0.3], ...],
    'clusters': [
      {
        'id': 1,
        'texts': [0, 1],  # 文字索引
        'keywords': ['關鍵字1', '關鍵字2']
      }
    ],
    'mostSimilarPairs': [
      {'text1': 0, 'text2': 1, 'similarity': 0.95}
    ]
  }
}
```
```

---

## 常見應用場景提示詞庫

### 場景 1：CSV 資料清理與標準化

**完整提示詞：**

```
【任務】在 n8n JavaScript Code 節點中清理和標準化 CSV 資料

【環境】
- 輸入：$input.first().binary.data（Buffer 格式的 CSV）
- 無外部套件依賴（使用原生 JavaScript）

【資料問題】
1. 欄位名稱不一致（有空格、大小寫不統一）
2. 資料中有多餘的空白字元
3. 日期格式不統一（YYYY-MM-DD, YYYY/MM/DD, DD/MM/YYYY）
4. 電話號碼格式不統一（有破折號、括號、空格）
5. 有空行和重複行
6. 數值欄位混有文字（如 "1,000" 或 "$100"）

【清理步驟】
1. 標準化欄位名稱：
   - 轉小寫
   - 空格替換為底線
   - 移除特殊字元
2. 清理資料值：
   - Trim 所有文字欄位
   - 統一日期格式為 YYYY-MM-DD
   - 統一電話格式為 XXXX-XXX-XXX
   - 數值欄位移除非數字字元並轉換為數字
3. 移除空行和完全重複的行
4. 驗證必填欄位（name, email）

【輸出要求】
返回包含兩個項目的陣列：
1. 清理後的資料（JSON 格式）
2. 清理報告（統計資訊）

【報告內容】
- 原始記錄數
- 清理後記錄數
- 移除的重複行數
- 移除的空行數
- 無效記錄數（及原因）
- 每個欄位的清理統計

請提供完整的程式碼，包含詳細註解。
```

### 場景 2：圖片批量處理（壓縮 + 縮圖 + 浮水印）

**完整提示詞：**

```
【任務】在 n8n JavaScript Code 節點中批量處理圖片

【環境】
- 已安裝：sharp
- 輸入：$input.all()，每個項目的 binary.data 是圖片 Buffer
- 浮水印圖片：$input.first().json.watermarkPath

【處理需求】
1. **壓縮**：
   - JPEG 格式，品質 85%
   - 啟用漸進式編碼
   - 移除 EXIF 資料（隱私保護）

2. **縮放**：
   - 如果寬度 > 2000px，縮放到 2000px
   - 如果高度 > 2000px，縮放到 2000px
   - 保持寬高比

3. **生成縮圖**：
   - 小：200x200px（裁切）
   - 中：600x600px（等比縮放）
   - 大：1200x1200px（等比縮放）

4. **浮水印**：
   - 位置：右下角
   - 偏移：距離邊緣 20px
   - 不透明度：70%
   - 只在原圖加浮水印，縮圖不加

【輸出格式】
每張原圖返回 4 個檔案：
1. 原圖壓縮版（含浮水印）
2. 小縮圖
3. 中縮圖
4. 大縮圖

每個輸出項目包含：
```javascript
{
  json: {
    originalFileName: "photo.jpg",
    type: "original|small|medium|large",
    originalSize: 5242880,  // bytes
    compressedSize: 1048576,
    compressionRatio: "80%",
    dimensions: {width: 2000, height: 1500}
  },
  binary: {
    data: Buffer,
    mimeType: "image/jpeg",
    fileName: "photo_original.jpg"
  }
}
```

【效能要求】
- 使用 async/await 確保記憶體不溢出
- 每處理 10 張圖片顯示進度
- 錯誤處理：單張圖片失敗不影響其他圖片

請提供完整程式碼，包含錯誤處理和進度追蹤。
```

### 場景 3：多來源資料整合與比對

**完整提示詞：**

```
【任務】在 n8n JavaScript Code 節點中整合和比對多個資料來源

【輸入資料】
1. CRM 資料：$input.first().json.crmData（客戶資料）
2. ERP 資料：$input.first().json.erpData（訂單資料）
3. Email 資料：$input.first().json.emailData（郵件互動記錄）

【資料結構】
```javascript
// CRM
[{customerId: "C001", name: "張三", email: "zhang@example.com", phone: "0912345678"}]

// ERP
[{orderId: "O001", customerId: "C001", amount: 10000, date: "2024-01-15"}]

// Email
[{email: "zhang@example.com", openCount: 5, clickCount: 2, lastOpen: "2024-01-20"}]
```

【整合需求】
1. 以 customerId 為主鍵整合 CRM 和 ERP
2. 以 email 為次要鍵整合 Email 資料
3. 處理資料不匹配的情況：
   - CRM 有但 ERP 沒有的客戶（標記為"無訂單"）
   - ERP 有但 CRM 沒有的訂單（標記為"異常訂單"）
   - Email 無法匹配的記錄（標記為"Email 不符"）

【分析需求】
1. 客戶價值分級：
   - VIP：訂單總額 > 50000
   - 重要：訂單總額 10000-50000
   - 一般：訂單總額 < 10000
   - 潛在：有互動但無訂單
2. 客戶活躍度：
   - 活躍：最近 30 天有互動或訂單
   - 沉睡：30-90 天無互動
   - 流失：90 天以上無互動

【輸出格式】
```javascript
{
  json: {
    integratedData: [
      {
        customerId: "C001",
        customerInfo: {...},
        orders: [...],
        emailStats: {...},
        valueLevel: "VIP",
        activeStatus: "活躍",
        totalAmount: 50000,
        orderCount: 5
      }
    ],
    summary: {
      totalCustomers: 100,
      vipCount: 10,
      activeCount: 60,
      anomalies: {
        unmatchedOrders: 3,
        unmatchedEmails: 5
      }
    },
    anomalies: [
      {type: "unmatchedOrder", data: {...}}
    ]
  }
}
```

請提供完整程式碼，使用 lodash 優化效能。
```

### 場景 4：影片字幕處理（SRT 解析、翻譯、合併）

**完整提示詞：**

```
【任務】在 n8n JavaScript Code 節點中處理 SRT 字幕檔案

【輸入資料】
- 原始字幕：$input.first().binary.data（SRT 格式 Buffer）
- 翻譯字幕：$input.item(1).binary.data（另一個 SRT 檔案）
- 時間調整：$input.first().json.timeOffset（秒數，可正可負）

【處理步驟】
1. **解析 SRT**：
   - 提取序號、時間軸、文字內容
   - 處理多行字幕
   - 處理特殊格式（HTML 標籤、位置標記）

2. **時間軸調整**：
   - 根據 timeOffset 調整所有時間戳
   - 確保時間不會變成負數
   - 保持時間格式 HH:MM:SS,mmm

3. **字幕合併**（雙語字幕）：
   - 原文在上，譯文在下
   - 確保時間軸對齊
   - 如果時間不完全匹配，找最接近的字幕配對

4. **字幕清理**：
   - 移除廣告字幕（包含特定關鍵字）
   - 移除重複字幕
   - 合併過短的字幕片段（< 1 秒）

【SRT 格式範例】
```
1
00:00:01,000 --> 00:00:03,500
這是第一段字幕

2
00:00:04,000 --> 00:00:07,000
這是第二段字幕
可以有多行
```

【輸出格式】
返回三個 binary 檔案：
1. 調整後的原始字幕
2. 調整後的翻譯字幕
3. 合併的雙語字幕

每個檔案的 json 包含：
```javascript
{
  fileName: "output.srt",
  subtitleCount: 150,
  totalDuration: "01:30:45",
  removedCount: 5,  // 清理掉的字幕數
  adjustedBy: "+3.5s"  // 時間調整量
}
```

請提供完整程式碼，包含時間計算函數和清理邏輯。
```

### 場景 5：Excel 報表自動生成（含圖表）

**完整提示詞：**

```
【任務】在 n8n JavaScript Code 節點中生成含圖表的 Excel 報表

【環境】
- 已安裝：xlsx, exceljs（選其一，推薦 exceljs）
- 輸入：$input.first().json.salesData（銷售資料陣列）

【資料格式】
```javascript
[
  {date: "2024-01-01", product: "產品A", category: "電子", sales: 10000, quantity: 5},
  {date: "2024-01-02", product: "產品B", category: "食品", sales: 5000, quantity: 20},
  ...
]
```

【報表需求】
1. **工作表結構**：
   - Sheet1: 原始資料
   - Sheet2: 依日期彙總
   - Sheet3: 依產品彙總
   - Sheet4: 依類別彙總
   - Sheet5: 圖表與分析

2. **格式要求**：
   - 標題列：粗體、背景色、凍結窗格
   - 數值格式：千分位、貨幣符號
   - 日期格式：YYYY-MM-DD
   - 自動調整欄寬
   - 交替行背景色（斑馬線）

3. **彙總計算**：
   - 每個彙總表包含：
     - 總銷售額
     - 平均銷售額
     - 最高/最低銷售額
     - 銷售佔比
     - 成長率（與前期比較）

4. **圖表**（Sheet5）：
   - 圓餅圖：類別銷售佔比
   - 長條圖：各產品銷售額
   - 折線圖：日銷售趨勢
   - 表格：Top 10 產品

5. **條件格式**：
   - 銷售額 > 50000：綠色背景
   - 銷售額 < 10000：紅色背景
   - 數量 < 5：橘色警告

【輸出格式】
```javascript
{
  binary: {
    data: Buffer,  // Excel 檔案
    mimeType: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    fileName: 'sales_report_2024.xlsx'
  },
  json: {
    summary: {
      totalRows: 1000,
      totalSales: 5000000,
      dateRange: "2024-01-01 to 2024-12-31",
      categories: 5,
      products: 50
    }
  }
}
```

請提供使用 exceljs 的完整程式碼，包含所有圖表和格式設定。
```

---

## 除錯與優化提示詞

### 除錯提示詞模板

```
【除錯請求】我的 n8n Code 節點執行時遇到錯誤

【環境】
- 語言：[JavaScript / Python]
- n8n 版本：[版本號]
- Node.js 版本：[版本號]（如果是 JavaScript）

【原始程式碼】
```[語言]
[貼上你的程式碼]
```

【錯誤訊息】
```
[完整的錯誤訊息]
```

【輸入資料範例】
```json
[提供實際的輸入資料]
```

【預期行為】
[描述你期望的結果]

【實際行為】
[描述實際發生的情況]

【已嘗試的解決方法】
1. [方法 1]
2. [方法 2]

請幫我找出問題並提供修正後的程式碼。
```

### 效能優化提示詞

```
【優化請求】我的 n8n Code 節點執行速度很慢

【目前程式碼】
```javascript
[貼上程式碼]
```

【效能問題】
- 處理時間：[例如：處理 1000 筆資料需要 30 秒]
- 記憶體使用：[如果知道的話]
- 資料量：[輸入資料的規模]

【優化目標】
- 期望處理時間：[例如：< 5 秒]
- 記憶體限制：[如果有的話]

【限制條件】
- 不能使用的套件：[列出限制]
- 必須保留的功能：[列出核心功能]

請提供優化建議和改進後的程式碼，並說明優化原理。
```

### 程式碼重構提示詞

```
【重構請求】請幫我重構這段程式碼，使其更易維護

【目前程式碼】
```javascript
[貼上程式碼]
```

【問題】
- 程式碼重複
- 可讀性差
- 難以擴展
- [其他問題]

【重構目標】
1. 提高可讀性（清楚的變數名、適當的註解）
2. 減少重複程式碼（DRY 原則）
3. 模組化（分離關注點）
4. 錯誤處理（完善的 try-catch）
5. 易於擴展（方便新增功能）

【編碼風格偏好】
- [例如：使用 async/await 而非 Promise.then]
- [例如：偏好函數式編程]

請提供重構後的程式碼，並說明改進之處。
```

---

## 進階技巧：提示詞優化

### 1. 提供足夠的上下文

**不好的提示詞：**
```
寫一個 n8n 程式碼處理資料
```

**好的提示詞：**
```
在 n8n JavaScript Code 節點中，處理來自前一個節點的 JSON 資料。
輸入資料包含 100 個客戶記錄，每個記錄有 name、email、phone 欄位。
我需要驗證 email 格式，並將無效記錄分離出來。
請返回兩個陣列：validRecords 和 invalidRecords。
```

### 2. 分步驟描述複雜任務

```
【任務】批量處理訂單資料並生成報表

【第一步】資料載入與驗證
- 從 $input.all() 讀取訂單資料
- 驗證必填欄位：orderId, customerId, amount, date
- 驗證資料型別：amount 必須是數字，date 必須是有效日期

【第二步】資料轉換
- 統一日期格式為 YYYY-MM-DD
- 金額四捨五入到小數點後 2 位
- 計算每筆訂單的稅金（amount * 0.05）

【第三步】資料聚合
- 依客戶 ID 分組
- 計算每個客戶的總訂單數、總金額、平均金額

【第四步】報表生成
- 生成 CSV 格式的彙總報表
- 包含欄位：客戶 ID、訂單數、總金額、平均金額、客戶等級

【第五步】錯誤處理
- 記錄所有驗證失敗的訂單
- 返回處理成功率和失敗原因

請依照這些步驟提供完整程式碼，每個步驟加上註解。
```

### 3. 使用範例驅動開發

```
【任務】解析複雜的日誌檔案

【範例輸入】
```
[2024-01-15 10:30:45] INFO: User login successful - UserID: 12345
[2024-01-15 10:31:20] ERROR: Database connection failed - Code: 500
[2024-01-15 10:32:10] WARNING: High memory usage - 85%
```

【範例輸出】
```javascript
[
  {
    timestamp: "2024-01-15 10:30:45",
    level: "INFO",
    message: "User login successful",
    details: {UserID: "12345"}
  },
  {
    timestamp: "2024-01-15 10:31:20",
    level: "ERROR",
    message: "Database connection failed",
    details: {Code: "500"}
  },
  {
    timestamp: "2024-01-15 10:32:10",
    level: "WARNING",
    message: "High memory usage",
    details: {percentage: "85%"}
  }
]
```

請提供能解析這種格式的程式碼，使用正規表達式提取資訊。
```

### 4. 指定程式碼風格

```
【任務】處理使用者輸入資料

【程式碼風格要求】
1. 使用 ES6+ 語法（箭頭函數、解構賦值、模板字串）
2. 優先使用 const，避免 var
3. 使用 async/await 而非 .then()
4. 函數式編程風格（map, filter, reduce）
5. 詳細的 JSDoc 註解
6. 每個函數不超過 20 行

【命名規範】
- 變數：camelCase
- 常數：UPPER_SNAKE_CASE
- 函數：動詞開頭（get, set, calculate, validate）
- 布林值：is, has, should 開頭

請提供符合這些規範的程式碼。
```

---

## 快速參考：常用程式碼片段請求

### JavaScript 快速請求

```
// 1. 陣列去重
"寫一個 n8n JavaScript 函數，根據 id 欄位對 $input.all() 的資料去重"

// 2. 深度複製物件
"在 n8n Code 節點中深度複製物件，不使用外部套件"

// 3. CSV 解析
"寫一個簡單的 CSV 解析器，處理引號包圍的欄位和跳脫字元"

// 4. 日期格式轉換
"寫一個函數將各種日期格式（YYYY-MM-DD, DD/MM/YYYY, MM-DD-YYYY）統一轉換為 ISO 8601"

// 5. 檔案路徑處理
"提取檔案路徑的目錄、檔名、副檔名，不使用 path 模組"

// 6. 資料分頁
"將陣列資料分頁，每頁 50 筆，返回指定頁面的資料"

// 7. 字串模糊搜尋
"實作 Levenshtein 距離演算法，用於模糊比對字串"

// 8. 物件陣列排序
"對物件陣列進行多欄位排序（先依 date 降序，再依 amount 升序）"

// 9. 遞迴處理巢狀物件
"遞迴遍歷巢狀物件，將所有字串值轉為大寫"

// 10. 批次處理
"將 1000 筆資料分批處理，每批 100 筆，避免記憶體溢出"
```

### Python 快速請求

```
// 1. DataFrame 操作
"用 pandas 讀取 JSON，過濾、分組、聚合，返回結果"

// 2. 正規表達式批次替換
"用 re 模組批次處理文字，替換多個模式"

// 3. 檔案批次重命名
"用 os 模組批次重命名資料夾中的檔案"

// 4. Excel 多工作表讀寫
"用 pandas 和 openpyxl 讀取多個工作表，處理後寫入新檔案"

// 5. 圖片處理
"用 PIL 批次調整圖片大小並加浮水印"

// 6. JSON 深度合併
"遞迴合併多個巢狀 JSON 物件"

// 7. 資料清理
"清理 DataFrame 中的缺失值、異常值、重複值"

// 8. 文字分析
"分析文字的詞頻、提取關鍵字、生成詞雲資料"

// 9. 時間序列處理
"用 pandas 處理時間序列，計算移動平均、變化率"

// 10. 批次 API 請求
"使用 requests 批次呼叫 API，加上重試機制和速率限制"
```

---

## 提示詞檢查清單

在提交提示詞之前，檢查是否包含：

- [ ] 明確的任務描述
- [ ] n8n 環境說明（JavaScript/Python）
- [ ] 輸入資料格式和來源
- [ ] 期望的輸出格式
- [ ] 具體的處理步驟或邏輯
- [ ] 範例資料（輸入和輸出）
- [ ] 錯誤處理要求
- [ ] 效能或限制條件
- [ ] 程式碼風格偏好（如果有）
- [ ] 是否需要詳細註解

---

## 實戰範例：完整對話流程

### 範例對話

**你的初次提示：**
```
我需要在 n8n JavaScript Code 節點中處理客戶資料。
輸入是 CSV 檔案，包含姓名、Email、電話、地址。
我要驗證資料並輸出清理後的 JSON。
```

**AI 可能的回應：**
```
我需要更多資訊來幫你寫出準確的程式碼：

1. CSV 檔案如何輸入？($input.first().binary.data?)
2. 驗證規則是什麼？（Email 格式？電話格式？）
3. 如果資料無效要如何處理？（跳過？記錄錯誤？）
4. 期望的 JSON 結構是什麼？
5. 是否需要去重？
6. 資料量大概多少？（影響效能考量）
```

**你的補充說明：**
```
1. 輸入：$input.first().binary.data（UTF-8 編碼的 CSV）
2. 驗證規則：
   - Email 必須符合標準格式
   - 電話必須是台灣手機（09 開頭 10 碼）或市話
   - 姓名和地址不可為空
3. 無效資料要分離出來，並記錄錯誤原因
4. 輸出 JSON：
   ```javascript
   {
     validRecords: [...],
     invalidRecords: [{record: {...}, errors: [...]}],
     summary: {total: 100, valid: 85, invalid: 15}
   }
   ```
5. 需要根據 Email 去重，保留第一筆
6. 資料量約 1000-5000 筆

請提供完整程式碼，包含詳細註解和錯誤處理。
```

**AI 提供完整程式碼**

---

## 結語

使用這份提示詞指南，你可以：
1. 快速生成高品質的 n8n Code 節點程式碼
2. 減少來回溝通的次數
3. 獲得更準確、更符合需求的程式碼
4. 學習如何更好地與 AI 協作

記住：**提示詞越詳細，AI 的輸出越準確**。不要吝嗇提供範例和上下文！