# CODESPACE README - NOVA 2.0

Welcome to NOVA 2.0 in GitHub Codespaces!

## Quick Start Commands

1. **Launch Interactive Shell:**
   ```bash
   python3 nova/ui/cli/nova_shell.py
   ```

2. **Launch Web Dashboard & To-Do App:**
   ```bash
   python3 nova/ui/web/server.py
   # Or with uvicorn:
   uvicorn nova.ui.web.server:app --reload --port 8000
   ```
