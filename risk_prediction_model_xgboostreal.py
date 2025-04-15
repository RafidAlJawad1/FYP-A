import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error

# Load cleaned dataset
df = pd.read_csv("DrLim1000Synthetic.csv")

# Separate input features and target
X = df.drop(columns=["Target_HbA1C", "Predicted_HbA1C"])
y = df["Target_HbA1C"]

# Ensure all object columns are strings
categorical_cols = X.select_dtypes(include=["object"]).columns.tolist()
for col in categorical_cols:
    X[col] = X[col].astype(str)

# Build pipeline
preprocessor = ColumnTransformer(
    transformers=[('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)],
    remainder='passthrough'
)

model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('xgb', XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42))
])

# Split and train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)

print(f"✅ MAE: {mae:.4f}")
