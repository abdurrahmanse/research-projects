# %% [markdown]
# # VA disability: peer-review robustness checks (দ্বিতীয় নোটবুক)
#
# **রোডম্যাপ:** ১ সমস্যা ও metric → ২ লাইব্রেরি → ৩ ডেটা (প্রথম নোটবুকের সংজ্ঞা হুবহু) → ৪ fold ও মডেল, প্রথম নোটবুকের ফল পুনরুৎপাদন →
# ৫ state-cluster bootstrap → ৬ Nadeau-Bengio test → ৭ weighted বনাম unweighted → ৮ leave-one-state-out ও region blocking →
# ৯ state fixed-effects → ১০ selection check → ১১ limitation ও paper-এ কী লিখবেন
#
# **শব্দকোষ**
# - **Cluster bootstrap:** কাউন্টি নয়, গোটা state ধরে নমুনা পুনর্নির্বাচন; একই state-এর কাউন্টিগুলো স্বাধীন নয় বলে।
# - **OOF (out-of-fold) prediction:** প্রতিটা কাউন্টির পূর্বাভাস এমন মডেল থেকে, যে মডেল ওই কাউন্টি দেখেনি।
# - **Weighted:** প্রতিটা কাউন্টির ওজন = তার মোট recipient সংখ্যা; বড় কাউন্টি বেশি গুরুত্ব পায়।
# - **LOSO:** leave-one-state-out; একটা state বাদ রেখে বাকি ৫০টায় শিখে সেটাকে পূর্বাভাস।
# - **Fixed effects (FE):** প্রতি state-এর নিজস্ব ধ্রুবক (one-hot state)।
#
# ## ধাপ ১: সমস্যা, hypothesis, metric (কিছু চালানোর আগেই লেখা)
#
# **অনুমোদিত (pre-approved) প্রশ্ন:** এই প্রশ্ন ও metric ব্যবহারকারীর কাছ থেকে ইন্টারেক্টিভভাবে নেওয়া হয়নি; কলকারী এজেন্ট আগে থেকে ঠিক করে দিয়েছে, tutor নিজে বাছেনি।
#
# - **গবেষণা প্রশ্ন:** প্রথম নোটবুকের মূল ফল (README-র RQ1 থেকে RQ3) কি weighting, leave-one-state-out, region blocking, আনুষ্ঠানিক তুলনা-test এবং state fixed-effects check-এর পরেও টিকে থাকে?
# - **H1:** random-বনাম-grouped R² ফারাক (gradient boosting) bootstrap CI-তে শূন্যের ওপরে থাকবে।
# - **H2:** grouped folds-এ gradient boosting ও linear-এর পার্থক্য ছোট; baseline-এর তুলনায় দুটোই ভালো।
# - **H3:** state-এর ভেতরের (within-state) সম্পর্ক pooled সম্পর্কের থেকে আলাদা হতে পারে; সেটা দেখা হবে, দিক আগে ধরা হয়নি।
# - **Primary metric:** state R² ও RMSE, দুভাবেই: unweighted (প্রথম নোটবুকের সাথে ধারাবাহিকতা) এবং recipient-weighted (পাশাপাশি)।
# - **Validation:** প্রথম নোটবুকের মতোই 5-fold × 10 repeat, random ও state-grouped; এর সাথে LOSO ও region-blocked।
#
# **Checkpoint:** weighted ও unweighted দুটো metric কেন পাশাপাশি রাখছি?

# %% [markdown]
# ## ধাপ ২: লাইব্রেরি ও সেটিংস
#
# **কী করছি:** লাইব্রেরি আনছি, পথ ও seed ঠিক করছি।
# **কেন:** একই seed আর একই সেটিং থাকলে প্রথম নোটবুকের সাথে তুলনা করা যায়।
# **কীভাবে পড়বেন:** কোনো আউটপুট নেই; error না এলেই হলো।

# %%
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import KFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

DATA_FILE = Path("../data/raw/Disability.csv")
RESULTS = Path("../results")
SEED, N_REPEATS, N_FOLDS, N_BOOT = 42, 10, 5, 2000
BLUE, ORANGE, GREY = "#2a78d6", "#eb6834", "#8a8a85"

# %% [markdown]
# ## ধাপ ৩: ডেটা (প্রথম নোটবুকের পরিষ্কার-করা ও outcome/feature সংজ্ঞা হুবহু একই)
#
# **কী করছি:** কাঁচা ফাইল পড়ে সংখ্যায় রূপ দিচ্ছি, কাউন্টি নয় এমন সারি বাদ দিচ্ছি।
# **কেন:** একই main sample না পেলে ফল তুলনা করা যায় না। EDA (বণ্টন, scatter) প্রথম নোটবুকে হয়েছে; এখানে আবার করা হচ্ছে না, কারণ এই নোটবুক শুধু robustness যাচাই করে।
# **কীভাবে পড়বেন:** কাউন্টি সংখ্যা ও duplicate গণনা দেখুন; duplicate শূন্য না হলে train/test leakage-এর ঝুঁকি।

# %%
raw = pd.read_csv(DATA_FILE, dtype=str)
raw.columns = ["fips", "state", "county", "total", "r0_20", "r30_40", "r50_60", "r70_90", "r100",
               "age_17_44", "age_45_64", "age_65_plus", "male", "female"]
COUNTS = list(raw.columns[3:])
for c in COUNTS:
    raw[c] = pd.to_numeric(raw[c].str.replace(",", ""), errors="coerce")
