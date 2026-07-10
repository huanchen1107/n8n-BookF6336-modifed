# n8n Excel Automation Course

Welcome to the modified n8n workflows repository! This project contains various n8n workflow examples (JSON files) designed to automate Excel tasks and more.

## Installation & Setup

To get started, you need to have [Node.js](https://nodejs.org/) installed on your machine.

### 1. Start the n8n Server
We have provided a cross-platform setup script that automatically sets up your administrator credentials and runs the latest version of n8n.

**For macOS / Linux:**
Open your terminal in this repository's folder and run:
```bash
./ch01/start-n8n.sh
```
*(Note: The initial start might take a few minutes as it downloads the latest n8n packages).*

**For Windows:**
You can run the provided batch file:
```cmd
.\ch01\1_n8n_server.bat
```

### 2. Log in to n8n
Once the server has started, open your web browser and go to:
👉 **http://localhost:5678**

Log in using the pre-configured credentials:
* **Email:** `huanzip@gmail.com`
* **Password:** `n8n`

---

## Getting Started: Importing an Example Workflow

n8n workflows are stored as JSON files. You can easily import any example from this repository into your local n8n instance. 

Let's use **`ch2-2-1.json`** as an example.

### Option A: Import via File Upload
1. In the n8n dashboard, click **Workflows** on the left menu, then click **Add Workflow**.
2. Click the **Options (⋮)** menu in the top right corner.
3. Select **Import from File**.
4. Navigate to this repository's folder and select `ch02/ch2-2-1.json`.

### Option B: Copy & Paste
1. Open `ch02/ch2-2-1.json` in a text editor (like VS Code, Notepad, or TextEdit).
2. Copy all the JSON text (`Cmd+C` or `Ctrl+C`).
3. Go to your n8n workflow canvas and simply paste it (`Cmd+V` or `Ctrl+V`). The nodes will automatically appear!

### ⚠️ Important Note on File Paths
Many workflows in this repository (such as `ch2-2-1.json`) interact with your local file system. 
Because operating systems have different path formats, make sure to update the paths in the nodes to match your machine before running them!
* **Windows Example:** `C:/n8n-data/`
* **macOS/Linux Example:** `/Users/your_username/n8n-data/`
