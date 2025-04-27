import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Load the dataset (change the file paths as needed)
file_path_1k = 'Final_DrLim_SyntheticData1000.csv'  
file_path_5k = 'Final_DrLim_SyntheticData5000.csv'  

# Load the datasets
df_1k = pd.read_csv(file_path_1k)
df_5k = pd.read_csv(file_path_5k)

# Drop rows with missing values
df_1k_cleaned = df_1k.dropna()
df_5k_cleaned = df_5k.dropna()

# Identify numeric columns for normalization
numeric_columns_1k = df_1k_cleaned.select_dtypes(include=['float64', 'int64']).columns
numeric_columns_5k = df_5k_cleaned.select_dtypes(include=['float64', 'int64']).columns

# Initialize the MinMaxScaler
scaler = MinMaxScaler()

# Normalize the numeric columns for both datasets
df_1k_cleaned[numeric_columns_1k] = scaler.fit_transform(df_1k_cleaned[numeric_columns_1k])
df_5k_cleaned[numeric_columns_5k] = scaler.fit_transform(df_5k_cleaned[numeric_columns_5k])

# Display the cleaned and normalized datasets
import ace_tools as tools
tools.display_dataframe_to_user(name="Normalized Dataset 1k", dataframe=df_1k_cleaned)
tools.display_dataframe_to_user(name="Normalized Dataset 5k", dataframe=df_5k_cleaned)

# Save the cleaned and normalized data to CSV
df_1k_cleaned.to_csv('Normalized_DrLim_Dataset_1000.csv', index=False)
df_5k_cleaned.to_csv('Normalized_DrLim_Dataset_1000.csv', index=False)
