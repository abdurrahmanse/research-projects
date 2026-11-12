# REGRESSION skeleton (tested). Classification version: docs/notebook_skeleton.py. Delete this line in the notebook.
# %% [markdown]
# TODO: প্রজেক্টের নাম: ধাপে ধাপে রিসার্চ নোটবুক (regression)
#
# **রোডম্যাপ:** ১ সমস্যা ও metric → ২ লাইব্রেরি → ৩ ডেটা পরিচিতি → ৪ split → ৫ EDA → ৬ preprocessing → ৭ মডেল → ৮ cross-validation → ৯ চূড়ান্ত test → ১০ ব্যাখ্যা → ১১ limitation ও paper
#
# **শব্দকোষ**
# - **Data leakage:** test ডেটার তথ্য ভুলবশত training-এ ঢুকে পড়া, ফলে ফল আসল থেকে ভালো দেখায়।
# - **Baseline:** সবচেয়ে সহজ উত্তর (এখানে সবসময় training-এর গড় মান বলা)। কোনো মডেল এটা না হারালে সেটা কাজের না।
# - **RMSE:** পূর্বাভাসের ভুলের বর্গের গড়ের বর্গমূল; target-এর একক একই, ছোট হলে ভালো, বড় ভুলকে বেশি শাস্তি দেয়।
# - **MAE:** ভুলের পরম মানের গড়; **R²:** মডেল baseline-এর তুলনায় কতটা variance ব্যাখ্যা করে (0 মানে গড়ের সমান)।
# - **Cross-validation (CV):** training ডেটাকে ভাগ করে বারবার পরীক্ষা, যাতে একটা ভাগ্যবান split-এর ওপর নির্ভর না করতে হয়।
# - **Pipeline:** preprocessing আর মডেল একসাথে বাঁধা, যাতে প্রতিটা fold-এ preprocessing শুধু training অংশ থেকে শেখে।

# %% [markdown]
# ## ধাপ ১: সমস্যা, hypothesis, metric (মডেল চালানোর আগেই লেখা)
#
# - **গবেষণা প্রশ্ন:** TODO (যেমন: Ridge, random forest ও gradient boosting-এর মধ্যে কোনটা `target` সবচেয়ে ভালো পূর্বাভাস দেয়, এবং তারা কি গড়-মান baseline-কে হারায়?)
# - **Hypothesis H1:** TODO (যেমন: প্রতিটা মডেলের CV RMSE গড়-মান baseline-এর চেয়ে কম হবে)।
# - **Hypothesis H2:** TODO
# - **Primary metric:** RMSE (target-এর এককেই ভুল মাপে)। Secondary: MAE ও R²।
# - **Validation:** সারিগুলো iid ধরা হচ্ছে, কোনো গ্রুপ নেই। 20% test আলাদা রাখা হবে, বাকি training অংশে 5-fold × 3 বার CV (`RepeatedKFold`)।
#
# **Checkpoint:** metric আগে ঠিক করা কেন দরকার?

# %% [markdown]
# ## ধাপ ২: লাইব্রেরি ও সেটিংস
#
# **কী করছি:** দরকারি লাইব্রেরি আনছি আর ফাইলের পথ, target কলাম, seed ঠিক করছি।
# **কেন:** একই seed থাকলে অন্য কেউ চালালে একই ফল পাবে (reproducibility)।
# **কীভাবে পড়বেন:** কোনো আউটপুট নেই; error না এলেই হলো।

# %%
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.model_selection import RepeatedKFold, cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

SEED = 42
DATA_PATH = "../data/data.csv"  # TODO
TARGET = "target"  # TODO
Path("../results/figures").mkdir(parents=True, exist_ok=True)

