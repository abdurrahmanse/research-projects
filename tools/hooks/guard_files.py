#!/usr/bin/env python3
"""PreToolUse hook for Write/Edit: protect raw data and keep .py as the notebook source of truth.

Exit 2 blocks the tool call and shows the message to the agent.
"""
import json
import sys

try:
    path = json.load(sys.stdin).get("tool_input", {}).get("file_path", "") or ""
except Exception:
    sys.exit(0)

if "/data/" in path:
    print("Blocked: raw data is read-only (Constitution Article 6.4). Clean data in code, never in the file.", file=sys.stderr)
    sys.exit(2)
if path.endswith(".ipynb"):
    print("Blocked: do not edit .ipynb directly. Edit notebooks/<name>.py and rebuild with tools/make_notebook.py.", file=sys.stderr)
    sys.exit(2)
sys.exit(0)
