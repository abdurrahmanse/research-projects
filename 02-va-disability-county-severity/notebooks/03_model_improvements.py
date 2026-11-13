# %%
"""
PRE-SPECIFIED PLAN (fixed before any new model was run; pre-approved by the caller, not chosen by the tutor)
Question: can out-of-state prediction of the county high-rating share be improved over untuned GB / linear, and is any gain real?
Data: Disability.csv, same cleaning, outcome, 4 features, main sample, seed and outer folds as notebook 02 (5 folds x 10 repeats, state-grouped).
Primary metric: grouped OOF R2 and RMSE, counties equal; recipient-weighted R2/RMSE alongside.
Candidates (12 grid points each, inner GroupKFold(3) over outer-training states only): Ridge, Ridge+poly2, RandomForest, HistGB,
  Ridge and HistGB fitted with recipient weights, ensemble of the inner-CV-best linear and best tree. References: baseline, untuned linear, untuned GB.
Improvement rule: 95% state-cluster bootstrap CI (2000 resamples, stored OOF, no refit) of the paired R2 difference vs the better existing model
  excludes 0 (lower bound > 0). Also reported: Nadeau-Bengio t-test on 50 fold scores with Holm over all new-vs-reference comparisons.
No features from the outcome or other rating bands; no tuning on outer test states.
Extras: (g) LOSO nearest-neighbour distance vs state RMSE (Spearman); (h) MixedLM only if statsmodels is already installed.
"""

# %%
import importlib.util
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from scipy import stats
from sklearn.base import clone
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import r2_score
from sklearn.model_selection import GroupKFold, ParameterGrid
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

# %%
DATA_FILE = Path("../data/raw/Disability.csv")
RESULTS = Path("../results")
SEED, N_REPEATS, N_FOLDS, N_BOOT = 42, 10, 5, 2000
BLUE, ORANGE, GREY = "#2a78d6", "#eb6834", "#8a8a85"
raw = pd.read_csv(DATA_FILE, dtype=str)
raw.columns = ["fips", "state", "county", "total", "r0_20", "r30_40", "r50_60", "r70_90", "r100",
               "age_17_44", "age_45_64", "age_65_plus", "male", "female"]
for c in raw.columns[3:]:
    raw[c] = pd.to_numeric(raw[c].str.replace(",", ""), errors="coerce")
df = raw[~raw.fips.isin(["72000", "88888", "00000", "Unknown"])].copy()
print(f"{len(df):,} counties, {df.state.nunique()} states | duplicate FIPS: {df.fips.duplicated().sum()}"
      f" | duplicate rows: {df.duplicated().sum()}")

# %%
df["high_share"] = (df.r70_90 + df.r100) / df.total
df["young_share"] = df.age_17_44 / df.total
df["older_share"] = df.age_65_plus / df.total
df["female_share"] = df.female / df.total
df["log_total"] = np.log10(df.total)
FEATURES = ["young_share", "older_share", "female_share", "log_total"]
main = df.dropna(subset=["high_share"] + FEATURES).reset_index(drop=True)
X_all = main[FEATURES].values
y_all = main.high_share.values * 100          # percentage points
state_all = main.state.values
TOTAL = main.total.values.astype(float)
WEIGHTS = {"unweighted": np.ones(len(main)), "recipient-weighted": TOTAL}
print(f"Main sample: {len(main):,} counties in {main.state.nunique()} states")

# %%
def state_folds(repeat):
    order = np.random.default_rng(SEED + repeat).permutation(np.unique(state_all))
    return [np.flatnonzero(np.isin(state_all, chunk)) for chunk in np.array_split(order, N_FOLDS)]

STATE_FOLDS = [state_folds(r) for r in range(N_REPEATS)]
MODELS = {
    "Overall average (baseline)": DummyRegressor(),
    "Linear regression": make_pipeline(StandardScaler(), LinearRegression()),
    "Gradient boosting": HistGradientBoostingRegressor(max_depth=3, learning_rate=0.05, max_iter=200, random_state=SEED),
}

def oof_predict(model, folds):
    pred = np.empty(len(y_all))
    for test in folds:
        train = np.setdiff1d(np.arange(len(y_all)), test)
        pred[test] = model.fit(X_all[train], y_all[train]).predict(X_all[test])
    return pred