# %% [markdown]
# ## ধাপ ৩: ডেটা পরিচিতি (data card-এর কাঁচামাল)
#
# **কী করছি:** ফাইল পড়ে আকার, ধরন, missing, duplicate আর target-এর সারসংক্ষেপ দেখছি।
# **কেন:** ডেটা না দেখে মডেল বানালে ভুল ধারণার ওপর কাজ হয়। duplicate থাকলে train আর test-এ একই সারি পড়ে leakage হতে পারে। regression-এ class গণনার বদলে target-এর বণ্টন (গড়, ছড়ানো, min/max) দেখি।
# **কীভাবে পড়বেন:** missing/duplicate শূন্য না হলে কারণ খুঁজুন। target-এর `std` হলো baseline-এর RMSE-র মোটামুটি মাপকাঠি: কোনো মডেলের RMSE এর কাছাকাছি হলে সে প্রায় কিছুই শেখেনি।
# **সাধারণ ভুল:** এখানেই missing মান ভরে ফেলা। ভরার কাজ পরে Pipeline-এর ভেতরে হবে।
#
# **Data card:** TODO: উৎস, লাইসেন্স, কলামের অর্থ, target-এর সংজ্ঞা, গ্রুপ/সময়ের কলাম আছে কি না, জানা সমস্যা (যাচাই না করা তথ্য "unverified" লিখুন)।

# %%
df = pd.read_csv(DATA_PATH)
print(df.shape)
print(df.dtypes.value_counts())
print("missing cells:", df.isna().sum().sum())
print("duplicate rows:", df.duplicated().sum())
print(df[TARGET].describe().round(1))
df.head()

# %% [markdown]
# ## ধাপ ৪: Train/test ভাগ (সবকিছুর আগে)
#
# **কী করছি:** 20% সারি test হিসেবে সরিয়ে রাখছি। target ক্রমাগত সংখ্যা, তাই `stratify` নেই।
# **কেন:** test ডেটা শুধু শেষে একবার ব্যবহার হবে। এর আগে কিছু শেখা বা বেছে নেওয়া হলে ফল অতিরঞ্জিত হয়।
# **কীভাবে পড়বেন:** দুই অংশের আকার প্রায় 80/20 হওয়ার কথা।
# **সাধারণ ভুল:** scaling করে তারপর split করা, এটাই সবচেয়ে সাধারণ leakage।
# **Checkpoint:** ব্যক্তি/এলাকা/সময়ের গ্রুপ থাকলে সাধারণ split কেন যথেষ্ট নয়?

# %%
X = df.drop(columns=TARGET)
y = df[TARGET]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=SEED)
print(X_train.shape, X_test.shape)

# %% [markdown]
# ## ধাপ ৫: EDA (শুধু training ডেটায়)
#
# **প্রশ্ন:** target-এর বণ্টন কেমন: খুব বাঁকা বা অদ্ভুত মান আছে কি, যা RMSE-কে প্রভাবিত করবে?
# **কী করছি:** training অংশের target-এর histogram।
# **কীভাবে পড়বেন:** একদিকে লম্বা লেজ থাকলে বড় ভুল RMSE-কে অনেক বাড়াবে; তখন MAE-ও পাশে দেখা জরুরি।

# %%
y_train.plot.hist(bins=30)
plt.title("Target distribution (train only)")
plt.xlabel("target")
plt.ylabel("rows")
plt.savefig("../results/figures/target_hist.png", dpi=150, bbox_inches="tight")
plt.show()

# %% [markdown]
# ## ধাপ ৬: Preprocessing Pipeline
#
# **কী করছি:** শুধু ততটুকুই রাখুন যা ধাপ ৩-এর আউটপুট দাবি করে। এখানে সব ফিচার সংখ্যাসূচক ও missing নেই ধরে শুধু `StandardScaler`। missing থাকলে `SimpleImputer(strategy="median")` আর ক্যাটাগরি কলাম থাকলে `OneHotEncoder(handle_unknown="ignore")` সহ `ColumnTransformer` যোগ করুন (ক্লাসিফিকেশন skeleton দেখুন)। যে শাখা লাগে না তা বাদ দিন।
# **কেন:** Ridge স্কেল-সংবেদনশীল। scaler Pipeline-এর ভেতরে থাকলে প্রতিটা CV fold-এ শুধু training অংশ থেকে শেখে, leakage হয় না। tree মডেলও একই preprocessing পায়, যাতে তুলনা ন্যায্য থাকে।
# **কীভাবে পড়বেন:** আউটপুট নেই; কেবল সংজ্ঞা।

# %%
preprocess = StandardScaler()

# %% [markdown]
# ## ধাপ ৭: মডেলের তালিকা (সবার জন্য একই শর্ত)
#
# **কী করছি:** একটা baseline (গড় মান), একটা সরল মডেল (Ridge), আর দুটো শক্তিশালী tree মডেল।
# **কেন:** সরল মডেল বা baseline হারাতে না পারলে জটিল মডেলের কোনো দাবি টেকে না। সব মডেল একই preprocessing ও একই fold পাবে। কোনো মডেলেরই hyperparameter tune করা হয়নি (default), তাই বাজেট সমান; তবে এটা একটা সীমাবদ্ধতা।

