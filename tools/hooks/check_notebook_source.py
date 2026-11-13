#!/usr/bin/env python3
"""Constitution linter for '# %%' notebook sources (notebooks/*.py). Code cells only, no markdown.

Hook mode : reads the Claude Code hook JSON on stdin; checks only notebooks/*.py.
CLI mode  : python tools/hooks/check_notebook_source.py notebooks/study.py
Exit 2 with findings on stderr (Claude Code feeds them back to the agent); exit 0 when clean.
"""
import ast
import json
import re
import sys
from pathlib import Path

MAX_CODE_LINES = 20
MAX_COMMENT_LINES = 2
LEGACY_WITH_MARKDOWN = {"02_robustness_checks.py"}  # written before the code-only rule
NEEDS_SEED = {
    "train_test_split", "RepeatedStratifiedKFold", "RepeatedKFold", "ShuffleSplit",
    "RandomForestClassifier", "RandomForestRegressor", "ExtraTreesClassifier", "ExtraTreesRegressor",
    "GradientBoostingClassifier", "GradientBoostingRegressor", "HistGradientBoostingClassifier",
    "HistGradientBoostingRegressor", "MLPClassifier", "MLPRegressor", "permutation_importance",
}
SEED_IF_SHUFFLED = {"KFold", "StratifiedKFold", "StratifiedGroupKFold"}
WHOLE_DATA_NAMES = {"X", "df", "data", "y"}


def split_cells(text):
    cells, kind, start, buf = [], None, 0, []
    for i, line in enumerate(text.split("\n"), 1):
        if line.startswith("# %%"):
            if kind:
                cells.append((kind, start, "\n".join(buf)))
            kind, start, buf = ("md" if "[markdown]" in line else "code"), i, []
        else:
            buf.append(line)
    if kind:
        cells.append((kind, start, "\n".join(buf)))
    return cells


def call_name(node):
    f = node.func
    return f.id if isinstance(f, ast.Name) else f.attr if isinstance(f, ast.Attribute) else None


def lint(text, legacy=False):
    out = []
    cells = split_cells(text)
    try:
        tree = ast.parse(text)
    except SyntaxError as e:
        return [f"line {e.lineno}: syntax error: {e.msg}"]

    imported, used = {}, set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for a in node.names:
                imported[(a.asname or a.name).split(".")[0]] = node.lineno
        elif isinstance(node, ast.Name):
            used.add(node.id)
        elif isinstance(node, ast.ExceptHandler):
            if node.type is None or (len(node.body) == 1 and isinstance(node.body[0], ast.Pass)):
                out.append(f"line {node.lineno}: bare/swallowed except hides errors (Article 1.2)")
        elif isinstance(node, ast.Call):
            name = call_name(node)
            kws = {k.arg: k.value for k in node.keywords}
            if name in ("filterwarnings", "simplefilter") and any(
                isinstance(a, ast.Constant) and a.value == "ignore" for a in node.args
            ):
                out.append(f"line {node.lineno}: warnings are silenced; read them instead (Article 1.2)")
            if name in NEEDS_SEED and "random_state" not in kws:
                out.append(f"line {node.lineno}: {name}() needs random_state=SEED (Article 3.10)")
            if name in SEED_IF_SHUFFLED and isinstance(kws.get("shuffle"), ast.Constant) \
                    and kws["shuffle"].value and "random_state" not in kws:
                out.append(f"line {node.lineno}: {name}(shuffle=True) needs random_state=SEED (Article 3.10)")
            if name in ("fit", "fit_transform") and node.args and isinstance(node.args[0], ast.Name) \
                    and node.args[0].id in WHOLE_DATA_NAMES:
                out.append(
                    f"line {node.lineno}: .{name}({node.args[0].id}) fits on the whole data; "
                    "fit on training data only (Article 3.2, leakage)"
                )
    for name, line in imported.items():
        if name not in used:
            out.append(f"line {line}: unused import '{name}' (Article 1.1)")

    test_cells = []
    for idx, (kind, start, body) in enumerate(cells):
        if kind == "code":
            lines = [l for l in body.split("\n") if l.strip() and not l.strip().startswith("#")]
            if len(lines) > MAX_CODE_LINES:
                out.append(f"line {start}: code cell has {len(lines)} lines (max {MAX_CODE_LINES}); split it (Article 1.3)")
            comments = [l for l in body.split("\n") if l.strip().startswith("#")]
            if len(comments) > MAX_COMMENT_LINES:
                out.append(f"line {start}: {len(comments)} comment lines; notebooks are code only, keep at most {MAX_COMMENT_LINES} (Article 4)")
            if re.search(r"\b(X_test|y_test)\b", body) and "train_test_split" not in body:
                test_cells.append(start)
        elif not legacy:
            out.append(f"line {start}: markdown cell not allowed; notebooks are code cells only (Article 4)")
    if len(test_cells) > 1:
        out.append(f"lines {test_cells}: test set used in {len(test_cells)} cells; touch it once (Article 3.2)")
    return out


def main():
    if len(sys.argv) > 1:
        paths = sys.argv[1:]
    else:
        try:
            fp = json.load(sys.stdin).get("tool_input", {}).get("file_path", "")
        except Exception:
            return 0
        paths = [fp] if re.search(r"/notebooks/[^/]+\.py$", fp or "") else []
    bad = 0
    for p in paths:
        problems = lint(Path(p).read_text(encoding="utf-8"), Path(p).name in LEGACY_WITH_MARKDOWN)
        for msg in problems:
            print(f"{p}: {msg}", file=sys.stderr)
        bad += len(problems)
    if bad:
        print(f"\n{bad} constitution violation(s). Fix them without adding extra code.", file=sys.stderr)
        return 2
    if len(sys.argv) > 1:
        print("OK: no constitution violations found")
    return 0


if __name__ == "__main__":
    sys.exit(main())