df = raw[~raw.fips.isin(["72000", "88888", "00000", "Unknown"])].copy()
print(f"{len(df):,} counties, {df.state.nunique()} states | duplicate FIPS: {df.fips.duplicated().sum()}"
      f" | duplicate rows: {df.duplicated().sum()}")

# %% [markdown]
# **কী করছি:** outcome (70–90% ও 100% যোগ ÷ মোট) আর চারটা feature বানিয়ে main sample বাছছি।
# **কেন:** প্রথম নোটবুকের সংজ্ঞা হুবহু; বাকি রেটিং band ও 45–64 share feature নয়, কারণ তারা outcome-কে প্রায় বলে দেয় (leakage)।
# **কীভাবে পড়বেন:** main sample-এর কাউন্টি সংখ্যা প্রথম নোটবুকের সংখ্যার সাথে মিলতে হবে (পরের ধাপে মিলিয়ে দেখব)।

# %%
df["high"] = df.r70_90 + df.r100
df["high_share"] = df.high / df.total
df["young_share"] = df.age_17_44 / df.total
df["older_share"] = df.age_65_plus / df.total
df["female_share"] = df.female / df.total
df["log_total"] = np.log10(df.total)
FEATURES = ["young_share", "older_share", "female_share", "log_total"]
main = df.dropna(subset=["high_share"] + FEATURES).reset_index(drop=True)
df["in_main"] = df.fips.isin(main.fips)
print(f"Main sample: {len(main):,} of {len(df):,} counties in {main.state.nunique()} states")

# %% [markdown]
# **কী করছি:** মডেলিং-এর array, weight (মোট recipient) ও metric-ফাংশন ঠিক করছি।
# **কেন:** weighted R² = `1 - Σw·e² / Σw·(y - ȳw)²`, যেখানে ȳw weighted গড়। সব weight 1 ধরলে এটা সাধারণ (unweighted) R²-এর সমান।
# **কীভাবে পড়বেন:** weighted RMSE বড় কাউন্টির ভুলকে বেশি গুরুত্ব দেয়। দুই ধরনের মান কাছাকাছি হলে ফল কাউন্টির আকারের ওপর নির্ভর করছে না।

# %%
X_all = main[FEATURES].values
y_all = main.high_share.values * 100          # percentage points, as in the first notebook
state_all = main.state.values
WEIGHTS = {"unweighted": np.ones(len(main)), "recipient-weighted": main.total.values.astype(float)}

def metrics(pred, w):
    e = y_all - pred
    ybar = np.average(y_all, weights=w)
    return {"r2": 1 - np.sum(w * e**2) / np.sum(w * (y_all - ybar) ** 2),
            "rmse": np.sqrt(np.average(e**2, weights=w)), "mae": np.average(np.abs(e), weights=w)}

print("Total recipients (weights) summary:", main.total.describe()[["min", "50%", "max"]].to_dict())

# %% [markdown]
# ## ধাপ ৪: Fold, মডেল, এবং প্রথম নোটবুকের ফল পুনরুৎপাদন
#
# **কী করছি:** প্রথম নোটবুকের fold-নকশা হুবহু আবার বানাচ্ছি: random 5-fold, আর state-grouped (state এলোমেলো করে `array_split`)।
# **কেন:** grouped folds-এ একটা state-এর সব কাউন্টি একই fold-এ থাকে, তাই test-এ সবসময় অদেখা state। এটাই group leakage আটকায়।
# **কীভাবে পড়বেন:** প্রতি fold-এর test কাউন্টি সংখ্যা; grouped-এ fold-ভেদে অসমান হওয়া স্বাভাবিক।

# %%
def random_folds(repeat):
    return [t for _, t in KFold(N_FOLDS, shuffle=True, random_state=SEED + repeat).split(X_all)]

def state_folds(repeat):
    order = np.random.default_rng(SEED + repeat).permutation(np.unique(state_all))
    return [np.flatnonzero(np.isin(state_all, chunk)) for chunk in np.array_split(order, N_FOLDS)]

FOLDS = {"Random folds": [random_folds(r) for r in range(N_REPEATS)],
         "State-grouped folds": [state_folds(r) for r in range(N_REPEATS)]}
print({k: [len(t) for t in v[0]] for k, v in FOLDS.items()})

# %% [markdown]
# **কী করছি:** তিনটা মডেল (baseline, linear + scaler, gradient boosting) আর OOF-পূর্বাভাসের ফাংশন ঠিক করছি।
# **কেন:** প্রথম নোটবুকের সেটিং হুবহু: কোনো tuning নেই, সব মডেল একই fold ও একই ডেটা পায়। scaler `make_pipeline`-এর ভেতরে, তাই প্রতি fold-এ শুধু training অংশ থেকে শেখে।
# **কীভাবে পড়বেন:** শুধু নামের তালিকা ছাপা হয়।

# %%
MODELS = {
    "Overall average (baseline)": DummyRegressor(),
    "Linear regression": make_pipeline(StandardScaler(), LinearRegression()),
    "Gradient boosting": HistGradientBoostingRegressor(max_depth=3, learning_rate=0.05, max_iter=200, random_state=SEED),
}

def oof_predict(model, folds, X=X_all):
    pred = np.empty(len(y_all))
    for test in folds:
        train = np.setdiff1d(np.arange(len(y_all)), test)
        pred[test] = model.fit(X[train], y_all[train]).predict(X[test])
    return pred

print(list(MODELS))