print([len(t) for t in STATE_FOLDS[0]])
OOF_REF = {m: np.array([oof_predict(MODELS[m], STATE_FOLDS[r]) for r in range(N_REPEATS)]) for m in MODELS}

# %%
def metrics(pred, w):
    e = y_all - pred
    ybar = np.average(y_all, weights=w)
    return {"r2": 1 - np.sum(w * e**2) / np.sum(w * (y_all - ybar) ** 2), "rmse": np.sqrt(np.average(e**2, weights=w))}

first = pd.read_csv(RESULTS / "table_07_cv_summary.csv").query("scheme == 'State-grouped folds'").set_index("model").r2
repro = pd.DataFrame({"this_notebook": {m: np.mean([metrics(p, WEIGHTS["unweighted"])["r2"] for p in P]) for m, P in OOF_REF.items()}})
repro["first_notebook"] = first.reindex(repro.index)
repro["difference"] = repro.this_notebook - repro.first_notebook
assert repro.difference.abs().max() < 0.0006, "reference scores NOT reproduced"
repro.round(4)

# %%
PIPES = {
    "ridge": Pipeline([("scale", StandardScaler()), ("model", Ridge())]),
    "poly": Pipeline([("poly", PolynomialFeatures(2, include_bias=False)), ("scale", StandardScaler()), ("model", Ridge())]),
    "rf": Pipeline([("model", RandomForestRegressor(n_estimators=150, random_state=SEED))]),
    "hgb": Pipeline([("model", HistGradientBoostingRegressor(random_state=SEED))]),
}
ALPHAS = np.logspace(-2, 3, 12)
GRIDS = {"ridge": {"model__alpha": ALPHAS}, "poly": {"model__alpha": ALPHAS},
         "rf": {"model__max_depth": [3, 6, 10], "model__min_samples_leaf": [5, 20, 50, 100]},
         "hgb": {"model__max_depth": [2, 3, 5], "model__learning_rate": [0.03, 0.1], "model__max_iter": [100, 300]}}
grid_table = pd.DataFrame({"grid": {k: {p: [round(float(v), 3) for v in vs] for p, vs in g.items()} for k, g in GRIDS.items()},
                           "combinations": {k: len(ParameterGrid(g)) for k, g in GRIDS.items()}})
grid_table.to_csv(RESULTS / "table_21_tuning_grids.csv")
grid_table

# %%
def inner_mse(key, params, Xt, yt, wt, inner):
    err, wts = [], []
    for a, b in inner:
        m = clone(PIPES[key]).set_params(**params).fit(Xt[a], yt[a], model__sample_weight=wt[a])
        err.append((yt[b] - m.predict(Xt[b])) ** 2)
        wts.append(wt[b])
    return np.average(np.concatenate(err), weights=np.concatenate(wts))

def tune_fit(key, train, test, weighted):
    Xt, yt = X_all[train], y_all[train]
    wt = TOTAL[train] if weighted else np.ones(len(train))
    inner = list(GroupKFold(3).split(Xt, yt, state_all[train]))
    grid = list(ParameterGrid(GRIDS[key]))
    scores = [inner_mse(key, p, Xt, yt, wt, inner) for p in grid]
    best = grid[int(np.argmin(scores))]
    model = clone(PIPES[key]).set_params(**best).fit(Xt, yt, model__sample_weight=wt)
    return best, min(scores), model.predict(X_all[test])

print("inner folds use states of the outer-training part only; example inner fold sizes:",
      [len(b) for _, b in GroupKFold(3).split(X_all, y_all, state_all)])

# %%
CANDS = {"Ridge (tuned)": ("ridge", False), "Ridge + poly2 (tuned)": ("poly", False),
         "Random forest (tuned)": ("rf", False), "HistGB (tuned)": ("hgb", False),
         "Ridge, recipient-weighted fit": ("ridge", True), "HistGB, recipient-weighted fit": ("hgb", True)}
ENS = "Ensemble: best linear + best tree"

