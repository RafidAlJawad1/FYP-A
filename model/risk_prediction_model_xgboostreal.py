import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_absolute_error
from xgboost import XGBRegressor
import numpy as np
import os
import joblib

# === LOAD TRAINING DATA (5k synthetic) ===
df_train = pd.read_csv("../data/Normalized_DrLim_Dataset_5000.csv")
df_train.columns = df_train.columns.str.strip()

# Define numeric columns
numeric_columns = [
    "HbA1c - After 1st Visit",
    "HbA1c - After 2nd Visit",
    "HbA1c - Before 1st Visit (Relabeled)",
    "DDS - Before 1st Visit",
    "DDS - After 2nd Visit",
    "FVG - Before 1st Visit (Relabeled)",
    "FVG - After 1st Visit",
    "FVG - After 2nd Visit",
    "Freq SMBG",
    "Freq Hypo",
    "Freq of Visits",
    "Duration",
    "eGFR"
]

# Force numeric types
for col in numeric_columns:
    df_train[col] = pd.to_numeric(df_train[col], errors='coerce')

# Fill missing values with median (no inplace=True)
for col in numeric_columns:
    median_value = df_train[col].median()
    df_train[col] = df_train[col].fillna(median_value)

# Clip outliers
df_train["eGFR"] = df_train["eGFR"].clip(lower=15, upper=120)
df_train["Duration"] = df_train["Duration"].clip(lower=0, upper=40)
df_train["HbA1c - After 2nd Visit"] = df_train["HbA1c - After 2nd Visit"].clip(lower=4, upper=14)

# Create Duration Buckets
df_train["Duration Bucket"] = pd.cut(df_train["Duration"], bins=[0,5,10,20,40], labels=["0-5","5-10","10-20","20-40"])
df_train["Duration Bucket"] = df_train["Duration Bucket"].astype(str)

# === FEATURE ENGINEERING ===
df_train["HbA1c Change After 1st Visit"] = df_train["HbA1c - After 1st Visit"] - df_train["HbA1c - Before 1st Visit (Relabeled)"]
df_train["HbA1c Change After 2nd Visit"] = df_train["HbA1c - After 2nd Visit"] - df_train["HbA1c - Before 1st Visit (Relabeled)"]
df_train["DDS Change"] = df_train["DDS - After 2nd Visit"] - df_train["DDS - Before 1st Visit"]
df_train["FVG Change After 1st Visit"] = df_train["FVG - After 1st Visit"] - df_train["FVG - Before 1st Visit (Relabeled)"]
df_train["FVG Change After 2nd Visit"] = df_train["FVG - After 2nd Visit"] - df_train["FVG - Before 1st Visit (Relabeled)"]
df_train["Compliance Score"] = df_train["Freq SMBG"] * 0.6 + df_train["Freq of Visits"] * 0.4
df_train["Log Duration"] = np.log1p(df_train["Duration"])

# Define features and target
X_train = df_train.drop(columns=["Target HbA1c"])
y_train = df_train["Target HbA1c"]

# === LOAD TEST DATA (1k synthetic) ===
df_test = pd.read_csv("../data/Normalized_DrLim_Dataset_1000.csv")
df_test.columns = df_test.columns.str.strip()

for col in numeric_columns:
    df_test[col] = pd.to_numeric(df_test[col], errors='coerce')
    median_value = df_test[col].median()
    df_test[col] = df_test[col].fillna(median_value)

df_test["eGFR"] = df_test["eGFR"].clip(lower=15, upper=120)
df_test["Duration"] = df_test["Duration"].clip(lower=0, upper=40)
df_test["HbA1c - After 2nd Visit"] = df_test["HbA1c - After 2nd Visit"].clip(lower=4, upper=14)
df_test["Duration Bucket"] = pd.cut(df_test["Duration"], bins=[0,5,10,20,40], labels=["0-5","5-10","10-20","20-40"])
df_test["Duration Bucket"] = df_test["Duration Bucket"].astype(str)

# Feature Engineering on Test Set
df_test["HbA1c Change After 1st Visit"] = df_test["HbA1c - After 1st Visit"] - df_test["HbA1c - Before 1st Visit (Relabeled)"]
df_test["HbA1c Change After 2nd Visit"] = df_test["HbA1c - After 2nd Visit"] - df_test["HbA1c - Before 1st Visit (Relabeled)"]
df_test["DDS Change"] = df_test["DDS - After 2nd Visit"] - df_test["DDS - Before 1st Visit"]
df_test["FVG Change After 1st Visit"] = df_test["FVG - After 1st Visit"] - df_test["FVG - Before 1st Visit (Relabeled)"]
df_test["FVG Change After 2nd Visit"] = df_test["FVG - After 2nd Visit"] - df_test["FVG - Before 1st Visit (Relabeled)"]
df_test["Compliance Score"] = df_test["Freq SMBG"] * 0.6 + df_test["Freq of Visits"] * 0.4
df_test["Log Duration"] = np.log1p(df_test["Duration"])

X_test = df_test.drop(columns=["Target HbA1c"])
y_true = df_test["Target HbA1c"]

# === FORCE FINAL CLEAN TYPES ===

# Force numeric columns properly
for col in numeric_columns:
    if col in X_train.columns:
        X_train[col] = pd.to_numeric(X_train[col], errors='coerce')
    if col in X_test.columns:
        X_test[col] = pd.to_numeric(X_test[col], errors='coerce')

# Force leftover object columns to string
for col in X_train.columns:
    if X_train[col].dtype == "object":
        X_train[col] = X_train[col].astype(str)
for col in X_test.columns:
    if X_test[col].dtype == "object":
        X_test[col] = X_test[col].astype(str)

# === DEFINE PIPELINE ===
categorical_cols = X_train.select_dtypes(include="object").columns.tolist()
preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols)
], remainder="passthrough")

model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("xgb", XGBRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=0.5,
        reg_lambda=1,
        random_state=42
    ))
])

# === TRAIN MODEL ===
model.fit(X_train, y_train)

# === PREDICT ===
y_pred = model.predict(X_test)

# === EVALUATE ===
mae = mean_absolute_error(y_true, y_pred)
print(f"✅ MAE after full cleaning: {mae:.4f}")

# === SAVE RESULTS ===
df_test["Predicted HbA1c"] = y_pred
os.makedirs("results", exist_ok=True)
df_test.to_csv("results/Final_DrLim_SyntheticData1000_With_Predictions.csv", index=False)
print("📁 Predictions saved to: results/Final_DrLim_SyntheticData1000_With_Predictions.csv")

# === SAVE MODEL ===
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/final_risk_prediction_model.pkl")
print("✅ Model saved to: models/final_risk_prediction_model.pkl")