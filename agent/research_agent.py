#!/usr/bin/env python3
"""Automated research agent (Claude API + server-side web search/fetch).

Pipeline:  plan  ->  parallel web research per sub-question  ->  synthesis  ->  fact-check
Output:    <out>/report.md, findings.md, sources.md, run.json  (inside research/<slug>/)

Usage:
    export ANTHROPIC_API_KEY=...        # or `ant auth login`
    python agent/research_agent.py "How well do SHAP and LIME agree on tabular health data?" \
        --project 01-postpartum-anxiety-xai-hybrid --depth standard
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path

import anthropic

MODEL = "claude-opus-5-5"
BETAS = ["server-side-fallback-2026-07-01"]  # refusal fallback, routed by category
MAX_CONTINUATIONS = 8  # pause_turn resumes per call

TOOLS = [
    {"type": "web_search_20260209", "name": "web_search", "max_uses": 12},
    {"type": "web_fetch_20260209", "name": "web_fetch", "max_uses": 8, "citations": {"enabled": True}},
]

DEPTH = {  # sub-questions, effort
    "quick": (3, "medium"),
    "standard": (5, "high"),
    "deep": (8, "xhigh"),
}

RULES = """Research standards (non-negotiable):
- Every factual claim must come from a source you actually opened or saw in search results. Never cite from memory.
- Prefer primary sources: peer-reviewed papers, preprints (arXiv/medRxiv), official statistics, dataset documentation.
- Record for each source: title, authors/org, year, URL. Do not invent DOIs, authors or numbers.
- Note disagreement between sources and weaknesses in the evidence (sample size, bias, no replication).
- If something cannot be verified, say "unverified". State confidence (high/medium/low) per conclusion.
- Today's date is {today}; check recency for fast-moving topics."""

client = anthropic.Anthropic(max_retries=3)


# ---------------------------------------------------------------- helpers
def call(*, system: str, user: str, tools=None, effort="high", schema=None, max_tokens=32000):
    """One agent turn (with pause_turn continuation). Returns (text, sources)."""
    messages = [{"role": "user", "content": user}]
    sources: dict[str, str] = {}
    kwargs = dict(
        model=MODEL,
        max_tokens=max_tokens,
        system=system,
        betas=BETAS,
        fallbacks="default",
        output_config={"effort": effort, **({"format": {"type": "json_schema", "schema": schema}} if schema else {})},
    )
    if tools:
        kwargs["tools"] = tools

    for _ in range(MAX_CONTINUATIONS + 1):
        with client.beta.messages.stream(messages=messages, **kwargs) as stream:
            msg = stream.get_final_message()
        collect_sources(msg.content, sources)
        if msg.stop_reason == "refusal":
            raise RuntimeError(f"Model refused: {getattr(msg, 'stop_details', None)}")
        if msg.stop_reason != "pause_turn":
            break
        messages = [messages[0], {"role": "assistant", "content": msg.content}]  # server resumes by itself
    text = "".join(b.text for b in msg.content if b.type == "text")
    return text, sources


def collect_sources(content, sources: dict[str, str]) -> None:
    """Harvest real URLs from server-tool result blocks (never from model prose)."""
    for b in content:
        if b.type == "web_search_tool_result" and isinstance(b.content, list):
            for r in b.content:
                if getattr(r, "url", None):
                    sources[r.url] = getattr(r, "title", "") or r.url
        elif b.type == "web_fetch_tool_result":
            c = b.content
            url = getattr(c, "url", None)
            if url:
                title = getattr(getattr(c, "content", None), "title", None) or url
                sources[url] = title


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60] or "research"


# ---------------------------------------------------------------- stages
def plan(question: str, n: int, context: str) -> list[dict]:
    schema = {
        "type": "object",
        "properties": {
            "sub_questions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "question": {"type": "string"},
                        "why": {"type": "string"},
                        "search_hints": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["question", "why", "search_hints"],
                    "additionalProperties": False,
                },
            }
        },
        "required": ["sub_questions"],
        "additionalProperties": False,
    }
    text, _ = call(
        system="You are a research director planning an investigation.",
        user=(
            f"Research question: {question}\n{context}\n\n"
            f"Break this into exactly {n} non-overlapping sub-questions that together fully answer it. "
            "Cover definitions/background, state of the evidence, methods & metrics, contradictions/limitations, "
            "and recent developments. Give search hints (queries, venues, key terms) for each."
        ),
        effort="medium",
        schema=schema,
    )
    return json.loads(text)["sub_questions"]


