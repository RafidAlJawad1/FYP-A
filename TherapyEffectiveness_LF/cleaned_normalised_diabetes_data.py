import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Load the original datasets
t1dm_file = "Shanghai_T1DM_Summary.xlsx"
t2dm_file = "Shanghai_T2DM_Summary.xlsx"

# Read the datasets
t1dm_df = pd.read_excel(t1dm_file, sheet_name='T1DM')
t2dm_df = pd.read_excel(t2dm_file, sheet_name='T2DM')

# Function to clean and normalize data
def clean_and_normalize(df):
    # Drop rows with missing values (do not remove columns)
    df_cleaned = df.dropna()

    # Identify numeric columns
    numeric_cols = df_cleaned.select_dtypes(include=['float64', 'int64']).columns

    # Normalize numeric columns using Min-Max scaling
    scaler = MinMaxScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df_cleaned[numeric_cols]), columns=numeric_cols)

    # Combine back the non-numeric columns with the normalized ones
    df_final = pd.concat([df_cleaned.drop(columns=numeric_cols), df_scaled], axis=1)
    return df_final

# Apply the cleaning and normalization
t1dm_cleaned = clean_and_normalize(t1dm_df)
t2dm_cleaned = clean_and_normalize(t2dm_df)

# Save the cleaned datasets to new files
t1dm_cleaned.to_excel("Cleaned_and_Normalized_T1DM.xlsx", index=False)
t2dm_cleaned.to_excel("Cleaned_and_Normalized_T2DM.xlsx", index=False)
