import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

# Step 1: Load the dataset
df = pd.read_csv("Anomymised_CT_DR_LIM(CONTROL).csv")

# Step 2: Clean the dataset by renaming columns and dropping unnecessary ones
df_cleaned = df.rename(columns={
    ' ': 'ID',
    'AW': 'Status',
    'BASELINE (RECRUITMENT)': 'Recruitment Date',
    'Unnamed: 3': 'AGE',
    'Unnamed: 4': 'GENDER',
    'Unnamed: 5': 'RACE',
    'Unnamed: 6': 'DURATION DM',
    'Unnamed: 7': 'DM TYPE',
    'INSULIN REGIMEN': 'Insulin Regimen',
    'DDS': 'DDS_1st',
    'Unnamed: 16': 'Freq SMBG',
    'Unnamed: 17': 'Freq Hypo',
    'Unnamed: 18': 'Freq Visits',
    'Unnamed: 22': 'Reduction (%)',
    'Unnamed: 23': 'eGFR',
    'Unnamed: 24': 'CKD Stage',
    'Unnamed: 25': 'Target HbA1C'
})

# Drop unnecessary or unnamed columns
df_cleaned = df_cleaned.drop(columns=[col for col in df_cleaned.columns if 'Unnamed' in col or ' ' in col])

# Step 3: Convert columns to appropriate data types
df_cleaned['AGE'] = pd.to_numeric(df_cleaned['AGE'], errors='coerce')
df_cleaned['Freq SMBG'] = pd.to_numeric(df_cleaned['Freq SMBG'], errors='coerce')
df_cleaned['Freq Hypo'] = pd.to_numeric(df_cleaned['Freq Hypo'], errors='coerce')
df_cleaned['Freq Visits'] = pd.to_numeric(df_cleaned['Freq Visits'], errors='coerce')
df_cleaned['eGFR'] = pd.to_numeric(df_cleaned['eGFR'], errors='coerce')
df_cleaned['Target HbA1C'] = pd.to_numeric(df_cleaned['Target HbA1C'], errors='coerce')

# Step 4: Clean non-numeric characters from the dataset
df_cleaned = df_cleaned.replace(r'[^\d.]', '', regex=True)

# Step 5: Convert all values to numeric, coercing errors to NaN
df_cleaned = df_cleaned.apply(pd.to_numeric, errors='coerce')

# Step 6: Fill missing values in numeric columns with the median
df_cleaned.fillna(df_cleaned.median(), inplace=True)

# Step 7: Expand the dataset to 5000 by duplicating it and adding small random noise for variability
expanded_df = pd.concat([df_cleaned] * 5, ignore_index=True)

# Add small noise to numeric columns for variability
for col in expanded_df.select_dtypes(include=[np.number]).columns:
    expanded_df[col] += np.random.normal(0, 0.01, expanded_df[col].shape)

# Step 8: Preprocess the data - One-hot encode categorical features and standardize numeric ones
categorical_features = ["GENDER", "DM TYPE", "CKD Stage"]
numeric_features = expanded_df.select_dtypes(include=[np.number]).columns.tolist()

# Separate features and target
X_expanded = expanded_df.drop(columns=["Target HbA1C"])
y_expanded = expanded_df["Target HbA1C"]

# One-hot encoding for categorical features
X_expanded = pd.get_dummies(X_expanded, columns=categorical_features, drop_first=True)

# Standardize numeric features
scaler = StandardScaler()
X_expanded[X_expanded.select_dtypes(include=[np.number]).columns] = scaler.fit_transform(X_expanded.select_dtypes(include=[np.number]))

# Step 9: Save the preprocessed expanded dataset
expanded_file_path = "expanded_preprocessed_dr_lim_5000.csv"
expanded_df.to_csv(expanded_file_path, index=False)

# Step 10: Output the path to the preprocessed dataset
expanded_file_path
