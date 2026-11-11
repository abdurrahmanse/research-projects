"""Build the project book (PDF) from the notebook's result files.

Every number in the book is read from ../results/*.csv, the raw data file or the
printed output of the executed notebook, so the book always matches the last run.

Requirements:  pip install jinja2 pandas pymupdf      and Google Chrome installed.
Run:           python build_book.py
Output:        book/Beyond_Accuracy_Postpartum_Anxiety_Screening_Book.pdf
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd
import pymupdf
from jinja2 import Environment, FileSystemLoader, StrictUndefined

BOOK = Path(__file__).resolve().parent
PROJECT = BOOK.parent
RESULTS = PROJECT / "results"
NOTEBOOK = PROJECT / "notebooks" / "postpartum_anxiety_xai_study.ipynb"
RAW = PROJECT / "data" / "raw" / "postpartum_depression.csv"
OUTPUT = BOOK / "Beyond_Accuracy_Postpartum_Anxiety_Screening_Book.pdf"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

TARGET = "Feeling anxious"
HYBRID = "Hybrid Stack (proposed)"


def table(name, **kwargs):
    return pd.read_csv(RESULTS / name, **kwargs)


def notebook_outputs():
    """Printed text of every notebook cell, keyed by its task number."""
    cells = json.loads(NOTEBOOK.read_text())["cells"]
    outputs = {}
    for cell in cells:
        source = "".join(cell["source"])
        match = re.match(r"# Task (\d+):", source)
        if cell["cell_type"] != "code" or not match:
            continue
        text = ""
        for out in cell.get("outputs", []):
            if out.get("output_type") == "stream" and out.get("name") == "stdout":
                text += "".join(out["text"])
        outputs[int(match.group(1))] = text
    return outputs


def find(pattern, text, cast=float):
    match = re.search(pattern, text)
    if not match:
        sys.exit(f"Could not find {pattern!r} in the notebook output. Run the notebook first.")
    return cast(match.group(1))


def load_context():
    out = notebook_outputs()

    # ---- result tables -------------------------------------------------
    cv = table("cv_results.csv", index_col=0)
    cv.columns = ["mean", "std"]
    test = table("test_results.csv", index_col=0)
    gap = table("train_vs_test.csv", index_col=0)
    confusion = table("confusion_matrices.csv", index_col=0)
    confusion.columns = ["tn", "fp", "fn", "tp"]
    wilcoxon = table("statistical_tests.csv")
    mcnemar = table("mcnemar_tests.csv")
    robust = table("robustness_grouped_cv.csv", index_col=0)
    robust.columns = ["standard", "grouped", "grouped_balanced"]
    conformal = table("conformal_prediction.csv")
    conformal.columns = ["target", "actual", "size", "single", "both", "empty"]
    fairness = table("fairness_by_age.csv", index_col=0)
    fairness.columns = ["people", "accuracy"]
    counterfactual = table("counterfactual_example.csv")
    literature = table("literature_comparison.csv")
    literature.columns = ["study", "accuracy"]
    importance = table("shap_vs_lime_importance.csv", index_col=0)
    importance.columns = ["shap", "lime"]
    importance = importance.sort_values("shap", ascending=False)
    faith = table("shap_vs_lime_faithfulness.csv", index_col=0)
    agreement = table("shap_vs_lime_agreement.csv", index_col=0)["value"]
    xai = table("shap_vs_lime_summary.csv", index_col=0)
    permutation = table("permutation_importance_by_model.csv", index_col=0)
    summary = table("final_summary.csv", index_col=0)["value"]

    model_order = list(test.index)                       # best test accuracy first
    tree_and_net = [m for m in model_order if m != "Logistic Regression"]

    # ---- raw data facts --------------------------------------------------
    raw = pd.read_csv(RAW)
    data = raw.drop(columns="Timestamp").fillna("No answer")
    features = [c for c in data.columns if c != TARGET]
    anxious = data[TARGET] == "Yes"
    stamps = pd.to_datetime(raw["Timestamp"], format="%m/%d/%Y %H:%M")
    questions = []
    for f in features:
        counts = data[f].value_counts()
        rate = anxious.groupby(data[f]).mean() * 100
        questions.append({"name": f, "answers": [
            {"text": a, "n": int(counts[a]), "share": counts[a] / len(data) * 100, "anxious": rate[a]}
            for a in counts.index]})
    pattern_labels = data.groupby(features)[TARGET].nunique()
    pattern_sizes = data.groupby(features).size()
    missing = raw.isna().sum()

    # ---- numbers printed by the notebook ----------------------------------
    twin_text = out[54]
    facts = {
        "rows": len(raw), "columns": raw.shape[1], "features": len(features),
        "anxious": int(anxious.sum()), "not_anxious": int((~anxious).sum()),
        "anxious_share": anxious.mean() * 100,
        "missing_cells": int(missing.sum()),
        "missing": {k: int(v) for k, v in missing[missing > 0].items()},
        "unique_patterns": int(len(pattern_sizes)),
        "repeated_rows": int(len(raw) - len(pattern_sizes)),
        "mixed_label_patterns": int((pattern_labels > 1).sum()),
        "largest_pattern": int(pattern_sizes.max()),
        "patterns_seen_once": int((pattern_sizes == 1).sum()),
        "first_stamp": stamps.min().strftime("%d %B %Y, %H:%M"),
        "last_stamp": stamps.max().strftime("%d %B %Y, %H:%M"),
        "collection_hours": (stamps.max() - stamps.min()).total_seconds() / 3600,
        "train_n": find(r"Train: \((\d+)", out[12], int),
        "test_n": find(r"Test: \((\d+)", out[12], int),
        "xgb_best_cv": find(r"Best CV accuracy: ([\d.]+)", out[16]) * 100,
        "xgb_params": eval(find(r"Best settings\s+: (\{.*\})", out[16], str)),
        "lgbm_best_cv": find(r"Best CV accuracy: ([\d.]+)", out[17]) * 100,
        "lgbm_params": eval(find(r"Best settings\s+: (\{.*\})", out[17], str)),
        "friedman_chi2": find(r"chi2 = ([\d.]+)", out[34]),
        "friedman_p": find(r"p = ([\d.e+-]+)", out[34]),
        "ci": summary["Hybrid Stack 95% CI (%)"].replace("-", "–"),
        "person_probability": find(r"Predicted anxious probability: ([\d.]+)", out[40]),
        "person_label": find(r"True label: (\d)", out[40], int),
        "shap_base": find(r"base ([\d.]+)", out[40]),
        "shap_sum": find(r"contributions (-?[\d.]+)", out[40]),
        "cf_person": find(r"Person (\d+):", out[52], int),
        "cf_probability": find(r"anxious probability ([\d.]+)", out[52]),
        "twins": find(r"training set: (\d+) of", twin_text, int),
        "twin_share": find(r"\(([\d.]+)%\)", twin_text),
        "twin_accuracy": find(r"with a twin\s*: ([\d.]+)%", twin_text),
        "no_twin_accuracy": find(r"without a twin\s*: ([\d.]+)%", twin_text),
        "no_twin_n": find(r"without a twin\s*: [\d.]+%\s+\(n = (\d+)\)", twin_text, int),
        "python": json.loads(NOTEBOOK.read_text())["metadata"]["language_info"]["version"],
    }
    facts["friedman_p"] = "p < 0.001" if facts["friedman_p"] < 0.001 else f"p = {facts['friedman_p']:.3f}"
    facts["nonlinear_train_min"] = gap.loc[tree_and_net, "train_accuracy"].min()
    facts["max_gap"] = gap.loc[tree_and_net, "gap"].max()
    facts["auc_low"] = test.loc[tree_and_net, "roc_auc"].min()
    facts["auc_high"] = test["roc_auc"].max()
    drop = (robust["standard"] - robust["grouped"]).loc[tree_and_net]
    facts["drop_low"], facts["drop_high"] = drop.min(), drop.max()
    balanced_gap = robust["grouped"] - robust["grouped_balanced"]
    facts["bal_gap_low"], facts["bal_gap_high"] = balanced_gap.min(), balanced_gap.max()
    facts["no_twin_right"] = round(facts["no_twin_accuracy"] / 100 * facts["no_twin_n"])
    facts["test_not_anxious"] = int(confusion.loc[HYBRID, ["tn", "fp"]].sum())
    facts["test_anxious"] = int(confusion.loc[HYBRID, ["fn", "tp"]].sum())
    facts["hybrid_errors"] = int(confusion.loc[HYBRID, ["fn", "fp"]].sum())
    facts["above_97"] = int((test["accuracy"] > 97).sum())
    facts["grouped_low"] = robust.loc[tree_and_net, "grouped"].min()
    facts["grouped_high"] = robust["grouped"].max()
    facts["grouped_best"] = robust["grouped"].idxmax()
    facts["cv_low"] = cv.loc[tree_and_net, "mean"].min()
    facts["cv_high"] = cv["mean"].max()
    facts["lit_low"] = literature[~literature["study"].str.startswith("This study")]["accuracy"].min()
    facts["lit_high"] = literature[~literature["study"].str.startswith("This study")]["accuracy"].max()

    requirements = [line.strip() for line in (PROJECT / "requirements.txt").read_text().splitlines()
                    if "==" in line]
    tasks = []
    for cell in json.loads(NOTEBOOK.read_text())["cells"]:
        source = "".join(cell["source"])
        if cell["cell_type"] == "markdown" and source.startswith("## Part"):
            tasks.append({"part": source[3:].strip(), "steps": []})
        match = re.match(r"# Task (\d+): (.*)", source)
        if cell["cell_type"] == "code" and match:
            tasks[-1]["steps"].append({"n": int(match.group(1)), "title": match.group(2).strip()})

    facts["task_count"] = sum(len(part["steps"]) for part in tasks)

    return {
        "n": facts, "H": HYBRID, "models": model_order,
        "cv": cv.to_dict("index"), "test": test.to_dict("index"), "gap": gap.to_dict("index"),
        "confusion": confusion.to_dict("index"), "robust": robust.to_dict("index"),
        "robust_order": list(robust.index),
        "wilcoxon": wilcoxon.to_dict("records"), "mcnemar": mcnemar.to_dict("records"),
        "conformal": conformal.to_dict("records"),
        "fairness": [{"age": a, **row} for a, row in fairness.to_dict("index").items()],
        "counterfactual": counterfactual.to_dict("records"),
        "literature": literature.to_dict("records"),
        "importance": [{"question": q, **row} for q, row in importance.to_dict("index").items()],
        "faith": [{"k": k, **row} for k, row in faith.to_dict("index").items()],
        "agreement": agreement.to_dict(), "xai": xai.to_dict("index"),
        "permutation": [{"question": q, **row} for q, row in permutation.to_dict("index").items()],
        "permutation_max": float(permutation.to_numpy().max()),
        "questions": questions, "requirements": requirements, "tasks": tasks,
        "fig": lambda name: (RESULTS / name).as_uri(),
        "css": (BOOK / "style.css").read_text(),
    }


def render_pdf(html, pdf_path, work):
    html_path = work / "book.html"
    html_path.write_text(html, encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    "--generate-pdf-document-outline", f"--print-to-pdf={pdf_path}", html_path.as_uri()],
                   check=True, capture_output=True, timeout=300)


def main():
    env = Environment(loader=FileSystemLoader(BOOK), undefined=StrictUndefined, trim_blocks=True, lstrip_blocks=True)
    env.filters["f1"] = lambda v: f"{float(v):.1f}"
    env.filters["f2"] = lambda v: f"{float(v):.2f}"
    env.filters["f3"] = lambda v: f"{float(v):.3f}"
    env.filters["p"] = lambda v: "< 0.001" if float(v) < 0.001 else f"{float(v):.3f}"
    template = env.get_template("book.html.j2")
    context = load_context()

    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        # Pass 1: lay the book out, then read which page every heading landed on.
        first = work / "pass1.pdf"
        render_pdf(template.render(**context, pages={}), first, work)
        with pymupdf.open(first) as doc:
            pages = {name: dest["page"] + 1 for name, dest in doc.resolve_names().items() if dest.get("page", -1) >= 0}
        # Pass 2: the same layout with the page numbers written into the contents.
        render_pdf(template.render(**context, pages=pages), OUTPUT, work)

    with pymupdf.open(OUTPUT) as doc:
        doc.set_metadata({**doc.metadata, "author": "Abdur Rahman", "creator": "build_book.py",
                          "subject": "Project book: explainable stacking ensemble for postpartum anxiety screening",
                          "keywords": "postpartum anxiety, stacking ensemble, SHAP, LIME, conformal prediction, data leakage"})
        doc.saveIncr()
        print(f"Wrote {OUTPUT.name}: {doc.page_count} pages, {OUTPUT.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
