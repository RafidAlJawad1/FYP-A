# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# Load the dataset
df = pd.read_csv("expanded_dr_lim_5000.csv")

# Define the features and target variable
X = df.drop(columns=["HbA1c", "Predicted_HbA1C"])  # Excluding 'HbA1c' and 'Predicted_HbA1C'
y = df["HbA1c"]

# One-hot encoding for categorical features
X = pd.get_dummies(X, columns=["Gender", "Insulin_Regimen", "CKD_Stage"], drop_first=True)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Random Forest Regressor
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Calculate Mean Absolute Error (MAE)
mae = mean_absolute_error(y_test, y_pred)

# Print the MAE
print(f"Mean Absolute Error (MAE): {mae}")
