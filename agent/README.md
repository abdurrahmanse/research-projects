# Automated Research Agent

Runs a full literature/evidence investigation end to end with Claude (`claude-opus-5-5`) and its server-side web search and web fetch tools.

```
question → plan sub-questions → parallel web research → synthesis → fact-check → report.md
```

## Setup
```bash
cd agent && python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...      # or: ant auth login
```

## Run
```bash
python agent/research_agent.py "Do SHAP and LIME agree on tabular health survey models?" \
    --project 01-postpartum-anxiety-xai-hybrid --depth standard
```
Depth: `quick` (3 sub-questions), `standard` (5), `deep` (8, highest effort; slowest and most expensive).
Add `--context "binary classification, n=1500, tree ensembles"` to steer it toward your data.

## Output (`<project>/research/YYYY-MM-DD-<slug>/`)
| File | Content |
|---|---|
| `report.md` | Executive summary, synthesis, contradictions, gaps, limitations, sources, fact-check verdict |
| `findings.md` | Raw per-sub-question findings (audit trail) |
| `sources.md` | URLs harvested from real search/fetch results, not model-written |
| `run.json` | Settings and run stats |

## Quality controls
- Sources come from tool results, and the synthesis may cite only those.
- A separate fact-check pass flags unsupported or overstated claims (PASS/REVISE).
- Failed sub-questions are reported, not hidden.
- Output is still AI-generated: open the key sources yourself before citing them in a paper.

## Schedule it
Weekly watch on a topic: `cron` / launchd running the command above, or `/schedule` in Claude Code.

Cost: each run makes many web-search calls on Opus-tier tokens; try `--depth quick` first.
