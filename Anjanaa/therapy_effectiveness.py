import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
import joblib  # for saving the model

# Load the dataset
df = pd.read_csv('/mnt/data/dv3.csv')  

# Create the binary target variable for classification based on HbA1c, FVG, and DDS
df['therapy_effective'] = (
    (df['HbA1c3'] < df['HbA1c1']) &   
    (df['FVG3'] < df['FVG1']) &        
    (df['DDS3'] < df['DDS1'])          
).astype(int)  # 1 if therapy is effective, 0 otherwise

# Define the features (X) and target (y) for classification
features = [
    'INSULIN REGIMEN', 'HbA1c1', 'HbA1c2', 'HbA1c3', 'HbA1c_Delta_1_2', 
    'Gap from initial visit (days)', 'Gap from first clinical visit (days)', 
    'eGFR', 'Reduction (%)', 'FVG1', 'FVG2', 'FVG3', 'FVG_Delta_1_2',
    'DDS1', 'DDS3', 'DDS_Trend_1_3'
]

target = 'therapy_effective'

X = df[features]
y = df[target]

# OneHotEncoding for INSULIN REGIMEN
preprocessor = ColumnTransformer(
    transformers=[('insulin', OneHotEncoder(), ['INSULIN REGIMEN'])],  
    remainder='passthrough'  
)

# Train the Random Forest Classifier
rf_model = RandomForestClassifier(n_estimators=200, random_state=42)

# Create a pipeline with preprocessor and model
pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('classifier', rf_model)])

# Train the model
pipeline.fit(X, y)

# Save the trained pipeline (preprocessor + model)
joblib.dump(pipeline, 'therapy_effectiveness_model.pkl')

# Manually select a patient 
patient_index = 15  # Example patient index
patient = df.iloc[patient_index] 

# Prepare the patient's data for prediction
patient_data = {
    'INSULIN REGIMEN': [patient['INSULIN REGIMEN']],  
    'HbA1c1': [patient['HbA1c1']],  # Patient's HbA1c at visit 1
    'HbA1c2': [patient['HbA1c2']],  # Patient's HbA1c at visit 2
    'HbA1c3': [patient['HbA1c3']],  # Patient's HbA1c at visit 3
    'HbA1c_Delta_1_2': [patient['HbA1c_Delta_1_2']],
    'Gap from initial visit (days)': [patient['Gap from initial visit (days)']],
    'Gap from first clinical visit (days)': [patient['Gap from first clinical visit (days)']],
    'eGFR': [patient['eGFR']],
    'Reduction (%)': [patient['Reduction (%)']],
    'FVG1': [patient['FVG1']],
    'FVG2': [patient['FVG2']],
    'FVG3': [patient['FVG3']],
    'FVG_Delta_1_2': [patient['FVG_Delta_1_2']],
    'DDS1': [patient['DDS1']],
    'DDS3': [patient['DDS3']],
    'DDS_Trend_1_3': [patient['DDS_Trend_1_3']]
}

# Convert patient data into a DataFrame for prediction
patient_df = pd.DataFrame(patient_data)

# Make predictions for the specific patient at each visit
predictions = []
insulin_regimen = patient['INSULIN REGIMEN']  

# Visit 1
patient_df['HbA1c1'] = [patient['HbA1c1']]  
predictions.append(pipeline.predict_proba(patient_df)[:, 1][0])

# Visit 2
patient_df['HbA1c1'] = [patient['HbA1c2']]  
predictions.append(pipeline.predict_proba(patient_df)[:, 1][0])

# Visit 3
patient_df['HbA1c1'] = [patient['HbA1c3']]  
predictions.append(pipeline.predict_proba(patient_df)[:, 1][0])

# Output effectiveness as percentage for each visit and insulin regimen
for i, prob in enumerate(predictions):
    effectiveness_percentage = round(prob * 100, 2)
    effectiveness_status = "Effective" if prob >= 0.5 else "Ineffective"
    print(f"Visit {i+1}: {effectiveness_status} ({effectiveness_percentage}% probability)")

print(f"Insulin Regimen: {insulin_regimen}")  

# Generate Therapy Pathline (visualize the predictions over time)
time_points = ['Visit 1', 'Visit 2', 'Visit 3']

# Plot the therapy pathline
plt.figure(figsize=(8, 6))
plt.plot(time_points, predictions, marker='o', linestyle='-', color='b')
plt.title(f'Therapy Effectiveness Pathline for Patient {patient_index}')
plt.xlabel('Time (Visits)')
plt.ylabel('Probability of Therapy Effectiveness')
plt.grid(True)
plt.show()