def outer_fold(r, k):
    test = STATE_FOLDS[r][k]
    train = np.setdiff1d(np.arange(len(y_all)), test)
    out = {n: tune_fit(key, train, test, w) for n, (key, w) in CANDS.items()}
    lin = min(["Ridge (tuned)", "Ridge + poly2 (tuned)"], key=lambda n: out[n][1])
    tree = min(["Random forest (tuned)", "HistGB (tuned)"], key=lambda n: out[n][1])
    out[ENS] = ({"linear": lin, "tree": tree}, np.nan, (out[lin][2] + out[tree][2]) / 2)
    return out

t0 = time.time()
results = Parallel(n_jobs=-1)(delayed(outer_fold)(r, k) for r in range(N_REPEATS) for k in range(N_FOLDS))
print(f"{len(results)} outer folds done in {time.time() - t0:.0f} s")

# %%
NEW = list(CANDS) + [ENS]
OOF_NEW = {n: np.zeros((N_REPEATS, len(y_all))) for n in NEW}
chosen = []
for i, res in enumerate(results):
    r, k = divmod(i, N_FOLDS)
    for n in NEW:
        OOF_NEW[n][r][STATE_FOLDS[r][k]] = res[n][2]
        chosen.append({"repeat": r, "fold": k, "candidate": n, "chosen": str(res[n][0]), "inner_mse": res[n][1]})
chosen = pd.DataFrame(chosen)
chosen.round(4).to_csv(RESULTS / "table_22_selected_hyperparameters.csv", index=False)
chosen.groupby("candidate").chosen.value_counts().groupby(level=0).head(2).to_frame("folds")

# %%
ALL = {**OOF_REF, **OOF_NEW}
rows = {}
for name, P in ALL.items():
    u = pd.DataFrame([metrics(p, WEIGHTS["unweighted"]) for p in P])
    w = pd.DataFrame([metrics(p, WEIGHTS["recipient-weighted"]) for p in P])
    rows[name] = {"r2_u": u.r2.mean(), "r2_min": u.r2.min(), "r2_max": u.r2.max(), "rmse_u": u.rmse.mean(),
                  "r2_w": w.r2.mean(), "rmse_w": w.rmse.mean()}
scores = pd.DataFrame(rows).T
scores.round(4).to_csv(RESULTS / "table_23_all_candidates.csv")
pd.DataFrame({f"{n}|rep{r}": P[r] for n, P in ALL.items() for r in range(N_REPEATS)}, index=main.fips).round(3).to_csv(
    RESULTS / "table_24_oof_predictions.csv")
scores.round(3)

# %%
states = np.unique(state_all)
rng = np.random.default_rng(SEED)
S1 = pd.get_dummies(main.state).values.astype(float)
COUNTS = np.vstack([np.ones(len(states))] + [np.bincount(rng.choice(len(states), len(states)), minlength=len(states))
                                              for _ in range(N_BOOT)])
NAMES = list(ALL)
STACK = np.array([ALL[n] for n in NAMES])

def boot_r2(w):
    sw, swy, swy2 = w @ S1, (w * y_all) @ S1, (w * y_all**2) @ S1
    swe2 = np.einsum("mrn,ns->mrs", w * (y_all - STACK) ** 2, S1)
    sst = COUNTS @ swy2 - (COUNTS @ swy) ** 2 / (COUNTS @ sw)
    return (1 - np.einsum("bs,mrs->bmr", COUNTS, swe2) / sst[:, None, None]).mean(axis=2)

BOOT = {k: boot_r2(w) for k, w in WEIGHTS.items()}
print("max |bootstrap point - table| :", np.abs(BOOT["unweighted"][0] - scores.loc[NAMES, "r2_u"].values).max(),
      np.abs(BOOT["recipient-weighted"][0] - scores.loc[NAMES, "r2_w"].values).max())

# %%
REF_U = scores.loc[["Linear regression", "Gradient boosting"], "r2_u"].idxmax()
REF_W = scores.loc[["Linear regression", "Gradient boosting"], "r2_w"].idxmax()
FS = {n: np.array([r2_score(y_all[t], ALL[n][r][t]) for r in range(N_REPEATS) for t in STATE_FOLDS[r]]) for n in NAMES}

def nb_test(a, b):
    d = a - b
    se = np.sqrt((1 / len(d) + 1 / (N_FOLDS - 1)) * d.var(ddof=1))
    half = stats.t.ppf(0.975, len(d) - 1) * se
    return {"nb_mean_diff": d.mean(), "nb_ci_low": d.mean() - half, "nb_ci_high": d.mean() + half,
            "p_raw": 2 * stats.t.sf(abs(d.mean() / se), df=len(d) - 1)}