# %% [markdown]
# **কী করছি:** দুই fold-নকশা × তিন মডেল × ১০ repeat চালিয়ে প্রতিটা কাউন্টির OOF-পূর্বাভাস `OOF`-এ জমা রাখছি এবং CSV-তে সংরক্ষণ করছি।
# **কেন:** পরের সব বিশ্লেষণ (bootstrap, weighting, test) এই জমা-করা পূর্বাভাস থেকেই হবে; মডেল আর refit লাগবে না।
# **কীভাবে পড়বেন:** array-র আকার (repeat × কাউন্টি) দেখে নিশ্চিত হোন প্রতি কাউন্টির প্রতি repeat-এ একটা পূর্বাভাস আছে।

# %%
OOF = {(s, m): np.array([oof_predict(MODELS[m], FOLDS[s][r]) for r in range(N_REPEATS)])
       for s in FOLDS for m in MODELS}
oof_table = pd.DataFrame({f"{s}|{m}|rep{r}": P[r] for (s, m), P in OOF.items() for r in range(N_REPEATS)}, index=main.fips)
oof_table.round(4).to_csv(RESULTS / "table_10_oof_predictions.csv")
print({k: v.shape for k, v in list(OOF.items())[:2]}, "| saved columns:", oof_table.shape[1])

# %% [markdown]
# **কী করছি:** একটা generic ফাংশন দিয়ে প্রতিটা (design, model)-এর R², RMSE, MAE দুই weighting-এ হিসাব করছি, এবং প্রথম নোটবুকের `table_07` (শুধু পড়া হচ্ছে) এর সাথে unweighted R² মেলাচ্ছি।
# **কেন:** নতুন কোড পুরোনো ফল পুনরুৎপাদন না করলে পরের সব ফলই সন্দেহজনক।
# **কীভাবে পড়বেন:** `difference` কলাম প্রায় শূন্য হলে পুনরুৎপাদন সফল। বড় ফারাক = কোথাও সংজ্ঞা আলাদা।

# %%
def score_table(store):
    rows = []
    for (design, model), P in store.items():
        for wname, w in WEIGHTS.items():
            r = pd.DataFrame([metrics(p, w) for p in P])
            rows.append({"design": design, "model": model, "weighting": wname, "r2": r.r2.mean(), "r2_min": r.r2.min(),
                         "r2_max": r.r2.max(), "rmse": r.rmse.mean(), "mae": r.mae.mean()})
    return pd.DataFrame(rows)

cv = score_table(OOF)
ref = pd.read_csv(RESULTS / "table_07_cv_summary.csv").set_index(["model", "scheme"]).r2
mine = cv[cv.weighting == "unweighted"].set_index(["model", "design"]).r2
repro = pd.DataFrame({"this_notebook": mine, "first_notebook": ref.reindex(mine.index)})
repro["difference"] = repro.this_notebook - repro.first_notebook
repro.round(4).to_csv(RESULTS / "table_10_cv_reproduction.csv")
repro.round(4)

# %% [markdown]
# **Checkpoint (ধাপ ৪):** grouped fold-এ random fold-এর চেয়ে R² কম হওয়ার কারণ কী (group leakage)?

# %% [markdown]
# ## ধাপ ৫: State-cluster bootstrap CI (পূর্বাভাস জমা-করা, refit নেই)
#
# **কী করছি:** ২০০০ বার state-সহ নমুনা পুনর্নির্বাচন (with replacement) করে তিনটা রাশির 95% CI বের করছি: (a) random-মাইনাস-grouped R² ফারাক (gradient boosting), (b) grouped R²-এ gradient boosting মাইনাস linear, (c) state-এর মধ্যকার variance-এর অংশ (unweighted eta-squared)।
# **কেন:** একই state-এর কাউন্টি স্বাধীন নয়; কাউন্টি ধরে bootstrap করলে CI অতি-সংকীর্ণ হতো। একই state দুবার এলে তাকে দুটো আলাদা cluster ধরা হয়েছে।
# **কীভাবে পড়বেন:** CI-তে শূন্য না থাকলে ফারাক নমুনা-পরিবর্তনের চেয়ে স্পষ্ট। (a)-এর মান এখানে ১০ repeat-এর গড় R²-এর ফারাক।
# **সাধারণ ভুল:** একে test-set-এর অনিশ্চয়তা ভাবা; এটা শুধু state-নমুনার অনিশ্চয়তা, fold-বিন্যাসের নয়।

# %%
states = np.unique(state_all)
rows_of = {s: np.flatnonzero(state_all == s) for s in states}
rng = np.random.default_rng(SEED)
boot = [rng.choice(states, len(states)) for _ in range(N_BOOT)]
KEYS = [("Random folds", "Gradient boosting"), ("State-grouped folds", "Gradient boosting"),
        ("State-grouped folds", "Linear regression")]

def pooled_r2(P, rows):
    y = y_all[rows]
    return np.mean([1 - ((y - p[rows]) ** 2).sum() / ((y - y.mean()) ** 2).sum() for p in P])

def three_numbers(draw):
    rows = np.concatenate([rows_of[s] for s in draw])
    label = np.repeat(np.arange(len(draw)), [len(rows_of[s]) for s in draw])
    y = y_all[rows]
    n_k, sum_k = np.bincount(label), np.bincount(label, y)
    eta2 = (n_k * (sum_k / n_k - y.mean()) ** 2).sum() / ((y - y.mean()) ** 2).sum()
    gb_rand, gb_grp, lin_grp = (pooled_r2(OOF[k], rows) for k in KEYS)
    return [gb_rand - gb_grp, gb_grp - lin_grp, eta2]

