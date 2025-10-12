# Therapy Effectiveness Model – Preprocessing and Classifier Pipeline
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
import shap

# Load dataset
df = pd.read_csv("therapy_effectiveness_synthetic.csv")
df.head()

# Drop IDs and visit dates 
df_model = df.drop(columns=['Patient_ID', 'VisitDate1', 'VisitDate2', 'VisitDate3'])

# Define X and y
X = df_model.drop(columns=['Therapy_Effective'])
y = df_model['Therapy_Effective']

# Identify column types
num_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
cat_cols = X.select_dtypes(include=['object']).columns.tolist()

print("Numerical columns:", num_cols)
print("Categorical columns:", cat_cols)

# Preprocessing steps
numeric_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder(drop='first', handle_unknown='ignore'))
])

# Full preprocessor
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, num_cols),
        ('cat', categorical_transformer, cat_cols)
    ]
)

# Model pipeline using Random Forest
model_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# Train model
model_pipeline.fit(X_train, y_train)

# Predict and evaluate
y_pred = model_pipeline.predict(X_test)
y_prob = model_pipeline.predict_proba(X_test)[:, 1]

# Output performance
print("✅ Classification Report:\n", classification_report(y_test, y_pred))
print("📊 Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("📈 ROC AUC Score:", roc_auc_score(y_test, y_prob))

# Rebuild preprocessed + encoded training data
preprocessor = model_pipeline.named_steps['preprocessor']
model = model_pipeline.named_steps['classifier']

# Extract fitted preprocessor and model
preprocessor = model_pipeline.named_steps['preprocessor']
model = model_pipeline.named_steps['classifier']

# Transform X_test using the fitted preprocessor
X_test_enc = preprocessor.transform(X_test)
feature_names = preprocessor.get_feature_names_out()

# Convert to DataFrame
import scipy.sparse
if isinstance(X_test_enc, scipy.sparse.spmatrix):
    X_test_enc = X_test_enc.toarray()
X_test_df = pd.DataFrame(X_test_enc, columns=feature_names)

# Use TreeExplainer for tree models (RF, XGB)
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test_df)

# If classifier → shap_values is a list (one per class), take class 1
if isinstance(shap_values, list):
    shap.summary_plot(shap_values[1], X_test_df, feature_names=feature_names, max_display=15)
else:
    shap.summary_plot(shap_values, X_test_df, feature_names=feature_names, max_display=15)