nb = pd.DataFrame({n: nb_test(FS[n], FS[REF_U]) for n in NEW}).T
p = nb.p_raw.values
nb["p_holm"] = np.minimum(1, np.maximum.accumulate((len(p) - np.arange(len(p))) * np.sort(p)))[np.argsort(np.argsort(p))]
print("Reference (unweighted R2):", REF_U, "| reference (weighted R2):", REF_W)

# %%
def paired(key, ref, cand):
    d = BOOT[key][:, NAMES.index(cand)] - BOOT[key][:, NAMES.index(ref)]
    return d[0], *np.percentile(d[1:], [2.5, 97.5])

comp = pd.DataFrame({n: dict(zip(["r2_diff", "boot_low", "boot_high"], paired("unweighted", REF_U, n)))
                     | dict(zip(["weighted_diff", "weighted_low", "weighted_high"], paired("recipient-weighted", REF_W, n)))
                     for n in NEW}).T.join(nb)
comp["improves_by_rule"] = comp.boot_low > 0
comp.round(4).to_csv(RESULTS / "table_25_paired_vs_reference.csv")
comp.round(4)

# %%
fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 4.2))
a1.boxplot([FS[n] for n in NAMES], vert=False, tick_labels=NAMES)
a1.set(title="Out-of-state fold R² (50 folds)", xlabel="R² per outer test fold (unitless)")
ypos = np.arange(len(NEW))[::-1]
a2.errorbar(comp.r2_diff, ypos, xerr=[comp.r2_diff - comp.boot_low, comp.boot_high - comp.r2_diff], fmt="o", color=BLUE, capsize=3)
a2.axvline(0, color=GREY, linewidth=1)
a2.set_yticks(ypos, NEW)
a2.set(title=f"Paired R² difference vs {REF_U}", xlabel="R² difference, 95% state-cluster bootstrap CI (unitless)")
fig.savefig(RESULTS / "fig_09_candidates_boxplot_and_paired_diff.png", dpi=150, bbox_inches="tight")
plt.show()

# %%
loso_pred = oof_predict(MODELS[REF_U], [np.flatnonzero(state_all == s) for s in states])
aoa = []
for s in states:
    test = np.flatnonzero(state_all == s)
    train = np.setdiff1d(np.arange(len(y_all)), test)
    scaler = StandardScaler().fit(X_all[train])
    dist, _ = NearestNeighbors(n_neighbors=1).fit(scaler.transform(X_all[train])).kneighbors(scaler.transform(X_all[test]))
    aoa.append({"state": s, "counties": len(test), "mean_nn_distance": dist.mean(),
                "rmse": np.sqrt(np.mean((loso_pred[test] - y_all[test]) ** 2))})
aoa = pd.DataFrame(aoa).set_index("state")
rho, rho_p = stats.spearmanr(aoa.mean_nn_distance, aoa.rmse)
aoa.round(3).to_csv(RESULTS / "table_26_area_of_applicability.csv")
print(f"Spearman rho = {rho:.3f}, p = {rho_p:.3g}, across {len(aoa)} states, model = {REF_U}")

# %%
fig, ax = plt.subplots(figsize=(6, 4.2))
ax.scatter(aoa.mean_nn_distance, aoa.rmse, s=aoa.counties.clip(upper=200) / 4 + 10, color=BLUE, alpha=0.7)
ax.set(title=f"Distance to training counties vs error (Spearman = {rho:.2f})",
       xlabel="Mean nearest-neighbour distance (standardised feature units)",
       ylabel="State RMSE (percentage points)")
fig.savefig(RESULTS / "fig_10_aoa_distance_vs_rmse.png", dpi=150, bbox_inches="tight")
plt.show()

# %%
print("statsmodels importable:", importlib.util.find_spec("statsmodels") is not None)

# %%
import matplotlib
import scipy
import sklearn

print("numpy", np.__version__, "| pandas", pd.__version__, "| scipy", scipy.__version__,
      "| scikit-learn", sklearn.__version__, "| matplotlib", matplotlib.__version__)