# %% [markdown]
# **কী করছি:** পূর্ণ নমুনায় (প্রতিটা state একবার) মূল মান এবং bootstrap CI হিসাব করে সংরক্ষণ করছি।
# **কেন:** (c)-এর মূল মান প্রথম নোটবুকের "variance between states"-এর সাথে মিলতে হবে।
# **কীভাবে পড়বেন:** `estimate` বনাম `ci_low`, `ci_high`; CI-র প্রস্থ অনিশ্চয়তার মাপ।

# %%
point = three_numbers(states)
draws = np.array([three_numbers(d) for d in boot])
boot_table = pd.DataFrame({"estimate": point, "ci_low": np.percentile(draws, 2.5, axis=0),
                           "ci_high": np.percentile(draws, 97.5, axis=0)},
                          index=["GB R2 gap: random minus grouped", "Grouped R2: GB minus linear",
                                 "Between-state share of variance (eta-squared)"])
boot_table.round(3).to_csv(RESULTS / "table_11_bootstrap_ci.csv")
boot_table.round(3)

# %% [markdown]
# **কী করছি:** তিনটা CI এক ছবিতে আঁকছি।
# **কেন:** প্রশ্ন: কোন ফারাকগুলো শূন্য থেকে স্পষ্ট আলাদা? এক ছবিতে তুলনা সহজ।
# **কীভাবে পড়বেন:** বিন্দু = অনুমান, দাগ = 95% CI, ধূসর রেখা = শূন্য। দাগ শূন্য ছুঁলে ফারাক অনিশ্চিত।

# %%
fig, ax = plt.subplots(figsize=(7.5, 2.8))
ypos = np.arange(len(boot_table))[::-1]
err = [boot_table.estimate - boot_table.ci_low, boot_table.ci_high - boot_table.estimate]
ax.errorbar(boot_table.estimate, ypos, xerr=err, fmt="o", color=BLUE, capsize=4)
ax.axvline(0, color=GREY, linewidth=1)
ax.set_yticks(ypos, boot_table.index)
ax.set(title="State-cluster bootstrap, 95% CI", xlabel="R² difference or share of variance (unitless)")
fig.savefig(RESULTS / "fig_05_bootstrap_ci.png", dpi=150, bbox_inches="tight")
plt.show()

# %% [markdown]
# **Checkpoint (ধাপ ৫):** কাউন্টি-ভিত্তিক বদলে state-ভিত্তিক bootstrap কেন?

# %% [markdown]
# ## ধাপ ৬: Nadeau-Bengio সংশোধিত paired t-test
#
# **কী করছি:** state-grouped folds-এ প্রতিটা test fold-এর নিজস্ব R² নিয়ে (repeat × fold = পরপর জোড়া স্কোর) দুটো পরিকল্পিত জোড়া তুলনা করছি: baseline বনাম gradient boosting, এবং gradient boosting বনাম linear।
# **কেন:** CV-র fold স্কোরগুলো স্বাধীন নয় (training অংশ ওভারল্যাপ করে), তাই সাধারণ t-test অতি-আত্মবিশ্বাসী। সংশোধিত variance = `(1/n + test/train) × s²`; এখানে 5 fold-এ test/train অনুপাত 1/4। দুই test-এর p-value-তে Holm সংশোধন।
# **কীভাবে পড়বেন:** `mean_diff` ধনাত্মক = প্রথম নাম-করা মডেল ভালো (R² বেশি)। `p_holm` ছোট না হলে "উল্লেখযোগ্য পার্থক্য নেই"। CI-তে শূন্য থাকলেও একই কথা।
# **সাধারণ ভুল:** fold স্কোরকে স্বাধীন ধরা। এখানে তারা স্বাধীন নয়; সংশোধনও আনুমানিক।

# %%
def fold_r2(model):
    P = OOF[("State-grouped folds", model)]
    return np.array([r2_score(y_all[t], P[r][t]) for r in range(N_REPEATS) for t in FOLDS["State-grouped folds"][r]])

def nb_test(a, b):
    d = a - b
    n, se = len(d), np.sqrt((1 / len(d) + 1 / (N_FOLDS - 1)) * d.var(ddof=1))
    p = 2 * stats.t.sf(abs(d.mean() / se), df=n - 1)
    half = stats.t.ppf(0.975, n - 1) * se
    return {"n_fold_scores": n, "mean_diff": d.mean(), "ci_low": d.mean() - half, "ci_high": d.mean() + half, "p_raw": p}

fs = {m: fold_r2(m) for m in MODELS}
nb = pd.DataFrame({"GB minus baseline": nb_test(fs["Gradient boosting"], fs["Overall average (baseline)"]),
                   "GB minus linear": nb_test(fs["Gradient boosting"], fs["Linear regression"])}).T
p = nb.p_raw.values
holm = np.minimum(1, np.maximum.accumulate((len(p) - np.arange(len(p))) * np.sort(p)))
nb["p_holm"] = holm[np.argsort(np.argsort(p))]
nb.round(4).to_csv(RESULTS / "table_12_nadeau_bengio.csv")
nb.round(4)

# %% [markdown]
# **Checkpoint (ধাপ ৬):** Holm সংশোধন কেন দরকার, আর fold স্কোর স্বাধীন না হলে সাধারণ t-test-এর কী ক্ষতি?

# %% [markdown]
# ## ধাপ ৭: Weighted বনাম unweighted মান
#
# **কী করছি:** `cv` টেবিল (ধাপ ৪) থেকে baseline, linear, gradient boosting-এর R², RMSE, MAE দুই weighting ও দুই fold-নকশায় সাজাচ্ছি। weight = মোট recipient।
# **কেন:** unweighted মান ছোট কাউন্টির ওপর নির্ভরশীল; ছোট কাউন্টির share বেশি noisy। weighted মান দেখায় বেশি recipient-ওয়ালা কাউন্টিতে মডেল কেমন।
# **কীভাবে পড়বেন:** দুই weighting-এর মান কাছাকাছি হলে সিদ্ধান্ত বদলায় না। আলাদা হলে ছোট ও বড় কাউন্টিতে মডেল আলাদাভাবে আচরণ করছে।

