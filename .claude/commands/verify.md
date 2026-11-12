---
description: Verify a notebook against the constitution (lint + full execution + review)
argument-hint: <path to notebooks/name.py>
---
Verify $ARGUMENTS against `docs/CONSTITUTION.md`.

1. Run `python tools/hooks/check_notebook_source.py $ARGUMENTS` and list every finding.
2. Build and execute: `python tools/make_notebook.py $ARGUMENTS <same path with .ipynb> --run`. Report any error with the failing cell.
3. Run the `data-auditor` and `methods-reviewer` subagents on the notebook in parallel.
4. Output a table: each Delivery-checklist item → pass / fail / not applicable, with evidence (cell or output). Do not edit the notebook unless the user asks.
