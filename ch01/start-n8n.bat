@echo off
echo 正在設定 n8n 環境變數...
REM 不顯示 Deprecation 警告訊息
set NODE_NO_WARNINGS=1

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

echo 正在啟動 n8n...
npx n8n
