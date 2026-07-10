@echo off
REM 設定當前fChartEasy目錄為應用啟動路徑
cd /d %~dp0
REM 設定 Python 的環境變數
call "%~dp0\WinPython\scripts\env_for_icons.bat"  %*
REM 切換至工作目錄
cd "%~dp0\n"
REM 設定 n8n 使用者目錄的 N8N_USER_FOLDER 環境變數
set N8N_USER_FOLDER=%~dp0\n

REM 設定 n8n 所需的環境變數
set NODE_TLS_REJECT_UNAUTHORIZED=0
set N8N_COMMUNITY_PACKAGES_ALLOW_TOOL_USAGE=true
set N8N_BLOCK_ENV_ACCESS_IN_NODE=false
set N8N_GIT_NODE_DISABLE_BARE_REPOS=true
set N8N_VERSION_NOTIFICATIONS_ENABLED=false
REM 啟用 ExecuteCommand 和 LocalFileTrigger 節點
set NODES_EXCLUDE=[]
REM 設定是否允許寫入檔案（true 為禁止，false 為允許）
set N8N_BLOCK_FS_WRITE_ACCESS=false
REM 設定允許存取的資料夾路徑（若有多個路徑，請用分號 ; 隔開）
set N8N_RESTRICT_FILE_ACCESS_TO=C:\n8n-data\

REM 取得 PATH 環境變數
set "envVar=%PATH%"
REM 檢查是否沒有 Portable 版 node.exe 的搜尋路徑, 沒有搜尋路徑, 就加入在最前面...
echo %envVar% | findstr /i /c:"%~dp0\WinPython\n" > nul || set "PATH=%~dp0\WinPython\n;%envVar%"
REM 啟動 n8n
start "" "%~dp0\n\n8n.cmd"
