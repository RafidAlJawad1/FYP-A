# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib  

# Load the dataset
df = pd.read_csv("cleaned_expanded_preprocessed_dr_lim_5000.csv")

# Define the features and target variable
X = df.drop(columns=["Target HbA1C"])  # Excluding 'Target HbA1C' for prediction
y = df["Target HbA1C"]

# One-hot encoding for categorical features: GENDER, DM TYPE, CKD Stage
X = pd.get_dummies(X, columns=["GENDER", "DM TYPE", "CKD Stage"], drop_first=True)

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
print(f"Mean Absolute Error: {mae}")

# Save the trained model to a file
joblib.dump(model, 'random_forest_model.joblib')
print("Model saved as 'random_forest_model.joblib'")

# Load the model from the file for later use
loaded_model = joblib.load('random_forest_model.joblib')
print("Model loaded from 'random_forest_model.joblib'")

# Use the loaded model to make predictions on new data (example with X_test)
y_pred_loaded_model = loaded_model.predict(X_test)

# Optionally, calculate the MAE with the loaded model (it should be the same as before)
mae_loaded_model = mean_absolute_error(y_test, y_pred_loaded_model)
print(f"Mean Absolute Error with loaded model: {mae_loaded_model}")