# %%
models = {
    "Mean baseline": DummyRegressor(strategy="mean"),
    "Ridge": Ridge(),
    "Random forest": RandomForestRegressor(random_state=SEED),
    "Gradient boosting": HistGradientBoostingRegressor(random_state=SEED),
}
pipes = {name: Pipeline([("prep", preprocess), ("model", m)]) for name, m in models.items()}

# %% [markdown]
# ## ধাপ ৮: Cross-validation (uncertainty সহ)
#
# **কী করছি:** training ডেটায় 5-fold CV তিনবার (মোট 15টা স্কোর প্রতি মডেলে), সব মডেলে একই fold। Primary RMSE, সঙ্গে MAE ও R²।
# **কেন:** একটা স্কোর ভাগ্য হতে পারে; 15টা স্কোরের গড় ও ছড়ানো দেখলে বোঝা যায় পার্থক্য আসল কি না।
# **কীভাবে পড়বেন:** RMSE ও MAE-তে **কম** ভালো, R²-তে **বেশি** ভালো। `std` বড় হলে ফল অস্থির। দুই মডেলের mean কাছাকাছি আর std-র সীমা ওভারল্যাপ করলে বলা যাবে না একটা অন্যটার চেয়ে ভালো।
# **সাধারণ ভুল:** sklearn-এর `neg_...` স্কোর (যেমন `neg_root_mean_squared_error`) ঋণাত্মক আসে; চিহ্ন উল্টে নিতে হয়। আর সেরা মডেল বাছতে error metric-এ `idxmin` (কম ভালো), R²-তে `idxmax` (বেশি ভালো)।

# %%
cv = RepeatedKFold(n_splits=5, n_repeats=3, random_state=SEED)
metrics = {"rmse": "neg_root_mean_squared_error", "mae": "neg_mean_absolute_error", "r2": "r2"}
runs = {name: cross_validate(p, X_train, y_train, cv=cv, scoring=metrics) for name, p in pipes.items()}
cv_table = pd.DataFrame({n: -r["test_rmse"] for n, r in runs.items()})
summary = pd.DataFrame({
    "rmse_mean": cv_table.mean(),
    "rmse_std": cv_table.std(),
    "mae_mean": pd.Series({n: -r["test_mae"].mean() for n, r in runs.items()}),
    "r2_mean": pd.Series({n: r["test_r2"].mean() for n, r in runs.items()}),
}).round(3)
summary

# %% [markdown]
# **ছবিতে দেখা:** প্রতিটা মডেলের 15টা RMSE স্কোরের ছড়ানো। box যত ছোট, মডেল তত স্থিতিশীল; বাঁয়ে থাকা box ভালো (কম ভুল); দুটো box বেশি ওভারল্যাপ করলে পার্থক্য বিশ্বাসযোগ্য নয়।

# %%
cv_table.plot.box(vert=False)
plt.title("CV RMSE by model (training data only)")
plt.xlabel("RMSE (target units, 15 CV scores per model; lower is better)")
plt.savefig("../results/figures/cv_boxplot.png", dpi=150, bbox_inches="tight")
plt.show()

# %% [markdown]
# ## ধাপ ৯: চূড়ান্ত test মূল্যায়ন (একবারই)
#
# **কী করছি:** CV-তে সর্বনিম্ন mean RMSE পাওয়া মডেলকে পুরো training ডেটায় শিখিয়ে test ডেটায় একবার চালাচ্ছি; একই সঙ্গে test-এর পূর্বাভাস, ভুল আর permutation importance এই একটাই cell-এ রেখে নিচের ধাপগুলোতে test আর ছোঁয়া হবে না।
# **কেন:** test-এর স্কোর দেখে মডেল বদলালে test আর test থাকে না।
# **কীভাবে পড়বেন:** test RMSE CV mean-এর কাছাকাছি হওয়া উচিত। অনেক ভালো হলে leakage সন্দেহ করুন, অনেক খারাপ হলে overfitting। baseline-এর সঙ্গে তুলনার জন্য ধাপ ৮-এর টেবিল দেখুন।