# %%
cv.round(3).to_csv(RESULTS / "table_13_weighted_vs_unweighted.csv", index=False)
cv.pivot_table(index=["design", "model"], columns="weighting", values=["r2", "rmse", "mae"]).round(3)

# %% [markdown]
# **কী করছি:** R²-এর unweighted ও weighted মান পাশাপাশি আঁকছি।
# **কেন:** প্রশ্ন: weighting কি মডেলের ক্রম বা random-বনাম-grouped ফারাক বদলায়?
# **কীভাবে পড়বেন:** প্রতি মডেলে দুই বার; নীল = unweighted, কমলা = weighted। বার শূন্য থেকে শুরু; ঋণাত্মক R² = গড়ের চেয়েও খারাপ।

# %%
fig, axes = plt.subplots(1, 2, figsize=(10, 3.6), sharey=True)
for ax, scheme in zip(axes, FOLDS):
    t = cv[cv.design == scheme].pivot(index="model", columns="weighting", values="r2").loc[list(MODELS)]
    t.plot.bar(ax=ax, color=[ORANGE, BLUE], rot=15, legend=False)
    ax.set(title=scheme, xlabel="", ylabel="R²")
axes[0].legend(frameon=False)
fig.savefig(RESULTS / "fig_06_weighted_vs_unweighted_r2.png", dpi=150, bbox_inches="tight")
plt.show()

# %% [markdown]
# **Checkpoint (ধাপ ৭):** weighted R²-এর বদলে শুধু unweighted দেখালে কোন তথ্য লুকিয়ে যেত?

# %% [markdown]
# ## ধাপ ৮: Leave-one-state-out (LOSO) ও Census-region blocking
#
# **কী করছি:** প্রতি state-কে একবার করে বাদ রেখে (৫১ বার × তিন মডেল refit) পূর্বাভাস নিচ্ছি; তারপর চার region (Northeast, Midwest, South, West) একটা করে বাদ রেখে।
# **কেন:** grouped 5-fold-এ একই fold-এ অনেক state থাকে। LOSO সবচেয়ে কঠোর "অদেখা state" পরীক্ষা, আর region blocking আরও কঠোর: কাছাকাছি state-গুলোও training-এ থাকে না।
# **কীভাবে পড়বেন:** LOSO ও region-blocked R² grouped-5-fold-এর থেকে অনেক কমলে ফল ভৌগোলিকভাবে অন্তর্ভুক্ত সম্পর্কের ওপর নির্ভর করছে।
#
# **Region ম্যাপিং সম্পর্কে সতর্কতা (unverified):** নিচের FIPS-state-থেকে-region ম্যাপিং আমি (tutor) সাধারণ জ্ঞান থেকে লিখেছি, কোনো সূত্র খুলে যাচাই করিনি। DC দক্ষিণে ধরা হয়েছে। ব্যবহারকারীর যাচাই দরকার।

# %%
REGION_OF_PREFIX = {}
for region, prefixes in {
    "Northeast": "09 23 25 33 44 50 34 36 42", "Midwest": "17 18 26 39 55 19 20 27 29 31 38 46",
    "South": "10 11 12 13 24 37 45 51 54 01 21 28 47 05 22 40 48", "West": "04 08 16 30 32 35 49 56 02 06 15 41 53"}.items():
    REGION_OF_PREFIX.update({p: region for p in prefixes.split()})
main["region"] = main.fips.str[:2].map(REGION_OF_PREFIX)
region_map = main.assign(prefix=main.fips.str[:2]).groupby("state").agg(fips_prefix=("prefix", "first"), region=("region", "first"))
region_map.sort_values(["region", "fips_prefix"]).to_csv(RESULTS / "table_14_fips_region_map.csv")
print("Counties without a region:", main.region.isna().sum(), "| states per region:", region_map.region.value_counts().to_dict())
region_map.sort_values(["region", "fips_prefix"])

# %% [markdown]
# **কী করছি:** দুই blocking-নকশার প্রতিটা block-এর test index বানিয়ে তিন মডেলের OOF-পূর্বাভাস নিচ্ছি।
# **কেন:** LOSO-তে ৫১ block, region-এ ৪ block; ফাংশন (`oof_predict`) আগের মতোই, শুধু fold আলাদা।
# **কীভাবে পড়বেন:** block সংখ্যা ও আকার ছাপা হয়; খুব অসমান region হলে region-ভিত্তিক গড়ের ব্যাখ্যায় সাবধান।

# %%
BLOCKS = {"Leave-one-state-out": [rows_of[s] for s in states],
          "Region-blocked": [np.flatnonzero(main.region.values == r) for r in sorted(main.region.unique())]}
BLOCK = {(d, m): oof_predict(MODELS[m], BLOCKS[d])[None] for d in BLOCKS for m in MODELS}
print({d: [len(b) for b in v] if len(v) < 10 else f"{len(v)} blocks" for d, v in BLOCKS.items()})