def research(sq: dict, question: str, effort: str):
    text, sources = call(
        system="You are a meticulous research analyst with web access.\n" + RULES.format(today=date.today()),
        user=(
            f"Overall question: {question}\n\nYour sub-question: {sq['question']}\n"
            f"Why it matters: {sq['why']}\nSearch hints: {', '.join(sq['search_hints'])}\n\n"
            "Search, open the most relevant primary sources, and write findings as markdown:\n"
            "### Key findings (bullets, each with inline source URL)\n"
            "### Evidence quality & disagreements\n"
            "### Confidence (high/medium/low) and gaps"
        ),
        tools=TOOLS,
        effort=effort,
    )
    return sq, text, sources


def synthesize(question: str, findings: str, source_list: str, effort: str) -> str:
    text, _ = call(
        system="You are a senior research scientist writing for expert readers.\n" + RULES.format(today=date.today()),
        user=(
            f"Question: {question}\n\n# Research findings\n{findings}\n\n# Verified source list\n{source_list}\n\n"
            "Write the final report in markdown:\n"
            "1. Executive summary (5 bullets max, with confidence)\n2. Background\n3. Evidence synthesis by theme "
            "(not by source), with inline [n] citations matching the source list numbers\n"
            "4. Contradictions and open problems\n5. Research gaps ranked by feasibility\n6. Limitations of this review\n"
            "Use ONLY the findings and sources above. Do not add facts from memory. Cite only sources in the list."
        ),
        effort=effort,
    )
    return text


def fact_check(report: str, findings: str) -> str:
    text, _ = call(
        system="You are a skeptical fact-checker. You verify, you do not rewrite.",
        user=(
            f"# Report\n{report}\n\n# Underlying findings\n{findings}\n\n"
            "List every claim in the report that is NOT supported by the findings, overstated, or cited to the "
            "wrong source. For each: quote, problem, suggested correction. End with a verdict: PASS or REVISE. "
            "If everything is supported, say PASS."
        ),
        effort="high",
    )
    return text


# ---------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser(description="Automated professional research agent")
    ap.add_argument("question")
    ap.add_argument("--project", help="project folder (e.g. 01-postpartum-anxiety-xai-hybrid); output goes to its research/ dir")
    ap.add_argument("--depth", choices=DEPTH, default="standard")
    ap.add_argument("--context", default="", help="extra context: dataset, constraints, audience")
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()

    n, effort = DEPTH[a.depth]
    root = Path(__file__).resolve().parent.parent
    base = (root / a.project / "research") if a.project else (root / "research")
    out = base / f"{date.today():%Y-%m-%d}-{slugify(a.question)}"
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    print(f"[1/4] Planning ({n} sub-questions)…")
    sqs = plan(a.question, n, f"Context: {a.context}" if a.context else "")
    for i, s in enumerate(sqs, 1):
        print(f"   {i}. {s['question']}")

    print(f"[2/4] Researching in parallel (workers={a.workers})…")
    results, all_sources = {}, {}
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = [ex.submit(research, s, a.question, effort) for s in sqs]
        for f in as_completed(futs):
            try:
                sq, text, src = f.result()
            except Exception as e:  # keep going; record the failure honestly
                print(f"   ! sub-question failed: {e}", file=sys.stderr)
                continue
            results[sq["question"]] = text
            all_sources.update(src)
            print(f"   ✓ {sq['question'][:70]}")

    if not results:
        print("All research tasks failed.", file=sys.stderr)
        return 1

    findings = "\n\n".join(f"## {q}\n\n{t}" for q, t in results.items())
    ordered = sorted(all_sources.items())
    source_list = "\n".join(f"[{i}] {t} — {u}" for i, (u, t) in enumerate(ordered, 1))
    (out / "findings.md").write_text(f"# Raw findings: {a.question}\n\n{findings}\n")
    (out / "sources.md").write_text(
        f"# Sources retrieved by the agent\n\nURLs harvested from actual search/fetch results. "
        f"Open and confirm before citing in a paper.\n\n{source_list}\n"
    )

    print("[3/4] Synthesizing report…")
    report = synthesize(a.question, findings, source_list, effort)

    print("[4/4] Fact-checking…")
    check = fact_check(report, findings)

    (out / "report.md").write_text(
        f"# {a.question}\n\n*Generated {date.today()} by research_agent.py ({MODEL}, depth={a.depth}). "
        f"AI-generated: verify sources before citing.*\n\n{report}\n\n---\n\n## Sources\n\n{source_list}\n\n"
        f"---\n\n## Automated fact-check\n\n{check}\n"
    )
    (out / "run.json").write_text(json.dumps(
        {"question": a.question, "depth": a.depth, "model": MODEL, "sub_questions": sqs,
         "n_sources": len(ordered), "seconds": round(time.time() - t0)}, indent=2))
    print(f"\nDone in {time.time()-t0:.0f}s → {out.relative_to(root)}/report.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