# %%
best = summary["rmse_mean"].idxmin()
final = pipes[best].fit(X_train, y_train)
y_pred = final.predict(X_test)
print("Chosen by CV:", best)
print("Test RMSE:", round(root_mean_squared_error(y_test, y_pred), 3))
print("Test MAE:", round(mean_absolute_error(y_test, y_pred), 3))
print("Test R2:", round(r2_score(y_test, y_pred), 3))
test_result = pd.DataFrame({"actual": y_test, "predicted": y_pred})
imp = permutation_importance(final, X_test, y_test, scoring="neg_root_mean_squared_error", n_repeats=10, random_state=SEED)

# %% [markdown]
# ## ধাপ ১০ক: ভুলের ধরন (predicted vs actual, residual)
#
# **প্রশ্ন:** মডেলের ভুল কি সবখানে সমান, নাকি নির্দিষ্ট মানের রোগীতে পদ্ধতিগতভাবে বেশি?
# **কীভাবে পড়বেন:** বাঁয়ের ছবিতে বিন্দুগুলো y=x রেখার কাছে থাকলে ভালো। ডানের ছবিতে residual (actual − predicted) শূন্য রেখার চারপাশে এলোমেলো থাকলে ভালো; বাঁকা বা ফানেল আকার থাকলে মডেল কিছু অঞ্চলে পদ্ধতিগতভাবে ভুল করছে।

# %%
fig, ax = plt.subplots(1, 2, figsize=(10, 4))
ax[0].scatter(test_result["actual"], test_result["predicted"])
lims = [test_result.min().min(), test_result.max().max()]
ax[0].plot(lims, lims, color="grey")
ax[0].set(title="Predicted vs actual (test)", xlabel="actual", ylabel="predicted")
ax[1].scatter(test_result["predicted"], test_result["actual"] - test_result["predicted"])
ax[1].axhline(0, color="grey")
ax[1].set(title="Residuals (test)", xlabel="predicted", ylabel="actual - predicted")
plt.savefig("../results/figures/pred_vs_actual_residuals.png", dpi=150, bbox_inches="tight")
plt.show()

# %% [markdown]
# ## ধাপ ১০খ: কোন ফিচার গুরুত্বপূর্ণ
#
# **কী করছি:** permutation importance: একটা ফিচারের মান এলোমেলো করলে RMSE কতটা বাড়ে।
# **কীভাবে পড়বেন:** বড় bar মানে মডেল ওই ফিচারের ওপর বেশি নির্ভরশীল। এটা কার্যকারণ নয়, শুধু মডেলের নির্ভরতা। ফিচারগুলো পরস্পর সম্পর্কিত (যেমন s1, s2) হলে গুরুত্ব তাদের মধ্যে ভাগ হয়ে যায়।

# %%
pd.Series(imp.importances_mean, index=X.columns).nlargest(10).sort_values().plot.barh()
plt.title("Permutation importance (test)")
plt.xlabel("increase in RMSE (target units)")
plt.savefig("../results/figures/permutation_importance.png", dpi=150, bbox_inches="tight")
plt.show()

# %% [markdown]
# ## ধাপ ১১: Limitation ও সিদ্ধান্ত (আউটপুট দেখে নিজে লিখুন)
#
# - H1 ও H2 সত্য হলো কি না, কোন সংখ্যা দেখে (ধাপ ৮-এর টেবিল ও ধাপ ৯-এর আউটপুট উল্লেখ করুন):
# - কোন মডেল কার চেয়ে *উল্লেখযোগ্যভাবে* ভালো, আর কোনগুলো আলাদা করা যায়নি (CV box ওভারল্যাপ দেখুন):
# - এই ডেটার সীমা (আকার, test অংশ ছোট হলে স্কোর নড়বড়ে, hyperparameter tuning হয়েছে কি না, সংগ্রহ পদ্ধতি):
# - যা এই গবেষণা প্রমাণ করে না: কার্যকারণ সম্পর্ক, বা অন্য জনগোষ্ঠীতে সাধারণীকরণ।
#
# **Paper-এ কোথায় যাবে:** ধাপ ১ → Introduction/Objectives, ৩ → Dataset, ৪-৭ → Methodology, ৮-৯ → Results, ১০ → Error analysis, ১১ → Discussion/Limitations।