# %% [markdown]
# **কী করছি:** LOSO ও region-blocked পূর্বাভাসের pooled R², RMSE, MAE (unweighted ও weighted) সারণিতে সাজাচ্ছি।
# **কেন:** এক সংখ্যায় "অদেখা state/region-এ মডেল কতটা ভালো" তুলনা করতে; grouped-5-fold-এর সাথে পাশাপাশি দেখব।
# **কীভাবে পড়বেন:** baseline-এর R² শূন্যের নিচে হওয়া স্বাভাবিক (training গড় test গড়ের সমান নয়)। মডেল baseline-কে হারাচ্ছে কি না দেখুন।

# %%
blocked = score_table(BLOCK)
blocked.round(3).to_csv(RESULTS / "table_15_loso_region_pooled.csv", index=False)
blocked.pivot_table(index=["design", "model"], columns="weighting", values=["r2", "rmse"]).round(3)

# %% [markdown]
# **কী করছি:** প্রতিটা বাদ-রাখা state ও region-এর জন্য কাউন্টি-গড় RMSE ও bias (পূর্বাভাস মাইনাস আসল, শতাংশ পয়েন্টে) বের করছি।
# **কেন:** pooled সংখ্যা লুকায় কোন state-এ মডেল ব্যর্থ। bias ধনাত্মক = মডেল ওই state-এর share বেশি অনুমান করছে।
# **কীভাবে পড়বেন:** সারণি gradient boosting RMSE অনুযায়ী সাজানো; শীর্ষ ও তলার ৫টা দেখুন। কয়েকটি state অতি-বড় ভুল করলে pooled R² তাদের দ্বারা টানা।

# %%
def error_table(design, group):
    rows = []
    for g in np.unique(group):
        i = group == g
        row = {"group": g, "counties": i.sum(), "recipients": int(WEIGHTS["recipient-weighted"][i].sum())}
        for m in MODELS:
            e = BLOCK[(design, m)][0][i] - y_all[i]
            row[m + " | rmse"], row[m + " | bias"] = np.sqrt((e**2).mean()), e.mean()
        rows.append(row)
    return pd.DataFrame(rows).set_index("group").sort_values("Gradient boosting | rmse")

loso_state = error_table("Leave-one-state-out", state_all)
loso_state.round(2).to_csv(RESULTS / "table_16_loso_per_state_error.csv")
pd.concat([loso_state.head(5), loso_state.tail(5)]).round(2)

# %% [markdown]
# **কী করছি:** region-blocked নকশার প্রতি region-এর একই ধরনের RMSE ও bias সারণি।
# **কেন:** চার region-এ ভৌগোলিক ব্যর্থতার ধরন (কোন region-এ মডেল কত বেশি/কম অনুমান করে) দেখতে।
# **কীভাবে পড়বেন:** `bias` ঋণাত্মক = মডেল ওই region-এর share কম অনুমান করে। সব region-এ একই দিকে হলে নির্ধারিত দিকের সমস্যা (systematic) নয়।

# %%
region_err = error_table("Region-blocked", main.region.values)
region_err.round(2).to_csv(RESULTS / "table_17_region_blocked_error.csv")
region_err.round(2)

# %% [markdown]
# **কী করছি:** LOSO-তে প্রতি state-এর gradient boosting bias আঁকছি।
# **কেন:** প্রশ্ন: ভুলগুলো কি এলোমেলো, নাকি কিছু state পদ্ধতিগতভাবে বেশি/কম অনুমান হয়?
# **কীভাবে পড়বেন:** শূন্যের রেখা থেকে দূরের বিন্দু = বড় bias। state-গুলো bias অনুযায়ী সাজানো।

# %%
bias = loso_state["Gradient boosting | bias"].sort_values()
fig, ax = plt.subplots(figsize=(6, 9))
ax.scatter(bias, np.arange(len(bias)), s=22, color=BLUE)
ax.axvline(0, color=GREY, linewidth=1)
ax.set_yticks(np.arange(len(bias)), bias.index, fontsize=7)
ax.set(title="Leave-one-state-out bias, gradient boosting", xlabel="Mean (predicted minus actual) high-rating share, percentage points")
fig.savefig(RESULTS / "fig_07_loso_bias_per_state.png", dpi=150, bbox_inches="tight")
plt.show()

# %% [markdown]
# **Checkpoint (ধাপ ৮):** LOSO আর region-blocked-এর মধ্যে কোনটা বেশি কঠোর, এবং কেন?

# %% [markdown]
# ## ধাপ ৯: State fixed-effects check (random folds)
#
# **কী করছি:** random folds-এ (একই ১০ repeat) তিনটা linear মডেল তুলনা করছি: শুধু state (one-hot), শুধু চার feature, এবং feature + state one-hot। মডেল সরল `LinearRegression`, কোনো regularisation (ridge) নেই; one-hot-এ সব state-এর কলাম রেখে minimum-norm সমাধান নেওয়া হয়। gradient boosting ব্যবহার করিনি, যাতে "state-ধ্রুবক যোগ হলে feature-এর বাড়তি ভূমিকা কত" পরিষ্কার থাকে।
# **কেন:** প্রথম নোটবুকে state-গড় (R² অনেক বেশি) feature-মডেলের চেয়ে ভালো ছিল। জিজ্ঞাসা: state জানার পরে কি feature কিছু যোগ করে?
# **কীভাবে পড়বেন:** "features + state" যদি "state only"-র চেয়ে স্পষ্ট ভালো না হয়, তবে state জানার পর feature-এর বাড়তি পূর্বাভাস-শক্তি সামান্য।
# **সাধারণ ভুল:** random folds-এ state-মডেল ভালো দেখায় কারণ test কাউন্টির state training-এ আছে; অদেখা state-এ এটা কাজ করে না।

