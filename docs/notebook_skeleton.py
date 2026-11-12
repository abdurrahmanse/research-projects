# %% [markdown]
# # TODO: প্রজেক্টের নাম: ধাপে ধাপে রিসার্চ নোটবুক
#
# **রোডম্যাপ:** ১ সমস্যা ও metric → ২ ডেটা পরিচিতি → ৩ split → ৪ EDA → ৫ preprocessing → ৬ মডেল → ৭ cross-validation → ৮ চূড়ান্ত test → ৯ ব্যাখ্যা → ১০ limitation ও paper
#
# **শব্দকোষ**
# - **Data leakage:** test ডেটার তথ্য ভুলবশত training-এ ঢুকে পড়া, ফলে ফল আসল থেকে ভালো দেখায়।
# - **Baseline:** সবচেয়ে সহজ উত্তর (যেমন সবসময় বড় class বলা)। কোনো মডেল এটা না হারালে সেটা কাজের না।
# - **Cross-validation (CV):** training ডেটাকে ভাগ করে বারবার পরীক্ষা, যাতে একটা ভাগ্যবান split-এর ওপর নির্ভর না করতে হয়।
# - **Pipeline:** preprocessing আর মডেল একসাথে বাঁধা, যাতে প্রতিটা fold-এ preprocessing শুধু training অংশ থেকে শেখে।

# %% [markdown]
# ## ধাপ ১: সমস্যা, hypothesis, metric (মডেল চালানোর আগেই লেখা)
#
# - **গবেষণা প্রশ্ন:** TODO
# - **Hypothesis:** TODO
# - **Primary metric:** balanced accuracy। class সংখ্যা অসমান হলে সাধারণ accuracy বিভ্রান্ত করে, তাই প্রতিটা class-এর recall-এর গড় নেওয়া হয়।
# - **Validation:** 20% test আলাদা রাখা হবে, বাকি training অংশে 5-fold × 3 বার CV।
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
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import ConfusionMatrixDisplay, balanced_accuracy_score, classification_report
from sklearn.model_selection import RepeatedStratifiedKFold, cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

SEED = 42
DATA_PATH = "../data/data.csv"  # TODO
TARGET = "target"  # TODO
Path("../results/figures").mkdir(parents=True, exist_ok=True)

# %% [markdown]
# ## ধাপ ৩: ডেটা পরিচিতি (data card-এর কাঁচামাল)
#
# **কী করছি:** ফাইল পড়ে আকার, ধরন, missing, duplicate আর target-এর গণনা দেখছি।
# **কেন:** ডেটা না দেখে মডেল বানালে ভুল ধারণার ওপর কাজ হয়। duplicate থাকলে train আর test-এ একই সারি পড়ে leakage হতে পারে।
# **কীভাবে পড়বেন:** target-এর একটা class অনেক ছোট হলে imbalance আছে; duplicate শূন্য না হলে কারণ খুঁজুন।
# **সাধারণ ভুল:** এখানেই missing মান ভরে ফেলা। ভরার কাজ পরে Pipeline-এর ভেতরে হবে।

# %%
df = pd.read_csv(DATA_PATH)
print(df.shape)
print(df.dtypes.value_counts())
print("missing cells:", df.isna().sum().sum())
print("duplicate rows:", df.duplicated().sum())
print(df[TARGET].value_counts())
df.head()

# %% [markdown]
# ## ধাপ ৪: Train/test ভাগ (সবকিছুর আগে)
#
# **কী করছি:** 20% সারি test হিসেবে সরিয়ে রাখছি, class অনুপাত বজায় রেখে (`stratify`)।
# **কেন:** test ডেটা শুধু শেষে একবার ব্যবহার হবে। এর আগে কিছু শেখা বা বেছে নেওয়া হলে ফল অতিরঞ্জিত হয়।
# **কীভাবে পড়বেন:** দুই অংশের আকার প্রায় 80/20 হওয়ার কথা।
# **সাধারণ ভুল:** scaling বা imputation করে তারপর split করা, এটাই সবচেয়ে সাধারণ leakage।
# **Checkpoint:** ব্যক্তি/এলাকা/সময়ের গ্রুপ থাকলে সাধারণ split কেন যথেষ্ট নয়?

# %%
X = df.drop(columns=TARGET)
y = df[TARGET]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=SEED)
print(X_train.shape, X_test.shape)

# %% [markdown]
# ## ধাপ ৫: EDA (শুধু training ডেটায়)
#
# **কী করছি:** training অংশে প্রতিটা class-এ কতগুলো সারি আছে তার bar chart।
# **কেন:** imbalance চোখে দেখলে metric ও মডেলের সিদ্ধান্ত নেওয়া সহজ হয়।
# **কীভাবে পড়বেন:** bar-এর উচ্চতা খুব অসমান হলে accuracy-র ওপর ভরসা করবেন না।

# %%
y_train.value_counts().plot.bar()
plt.title("Class counts (train only)")
plt.ylabel("rows")
plt.savefig("../results/figures/class_counts.png", dpi=150, bbox_inches="tight")
plt.show()

# %% [markdown]
# ## ধাপ ৬: Preprocessing Pipeline
#
# **কী করছি:** সংখ্যার কলামে median দিয়ে missing ভরা ও scaling; ক্যাটাগরির কলামে most-frequent দিয়ে ভরা ও one-hot encoding।
# **কেন:** Pipeline-এর ভেতরে থাকলে প্রতিটা CV fold-এ এগুলো শুধু সেই fold-এর training অংশ থেকে শেখে, leakage হয় না।
# **কীভাবে পড়বেন:** আউটপুট নেই; কেবল সংজ্ঞা।
# **নোট:** ধাপ ৩-এর আউটপুটে missing বা ক্যাটাগরি কলাম না থাকলে সেই শাখা বাদ দিন (বাড়তি কোড চলবে না)।

