import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from xgboost import XGBRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Load your dataset
df = pd.read_csv("NCD_Risk_Prediction_Synthetic.csv")
X = df.drop(columns=["future_hba1c"])
y = df["future_hba1c"]

results = []
random_states = [1, 7, 13, 21, 33, 42, 66, 77, 88, 99]

for rs in random_states:
    X_train_df, X_test_df, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=rs)
    X_train = X_train_df.drop(columns=["patient_id"])
    X_test = X_test_df.drop(columns=["patient_id"])

    cat_cols = X_train.select_dtypes(include=["object"]).columns.tolist()
    if "patient_id" in cat_cols:
        cat_cols.remove("patient_id")

    preprocessor = ColumnTransformer([
        ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols)
    ], remainder='passthrough')

    model = Pipeline(steps=[
        ('prep', preprocessor),
        ('xgb', XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=rs))
    ])

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)

    results.append({"random_state": rs, "mae": round(mae, 4)})
    print(f"Random State {rs} → MAE: {mae:.4f}")

# Save to CSV
results_df = pd.DataFrame(results)
results_df.to_csv("MAE_by_RandomState.csv", index=False)
print("\n✅ Saved results to MAE_by_RandomState.csv")

# Plot the results
plt.figure(figsize=(10, 5))
plt.plot(results_df["random_state"], results_df["mae"], marker='o', linestyle='-', color='blue')
plt.title("MAE vs Random State")
plt.xlabel("Random State")
plt.ylabel("Mean Absolute Error (MAE)")
plt.grid(True)
plt.xticks(results_df["random_state"])
plt.tight_layout()
plt.savefig("MAE_vs_RandomState_Plot.png")
plt.show()
print("📈 Plot saved as MAE_vs_RandomState_Plot.png")
