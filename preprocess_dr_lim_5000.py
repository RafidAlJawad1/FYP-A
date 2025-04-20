import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

# Load the dataset
df_expanded = pd.read_csv("DrLim1000Synthetic.csv")

# Expand the dataset to 5000 by duplicating it and adding small random noise for variability
expanded_df = pd.concat([df_expanded] * 5, ignore_index=True)

# Adding small noise to numeric columns for variability
for col in expanded_df.select_dtypes(include=[np.number]).columns:
    expanded_df[col] += np.random.normal(0, 0.01, expanded_df[col].shape)

# Preprocessing: Encode categorical features and standardize numeric ones
categorical_features = ["Gender", "Insulin_Regimen", "CKD_Stage"]
numeric_features = expanded_df.select_dtypes(include=[np.number]).columns.tolist()

# Separate features and target
X_expanded = expanded_df.drop(columns=["HbA1c", "Predicted_HbA1C"])
y_expanded = expanded_df["HbA1c"]

# One-hot encoding for categorical features
X_expanded = pd.get_dummies(X_expanded, columns=categorical_features, drop_first=True)

# Standardize numeric features
scaler = StandardScaler()
X_expanded[X_expanded.select_dtypes(include=[np.number]).columns] = scaler.fit_transform(X_expanded.select_dtypes(include=[np.number]))

# Check the processed data (First few rows)
print(X_expanded.head())
