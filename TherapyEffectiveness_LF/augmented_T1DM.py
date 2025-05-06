import pandas as pd
import numpy as np

t1dm_file = "Cleaned_and_Normalized_T1DM.xlsx"
t1dm_df = pd.read_excel(t1dm_file)

# Function to augment the dataset
def augment_data(df, target_size):
    # Get the current number of rows
    current_size = len(df)
    
    # Calculate the number of new rows to generate
    new_rows_needed = target_size - current_size
    
    if new_rows_needed <= 0:
        raise ValueError("Target size must be larger than the current dataset size")
    
    # Add noise to numeric columns
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    df_augmented = df.copy()
    
    for col in numeric_cols:
        noise = np.random.normal(0, 0.01, size=(new_rows_needed, len(numeric_cols)))
        noisy_data = df[numeric_cols].sample(new_rows_needed, replace=True).reset_index(drop=True)
        noisy_data += noise
        df_augmented = pd.concat([df_augmented, noisy_data], axis=0)
    
    # Randomly sample from the existing data to fill the required number of rows
    if len(df_augmented) < target_size:
        additional_rows = df.sample(target_size - len(df_augmented), replace=True)
        df_augmented = pd.concat([df_augmented, additional_rows], axis=0)

    return df_augmented

# Augment the data to 1000 and 5000 rows
t1dm_augmented_1000 = augment_data(t1dm_df, 1000)
t1dm_augmented_5000 = augment_data(t1dm_df, 5000)

# Save the augmented datasets
t1dm_augmented_1000.to_excel("Augmented_T1DM_1000.xlsx", index=False)
t1dm_augmented_5000.to_excel("Augmented_T1DM_5000.xlsx", index=False)
