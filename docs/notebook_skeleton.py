# %% plan
"""
Question: TODO
Hypothesis: TODO
Primary metric: balanced accuracy
Validation: 20% test held out, 5-fold x 3 repeats CV on training
Models: baseline, simple, tree ensembles; same folds and budget
"""

# %% setup
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

# %% data inspection
df = pd.read_csv(DATA_PATH)
print(df.shape)
print(df.dtypes.value_counts())
print("missing cells:", df.isna().sum().sum())
print("duplicate rows:", df.duplicated().sum())
print(df[TARGET].value_counts())
df.head()

# %% split
X = df.drop(columns=TARGET)
y = df[TARGET]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=SEED)
print(X_train.shape, X_test.shape)

# %% eda
y_train.value_counts().plot.bar()
plt.title("Class counts (train only)")
plt.ylabel("rows")
plt.savefig("../results/figures/class_counts.png", dpi=150, bbox_inches="tight")
plt.show()

# %% preprocessing
numeric = X_train.select_dtypes("number").columns
categorical = X_train.columns.difference(numeric)
preprocess = ColumnTransformer([
    ("num", Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), numeric),
    ("cat", Pipeline([("impute", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore"))]), categorical),
])

# %% models
models = {
    "Majority baseline": DummyClassifier(strategy="most_frequent"),
    "Logistic regression": LogisticRegression(max_iter=1000),
    "Random forest": RandomForestClassifier(random_state=SEED),
    "Gradient boosting": HistGradientBoostingClassifier(random_state=SEED),
}
pipes = {name: Pipeline([("prep", preprocess), ("model", m)]) for name, m in models.items()}

# %% cross-validation
cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=3, random_state=SEED)
scores = {
    name: cross_validate(p, X_train, y_train, cv=cv, scoring="balanced_accuracy")["test_score"]
    for name, p in pipes.items()
}
cv_table = pd.DataFrame(scores)
summary = cv_table.agg(["mean", "std"]).T.round(3)
summary

# %% cv boxplot
cv_table.plot.box(vert=False)
plt.xlabel("balanced accuracy (15 CV scores per model)")
plt.savefig("../results/figures/cv_boxplot.png", dpi=150, bbox_inches="tight")
plt.show()

# %% final test
best = summary["mean"].idxmax()
final = pipes[best].fit(X_train, y_train)
y_pred = final.predict(X_test)
print("Chosen by CV:", best)
print("Test balanced accuracy:", round(balanced_accuracy_score(y_test, y_pred), 3))
print(classification_report(y_test, y_pred))
ConfusionMatrixDisplay.from_predictions(y_test, y_pred)
imp = permutation_importance(final, X_test, y_test, scoring="balanced_accuracy", n_repeats=10, random_state=SEED)

# %% importance
pd.Series(imp.importances_mean, index=X.columns).nlargest(10).sort_values().plot.barh()
plt.xlabel("drop in balanced accuracy")
plt.savefig("../results/figures/permutation_importance.png", dpi=150, bbox_inches="tight")
plt.show()
