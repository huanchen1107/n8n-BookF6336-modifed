# Chapter 1: n8n Installation & Setup Log

This document records the steps and troubleshooting taken to successfully set up n8n for this repository on a macOS environment.

## 1. Initial Challenge
The original repository provided a Windows Batch file (`ch01/1_n8n_server.bat`) to start the n8n server. This script contained environment variables for basic authentication and started an older, globally installed n8n version. Since macOS cannot natively run `.bat` files, a new approach was required.

## 2. Creating a macOS-Compatible Startup Script
We created a new shell script (`ch01/start-n8n.sh`) to handle the server startup on macOS and Linux systems. 

**Modifications Made:**
* **Transition to `npx`:** Instead of relying on a pre-installed global package, we updated the command to `npx -y n8n@latest`. This ensures that the system always fetches and runs the most up-to-date n8n version without requiring manual installation. 
* **Targeted Version:** The `latest` tag downloaded and utilized **n8n version 2.29.10**.
* **Automated Owner Setup:** Modern n8n versions require the first user to register an "Owner" account. To bypass the manual web setup, we configured the following environment variables inside the script:
  * `N8N_INSTANCE_OWNER_EMAIL`: `huanzip@gmail.com`
  * `N8N_INSTANCE_OWNER_PASSWORD_HASH`: A bcrypt hash of the password `n8n`
  * `N8N_INSTANCE_OWNER_MANAGED_BY_ENV`: `true`

## 3. Troubleshooting Issues Encountered

During the installation process, we encountered two significant roadblocks:

### A. Database Owner Collision
**Issue:** The n8n SQLite database located at `~/.n8n/database.sqlite` already contained an existing Owner account from a previous local installation. n8n threw an error because the script attempted to automatically create an owner when one already existed.
**Resolution:** We utilized the `sqlite3` command-line tool to inspect the database and manually resolve the conflict, allowing our new environment variables to seamlessly take over.

### B. NPM Cache Corruption (`ECOMPROMISED`)
**Issue:** While running `npx -y n8n@latest`, the installation repeatedly crashed with an `npm error code ECOMPROMISED` and a "Lock compromised" error. This was caused by corrupted cache files inside the local Node environment (`~/.npm/_npx/`).
**Resolution:** We performed a deep clean of the npm cache by executing the following commands:
```bash
rm -rf ~/.npm/_npx
npm cache clean --force
```
After clearing the cache, `npx` performed a fresh, successful download of the n8n package (~500MB).

## 4. Final Result
The n8n application is now fully stable and accessible locally.
* **Access URL:** `http://localhost:5678`
* **Configured Email:** `huanzip@gmail.com`
* **Configured Password:** `n8n`

All setup logic for Chapter 1 is neatly contained within the new `ch01/start-n8n.sh` script, providing a reliable 1-click startup experience.
