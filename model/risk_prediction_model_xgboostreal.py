import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_absolute_error
from xgboost import XGBRegressor
import os

# === LOAD TRAINING DATA (1k synthetic with predictions) ===
df_train = pd.read_csv("../data/DrLim1000Synthetic.csv")
X_train = df_train.drop(columns=["Predicted_HbA1C", "Target_HbA1C"])
y_train = df_train["Predicted_HbA1C"]

# Ensure object columns are strings
for col in X_train.select_dtypes(include="object").columns:
    X_train[col] = X_train[col].astype(str)

# === LOAD TEST DATA (5k synthetic with true Target_HbA1C) ===
df_predict = pd.read_csv("../data/DrLim5000Synthetic.csv")
y_true = df_predict["Target_HbA1C"]
X_test = df_predict.drop(columns=["Target_HbA1C"])

# Ensure categorical consistency
for col in X_test.select_dtypes(include="object").columns:
    X_test[col] = X_test[col].astype(str)

# === SANITY CHECK BEFORE PREDICTION ===
assert "Target_HbA1C" not in X_test.columns, "❌ ERROR: 'Target_HbA1C' is still in the test features!"

# === CREATE MODEL PIPELINE ===
categorical_cols = X_train.select_dtypes(include="object").columns.tolist()
preprocessor = ColumnTransformer(
    transformers=[("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols)],
    remainder="passthrough"
)

model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("xgb", XGBRegressor(n_estimators=50, learning_rate=0.1, random_state=42))
])

# === TRAIN AND PREDICT ===
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# === Evaluate with real MAE ===
mae = mean_absolute_error(y_true, y_pred)
print(f"✅ MAE between predicted and actual Target_HbA1C: {mae:.4f}")

# === Append predictions and save ===
df_predict["Predicted_HbA1C"] = y_pred

os.makedirs("results", exist_ok=True)
df_predict.to_csv("results/DrLim5000Synthetic_With_Predictions.csv", index=False)
print("📁 Saved to: results/DrLim5000Synthetic_With_Predictions.csv")