# %%
D = pd.get_dummies(main.state).values.astype(float)
FE_DESIGNS = {"State only (one-hot)": D, "Features only": X_all, "Features + state one-hot": np.hstack([X_all, D])}
FE = {(name, "Linear regression"): np.array([oof_predict(LinearRegression(), FOLDS["Random folds"][r], Xd)
                                            for r in range(N_REPEATS)]) for name, Xd in FE_DESIGNS.items()}
fe_table = score_table(FE)
fe_table.round(3).to_csv(RESULTS / "table_18_fixed_effects_cv.csv", index=False)
fe_table.pivot_table(index="design", columns="weighting", values=["r2", "rmse"]).round(3)

# %% [markdown]
# **কী করছি:** within-state RQ2: outcome ও চার feature (pooled SD-তে standardise করে) প্রতি state-এর গড় বিয়োগ করে (de-mean) OLS চালাচ্ছি, আর pooled (প্রথম নোটবুকের) সহগের সাথে পাশাপাশি রাখছি। CI আবার state-cluster bootstrap (একই ২০০০ draw)।
# **কেন:** pooled সহগ state-এর মধ্যকার আর state-এর ভেতরের উভয় পার্থক্য মেশায়। within-state সহগ শুধু একই state-এর কাউন্টিগুলোর তুলনা। (এটা সম্পর্ক, কারণ নয়।)
# **কীভাবে পড়বেন:** একক: প্রতি 1 SD feature-বৃদ্ধিতে share-এর পরিবর্তন (শতাংশ পয়েন্ট)। চিহ্ন বা আকার বদলালে pooled সহগের ব্যাখ্যা state-পার্থক্য মিশিয়েছিল।

# %%
def std_coefs(rows, within):
    d = main.iloc[rows]
    Xs, y = (d[FEATURES] - d[FEATURES].mean()) / d[FEATURES].std(), d.high_share * 100
    if within:
        Xs, y = Xs - Xs.groupby(d.state).transform("mean"), y - y.groupby(d.state).transform("mean")
    return LinearRegression().fit(Xs, y).coef_

all_rows = np.arange(len(main))
boot_rows = [np.concatenate([rows_of[s] for s in draw]) for draw in boot]
coef = {}
for name, within in [("Pooled", False), ("Within-state", True)]:
    b = np.array([std_coefs(r, within) for r in boot_rows])
    coef[name] = pd.DataFrame({"points_per_sd": std_coefs(all_rows, within), "ci_low": np.percentile(b, 2.5, axis=0),
                               "ci_high": np.percentile(b, 97.5, axis=0)}, index=FEATURES)

# %% [markdown]
# **কী করছি:** pooled ও within-state সহগ এক সারণিতে ও এক ছবিতে দেখাচ্ছি।
# **কেন:** প্রশ্ন: state-ধ্রুবক সরালে কোন feature-এর সম্পর্ক টেকে?
# **কীভাবে পড়বেন:** বিন্দু = সহগ, দাগ = 95% CI, ধূসর রেখা = শূন্য। যে সহগের CI শূন্য ছোঁয় তার সম্পর্ক অনিশ্চিত।

# %%
coef_table = pd.concat(coef, names=["model", "feature"]).round(2)
coef_table.to_csv(RESULTS / "table_19_within_state_coefficients.csv")
fig, ax = plt.subplots(figsize=(7.5, 3.6))
for k, (name, colour) in enumerate([("Pooled", BLUE), ("Within-state", ORANGE)]):
    c = coef[name]
    ax.errorbar(c.points_per_sd, np.arange(4)[::-1] + (k - 0.5) * 0.25, fmt="o", color=colour, label=name, capsize=3,
                xerr=[c.points_per_sd - c.ci_low, c.ci_high - c.points_per_sd])
ax.axvline(0, color=GREY, linewidth=1)
ax.set_yticks(np.arange(4)[::-1], FEATURES)
ax.set(title="Linear coefficients: pooled vs within-state", xlabel="Percentage points of high-rating share per 1 SD of feature")
ax.legend(frameon=False)
fig.savefig(RESULTS / "fig_08_pooled_vs_within_coefficients.png", dpi=150, bbox_inches="tight")
coef_table

# %% [markdown]
# **Checkpoint (ধাপ ৯):** pooled আর within-state সহগের পার্থক্য কেন "কারণ" নয়, শুধু সম্পর্কের উৎসের পার্থক্য?

# %% [markdown]
# ## ধাপ ১০: Selection check (বাদ-পড়া কাউন্টি)
#
# **কী করছি:** সব কাউন্টিকে তিন দলে ভাগ করে গুনছি: main sample, বাদ-পড়া কিন্তু outcome হিসাব করা যায় (কোনো predictor ঘর ফাঁকা), বাদ-পড়া ও outcome হিসাব করা যায় না। আরও দেখছি বাদ-পড়া দলে কয়টা কাউন্টির চারটা feature-ই বানানো যায়।
# **কেন:** ছোট-সংখ্যার ঘর publisher লুকিয়েছে, তাই বাদ-পড়া কাউন্টিগুলো পদ্ধতিগতভাবে আলাদা হতে পারে (selection bias)। সব চার feature বানানো গেলে main sample-এর মডেল দিয়ে তাদের স্কোর করতাম; না গেলে শুধু pooled share তুলনা করব।
# **কীভাবে পড়বেন:** তিন দলের যোগফল মোট কাউন্টির সমান হতে হবে। "all four features buildable" শূন্য হলে মডেল-স্কোরিং সম্ভব নয়।

