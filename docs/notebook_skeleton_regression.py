# %% plan
"""
Question: TODO
Hypothesis: TODO
Primary metric: RMSE (secondary MAE, R2)
Validation: 20% test held out, 5-fold x 3 repeats CV on training
Models: baseline, simple, tree ensembles; same folds and budget
"""

# %% setup
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

# %% data inspection
df = pd.read_csv(DATA_PATH)
print(df.shape)
print(df.dtypes.value_counts())
print("missing cells:", df.isna().sum().sum())
print("duplicate rows:", df.duplicated().sum())
print(df[TARGET].describe().round(1))
df.head()

# %% split
X = df.drop(columns=TARGET)
y = df[TARGET]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=SEED)
print(X_train.shape, X_test.shape)

# %% eda
y_train.plot.hist(bins=30)
plt.title("Target distribution (train only)")
plt.xlabel("target")
plt.ylabel("rows")
plt.savefig("../results/figures/target_hist.png", dpi=150, bbox_inches="tight")
plt.show()

# %% preprocessing
preprocess = StandardScaler()

# %% models
models = {
    "Mean baseline": DummyRegressor(strategy="mean"),
    "Ridge": Ridge(),
    "Random forest": RandomForestRegressor(random_state=SEED),
    "Gradient boosting": HistGradientBoostingRegressor(random_state=SEED),
}
pipes = {name: Pipeline([("prep", preprocess), ("model", m)]) for name, m in models.items()}

# %% cross-validation
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

# %% cv boxplot
cv_table.plot.box(vert=False)
plt.title("CV RMSE by model (training data only)")
plt.xlabel("RMSE (target units, 15 CV scores per model; lower is better)")
plt.savefig("../results/figures/cv_boxplot.png", dpi=150, bbox_inches="tight")
plt.show()

# %% final test
best = summary["rmse_mean"].idxmin()
final = pipes[best].fit(X_train, y_train)
y_pred = final.predict(X_test)
print("Chosen by CV:", best)
print("Test RMSE:", round(root_mean_squared_error(y_test, y_pred), 3))
print("Test MAE:", round(mean_absolute_error(y_test, y_pred), 3))
print("Test R2:", round(r2_score(y_test, y_pred), 3))
test_result = pd.DataFrame({"actual": y_test, "predicted": y_pred})
imp = permutation_importance(final, X_test, y_test, scoring="neg_root_mean_squared_error", n_repeats=10, random_state=SEED)

# %% error analysis
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

# %% importance
pd.Series(imp.importances_mean, index=X.columns).nlargest(10).sort_values().plot.barh()
plt.title("Permutation importance (test)")
plt.xlabel("increase in RMSE (target units)")
plt.savefig("../results/figures/permutation_importance.png", dpi=150, bbox_inches="tight")
plt.show()
