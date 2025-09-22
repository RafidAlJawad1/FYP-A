import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
import joblib
from groq import Groq

# Load the dataset
df = pd.read_csv('/mnt/data/dv3.csv')

# Create the binary target variable for classification based on HbA1c, FVG, and DDS
df['therapy_effective'] = (
    (df['HbA1c3'] < df['HbA1c1']) &
    (df['FVG3'] < df['FVG1']) &
    (df['DDS3'] < df['DDS1'])
).astype(int)

# --- Temporal Delta & Trend Features ---

df['HbA1c_Delta_1_3'] = df['HbA1c3'] - df['HbA1c1']
df['FVG_Delta_1_3'] = df['FVG3'] - df['FVG1']
df['DDS_Delta_1_3'] = df['DDS3'] - df['DDS1']
df['HbA1c_Trend_2_3'] = df['HbA1c3'] - df['HbA1c2']
df['FVG_Trend_2_3'] = df['FVG3'] - df['FVG2']

# Define the features (X) and target (y) for classification
features = [
    'INSULIN REGIMEN', 'HbA1c1', 'HbA1c2', 'HbA1c3', 'HbA1c_Delta_1_2',
    'Gap from initial visit (days)', 'Gap from first clinical visit (days)',
    'eGFR', 'Reduction (%)', 'FVG1', 'FVG2', 'FVG3', 'FVG_Delta_1_2', 'FVG_Delta_1_3', 'FVG_Trend_2_3',
    'DDS1', 'DDS3', 'DDS_Trend_1_3', 'DDS_Delta_1_3'
]

target = 'therapy_effective'

X = df[features]
y = df[target]

# OneHotEncoding for INSULIN REGIMEN
preprocessor = ColumnTransformer(
    transformers=[('insulin', OneHotEncoder(), ['INSULIN REGIMEN'])],
    remainder='passthrough'  # Leave other columns as is
)

# Train the Random Forest Classifier
rf_model = RandomForestClassifier(n_estimators=200, random_state=42)

# Create a pipeline with preprocessor and model
pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('classifier', rf_model)])

# Train the model
pipeline.fit(X, y)

# Save the trained pipeline (preprocessor + model)
joblib.dump(pipeline, '/mnt/data/therapy_effectiveness_model.pkl')

# Manually select a patient
patient_index = 15
patient = df.iloc[patient_index]

# Prepare the patient's data for prediction
patient_data = {
    'INSULIN REGIMEN': [patient['INSULIN REGIMEN']],
    'HbA1c1': [patient['HbA1c1']],
    'HbA1c2': [patient['HbA1c2']],
    'HbA1c3': [patient['HbA1c3']],
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
    'DDS_Trend_1_3': [patient['DDS_Trend_1_3']],
    'FVG_Delta_1_3': [patient['FVG_Delta_1_3']],
    'HbA1c_Delta_1_3': [patient['HbA1c_Delta_1_3']],
    'HbA1c_Trend_2_3': [patient['HbA1c_Trend_2_3']],
    'FVG_Trend_2_3': [patient['FVG_Trend_2_3']],
    'DDS_Delta_1_3': [patient['DDS_Delta_1_3']]
}

# Convert patient data into a DataFrame for prediction
patient_df = pd.DataFrame(patient_data)

# Make predictions for the specific patient at each visit
predictions = []

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

print(f"Insulin Regimen: {patient['INSULIN REGIMEN']}")

# --- Add Confidence + SHAP Local Explainability ---

import shap

# Transform the full training data for SHAP background (for TreeExplainer)
X_transformed = pipeline.named_steps['preprocessor'].transform(X)

# Create SHAP explainer for the tree-based model (Random Forest)
explainer = shap.Explainer(pipeline.named_steps['classifier'], X_transformed)

# Transform the selected patient's input
patient_transformed = pipeline.named_steps['preprocessor'].transform(patient_df)

# Get SHAP values for the single patient instance (Visit 3)
shap_values_patient = explainer(patient_transformed)

# --- Build a single-class, single-sample SHAP explanation and plot ---
import numpy as np

# Use the positive class (label 1)
clf = pipeline.named_steps['classifier']
pos_idx = int(np.where(clf.classes_ == 1)[0][0])

# Feature names after preprocessing
feature_names = pipeline.named_steps['preprocessor'].get_feature_names_out()

# Ensure the transformed patient row is a 1D dense vector
pt = patient_transformed
if hasattr(pt, "toarray"):
    data_vec = pt.toarray().ravel()
else:
    data_vec = np.array(pt).ravel()

# Slice SHAP outputs for: [sample 0, positive class]
vals = shap_values_patient.values[0][:, pos_idx]          # (n_features,)
base = shap_values_patient.base_values[0][pos_idx]        # scalar

# Build a single-sample Explanation
shap_expl = shap.Explanation(
    values=vals,
    base_values=base,
    data=data_vec,
    feature_names=feature_names
)

shap.initjs()
shap.plots.waterfall(shap_expl, max_display=15)

# --- Groq LLM Integration for Patient-Specific Insights ---

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Prepare input prompt for the LLM
prob_strings = [f"Visit {i+1}: {round(prob * 100, 2)}%" for i, prob in enumerate(predictions)]

# Prepare input prompt for the LLM
prompt = (
    f"The patient is undergoing the insulin regimen: {patient['INSULIN REGIMEN']}.\n"
    f"The predicted therapy effectiveness probabilities over three visits are:\n"
    + "\n".join(prob_strings) +
    "\n\n"
    "Based on these probabilities, provide only the single most important personalized recommendation regarding this patient's therapy effectiveness.\n"
    "Also, briefly justify the therapy effectiveness probabilities by summarizing the trends in the patient's HbA1c, FVG, and DDS scores in simple and concise terms.\n"
    "Use the following patient score values for your analysis:\n"
    f"- HbA1c scores: {patient['HbA1c1']}, {patient['HbA1c2']}, {patient['HbA1c3']}\n"
    f"- FVG scores: {patient['FVG1']}, {patient['FVG2']}, {patient['FVG3']}\n"
    f"- DDS scores: {patient['DDS1']}, {patient['DDS3']}\n"
    "Please keep your entire response under 150 words and focused on clarity and brevity."
)

# Call Groq LLM for insights
llm = client.chat.completions.create(
    model="deepseek-r1-distill-llama-70b",
    messages=[
        {"role": "system", "content": "You are a helpful medical AI assistant."},
        {"role": "user", "content": prompt}
    ]
)

insights_raw = llm.choices[0].message.content

if "<think>" in insights_raw and "</think>" in insights_raw:
    insights = insights_raw.split("</think>", 1)[1].strip()
else:
    insights = insights_raw

print("\n--- Patient-Specific Therapy Insights ---")
print(insights)

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