# %%
excl = df[~df.in_main & df.high_share.notna()]
groups = pd.Series({"in main sample": df.in_main.sum(), "excluded, outcome computable": len(excl),
                    "excluded, outcome not computable": (~df.in_main & df.high_share.isna()).sum()})
print("Sum of groups:", groups.sum(), "| all counties:", len(df))
print("Excluded-with-outcome counties with all four features buildable:", excl[FEATURES].notna().all(axis=1).sum())
print("Blank features among excluded-with-outcome:\n", excl[FEATURES].isna().sum().to_string())
groups.to_frame("counties")

# %% [markdown]
# **কী করছি:** মডেল-স্কোরিং সম্ভব না হলে বিকল্প হিসেবে বাদ-পড়া (outcome-সহ) কাউন্টির pooled high share main sample-এর সাথে তুলনা করছি, সাথে "state-মিলানো প্রত্যাশিত share": বাদ-পড়া কাউন্টির recipient-ভর অনুযায়ী main sample-এর নিজ state-এর pooled share-এর গড়।
# **কেন:** বাদ-পড়া কাউন্টি কি শুধু ভিন্ন state-এ আছে বলে আলাদা, নাকি state ধরার পরেও আলাদা?
# **কীভাবে পড়বেন:** `excluded` ও `expected given its states` কাছাকাছি হলে ফারাক মূলত state-এর। `main sample`-এর সাথে ফারাক বড় হলে selection-এর ফল সাধারণীকরণে বাধা।

# %%
state_share = main.groupby("state").high.sum() / main.groupby("state").total.sum()
expected = (excl.total * excl.state.map(state_share)).sum() / excl.total.sum()
sel = pd.DataFrame({
    "counties": [len(main), len(excl)],
    "recipients": [main.total.sum(), excl.total.sum()],
    "pooled_high_share": [main.high.sum() / main.total.sum(), excl.high.sum() / excl.total.sum()],
    "median_recipients": [main.total.median(), excl.total.median()]}, index=["main sample", "excluded (outcome computable)"])
sel["expected_given_its_states"] = [np.nan, expected]
print("Excluded counties whose state has no main-sample county:", (~excl.state.isin(state_share.index)).sum())
sel.round(4).to_csv(RESULTS / "table_20_selection_check.csv")
sel.round(4)

# %% [markdown]
# ## ধাপ ১১: Limitation ও এই নোটবুক কী দেখায়
#
# **এই নোটবুক কী দেখায়:** প্রথম নোটবুকের মূল ফলগুলো (random-বনাম-grouped ফারাক, মডেলগুলোর ক্রম, state-গড়ের ভূমিকা) weighting, LOSO, region blocking এবং fixed-effects check-এ কতটা স্থির, তা উপরের সারণি ও ছবিগুলোতে (`table_10` থেকে `table_20`, `fig_05` থেকে `fig_08`) দেখুন। কোনো সংখ্যা এখানে হাতে লেখা হয়নি।
#
# **Limitation:**
# - ফলাফল সম্পর্ক, কারণ নয়; কোনো causal দাবি করা হচ্ছে না।
# - Region ম্যাপিং সাধারণ জ্ঞান থেকে লেখা, যাচাই হয়নি (unverified); ব্যবহারকারীকে মিলিয়ে দেখতে হবে।
# - Nadeau-Bengio সংশোধন আনুমানিক; fold স্কোর স্বাধীন নয়। grouped fold-এর স্কোর fold-এর নিজস্ব গড়ের সাপেক্ষে, তাই baseline-এর fold R² ঋণাত্মক হতে পারে।
# - Bootstrap শুধু state-নমুনার অনিশ্চয়তা ধরে; fold-বিন্যাসের পরিবর্তন আলাদা, এবং OOF-পূর্বাভাস আগে থেকেই জমা, তাই মডেল-refit-এর অনিশ্চয়তা ধরা হয়নি।
# - Hyperparameter tuning করা হয়নি (প্রথম নোটবুকের মতো); চারটা feature ছাড়া অন্য কোনো কাউন্টি-তথ্য ডেটায় নেই।
# - ছোট-সংখ্যা suppression-এর কারণে বাদ-পড়া কাউন্টিগুলোর feature নেই, তাই তাদের উপর মডেলের পারফরম্যান্স যাচাই করা যায়নি; শুধু pooled share তুলনা করা গেছে।
# - Fixed-effects মডেল সরল linear, কোনো regularisation নেই; unweighted OLS সহগ, কাউন্টি-ওজন ছাড়া।
# - Test set আলাদা রাখা হয়নি; এই নোটবুকের সব ফল CV-ভিত্তিক, তাই চূড়ান্ত একক test মূল্যায়ন (ধাপ ৯, Constitution) প্রযোজ্য নয়।
#
# **Paper-এ কী লিখবেন:** Methods-এ weighting, LOSO ও region blocking-এর নকশা; Results-এ `table_11`, `table_12`, `table_13`, `table_15`, `table_18`, `table_19`; Limitations-এ উপরের তালিকা। প্রতিটি সংখ্যা সারণি থেকে নিন।

# %% [markdown]
# **কী করছি:** ব্যবহৃত লাইব্রেরির সংস্করণ লিখে রাখছি।
# **কেন:** reproducibility।
# **কীভাবে পড়বেন:** `requirements.txt`-এর সাথে মিলিয়ে দেখুন।

# %%
import matplotlib
import scipy
import sklearn

print("numpy", np.__version__, "| pandas", pd.__version__, "| scipy", scipy.__version__,
      "| scikit-learn", sklearn.__version__, "| matplotlib", matplotlib.__version__)
