#!/bin/bash

echo "Setting up n8n environment variables..."
export NODE_NO_WARNINGS=1
export NODE_TLS_REJECT_UNAUTHORIZED=0
export N8N_COMMUNITY_PACKAGES_ALLOW_TOOL_USAGE=true
export N8N_BLOCK_ENV_ACCESS_IN_NODE=false
export N8N_GIT_NODE_DISABLE_BARE_REPOS=true
export N8N_VERSION_NOTIFICATIONS_ENABLED=false
export NODES_EXCLUDE="[]"
export N8N_BLOCK_FS_WRITE_ACCESS=false

export N8N_INSTANCE_OWNER_MANAGED_BY_ENV=true
export N8N_INSTANCE_OWNER_EMAIL="huanzip@gmail.com"
export N8N_INSTANCE_OWNER_PASSWORD_HASH='$2a$10$OuIaM1yk8txFhKTH2UQ6ROy8tEY6W3CVvmkhjaENKlqRBdgWs4Jp.'

# Create the n8n-data directory in home folder if it doesn't exist
mkdir -p "$HOME/n8n-data"
export N8N_RESTRICT_FILE_ACCESS_TO="$HOME/n8n-data/"

echo "Starting n8n..."
npx n8n@latest