# %%
numeric = X_train.select_dtypes("number").columns
categorical = X_train.columns.difference(numeric)
preprocess = ColumnTransformer([
    ("num", Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), numeric),
    ("cat", Pipeline([("impute", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore"))]), categorical),
])

# %% [markdown]
# ## ধাপ ৭: মডেলের তালিকা (সবার জন্য একই শর্ত)
#
# **কী করছি:** একটা baseline, একটা সরল মডেল (logistic regression), আর দুটো শক্তিশালী tree মডেল।
# **কেন:** সরল মডেল বা baseline হারাতে না পারলে জটিল মডেলের কোনো দাবি টেকে না। সব মডেল একই preprocessing ও একই fold পাবে।

# %%
models = {
    "Majority baseline": DummyClassifier(strategy="most_frequent"),
    "Logistic regression": LogisticRegression(max_iter=1000),
    "Random forest": RandomForestClassifier(random_state=SEED),
    "Gradient boosting": HistGradientBoostingClassifier(random_state=SEED),
}
pipes = {name: Pipeline([("prep", preprocess), ("model", m)]) for name, m in models.items()}

# %% [markdown]
# ## ধাপ ৮: Cross-validation (uncertainty সহ)
#
# **কী করছি:** training ডেটায় 5-fold CV তিনবার (মোট 15টা স্কোর প্রতি মডেলে), সব মডেলে একই fold।
# **কেন:** একটা স্কোর ভাগ্য হতে পারে; 15টা স্কোরের গড় ও ছড়ানো দেখলে বোঝা যায় পার্থক্য আসল কি না।
# **কীভাবে পড়বেন:** `mean` বেশি হলে ভালো; `std` বড় হলে ফল অস্থির। দুই মডেলের mean কাছাকাছি আর std-র সীমা ওভারল্যাপ করলে বলা যাবে না একটা অন্যটার চেয়ে ভালো।

# %%
cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=3, random_state=SEED)
scores = {
    name: cross_validate(p, X_train, y_train, cv=cv, scoring="balanced_accuracy")["test_score"]
    for name, p in pipes.items()
}
cv_table = pd.DataFrame(scores)
summary = cv_table.agg(["mean", "std"]).T.round(3)
summary

# %% [markdown]
# **ছবিতে দেখা:** প্রতিটা মডেলের 15টা স্কোরের ছড়ানো। box যত ছোট, মডেল তত স্থিতিশীল; দুটো box বেশি ওভারল্যাপ করলে পার্থক্য বিশ্বাসযোগ্য নয়।

# %%
cv_table.plot.box(vert=False)
plt.xlabel("balanced accuracy (15 CV scores per model)")
plt.savefig("../results/figures/cv_boxplot.png", dpi=150, bbox_inches="tight")
plt.show()

# %% [markdown]
# ## ধাপ ৯: চূড়ান্ত test মূল্যায়ন (একবারই)
#
# **কী করছি:** CV-তে সেরা mean পাওয়া মডেলকে পুরো training ডেটায় শিখিয়ে test ডেটায় একবার চালাচ্ছি; সঙ্গে confusion matrix ও permutation importance।
# **কেন:** test-এর স্কোর দেখে মডেল বদলালে test আর test থাকে না।
# **কীভাবে পড়বেন:** test স্কোর CV mean-এর খুব কাছাকাছি হওয়া উচিত। অনেক বেশি ভালো হলে leakage সন্দেহ করুন, অনেক খারাপ হলে overfitting।

# %%
best = summary["mean"].idxmax()
final = pipes[best].fit(X_train, y_train)
y_pred = final.predict(X_test)
print("Chosen by CV:", best)
print("Test balanced accuracy:", round(balanced_accuracy_score(y_test, y_pred), 3))
print(classification_report(y_test, y_pred))
ConfusionMatrixDisplay.from_predictions(y_test, y_pred)
imp = permutation_importance(final, X_test, y_test, scoring="balanced_accuracy", n_repeats=10, random_state=SEED)

# %% [markdown]
# ## ধাপ ১০: কোন ফিচার গুরুত্বপূর্ণ
#
# **কী করছি:** permutation importance: একটা ফিচারের মান এলোমেলো করলে স্কোর কতটা কমে।
# **কীভাবে পড়বেন:** বড় bar মানে মডেল ওই ফিচারের ওপর বেশি নির্ভরশীল। এটা কার্যকারণ নয়, শুধু মডেলের নির্ভরতা।

# %%
pd.Series(imp.importances_mean, index=X.columns).nlargest(10).sort_values().plot.barh()
plt.xlabel("drop in balanced accuracy")
plt.savefig("../results/figures/permutation_importance.png", dpi=150, bbox_inches="tight")
plt.show()

# %% [markdown]
# ## ধাপ ১১: Limitation ও সিদ্ধান্ত (আউটপুট দেখে নিজে লিখুন)
#
# - hypothesis সত্য হলো কি না, কোন সংখ্যা দেখে (উপরের টেবিল/আউটপুট উল্লেখ করুন):
# - কোন মডেল কার চেয়ে *উল্লেখযোগ্যভাবে* ভালো, আর কোনগুলো আলাদা করা যায়নি:
# - এই ডেটার সীমা (আকার, সংগ্রহ পদ্ধতি, গ্রুপ কাঠামো, imbalance):
# - যা এই গবেষণা প্রমাণ করে না:
#
# **Paper-এ কোথায় যাবে:** ধাপ ১ → Introduction/Objectives, ৩ → Dataset, ৪-৬ → Methodology, ৮-৯ → Results, ১১ → Discussion/Limitations।
