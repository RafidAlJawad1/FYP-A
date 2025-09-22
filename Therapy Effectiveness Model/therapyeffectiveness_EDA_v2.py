import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv('/mnt/data/dv3.csv')

# Create binary target variable therapy_effective as defined in your model
df['therapy_effective'] = (
    (df['HbA1c3'] < df['HbA1c1']) &
    (df['FVG3'] < df['FVG1']) &
    (df['DDS3'] < df['DDS1'])
).astype(int)

# --- Add Temporal Delta and Trend Features ---
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

# --- Step 1: Overview ---
print(f"Dataset Shape: {df.shape}")
print("\nMissing Values:\n", df.isnull().sum())

print("\nTarget Variable Distribution:\n", df['therapy_effective'].value_counts(normalize=True))

# --- Step 2: Summary Statistics for Numeric Features ---
print("\nSummary Statistics for Selected Features:")
print(df[features].describe())

# --- Step 3: Visualizations ---

plt.figure(figsize=(16, 12))

# Target distribution
plt.subplot(3, 2, 1)
sns.countplot(x='therapy_effective', data=df)
plt.title('Target Variable Distribution (therapy_effective)')
plt.xlabel('Therapy Effective (0=No, 1=Yes)')
plt.ylabel('Count')

# HbA1c scores by therapy effectiveness
plt.subplot(3, 2, 2)
sns.boxplot(x='therapy_effective', y='HbA1c1', data=df)
plt.title('HbA1c1 by Therapy Effectiveness')

plt.subplot(3, 2, 3)
sns.boxplot(x='therapy_effective', y='HbA1c3', data=df)
plt.title('HbA1c3 by Therapy Effectiveness')

# FVG scores by therapy effectiveness
plt.subplot(3, 2, 4)
sns.boxplot(x='therapy_effective', y='FVG1', data=df)
plt.title('FVG1 by Therapy Effectiveness')

plt.subplot(3, 2, 5)
sns.boxplot(x='therapy_effective', y='FVG3', data=df)
plt.title('FVG3 by Therapy Effectiveness')

# DDS scores by therapy effectiveness
plt.subplot(3, 2, 6)
sns.boxplot(x='therapy_effective', y='DDS1', data=df)
plt.title('DDS1 by Therapy Effectiveness')

plt.tight_layout()
plt.show()

# --- Temporal Delta and Trend Features ---

plt.figure(figsize=(16, 10))

# HbA1c Delta 1–3
plt.subplot(2, 2, 1)
sns.boxplot(x='therapy_effective', y='HbA1c_Delta_1_3', data=df)
plt.title("HbA1c Change (Visit 1 → 3) by Therapy Effectiveness")
plt.axhline(0, color='red', linestyle='--')

# FVG Delta 1–3
plt.subplot(2, 2, 2)
sns.boxplot(x='therapy_effective', y='FVG_Delta_1_3', data=df)
plt.title("FVG Change (Visit 1 → 3) by Therapy Effectiveness")
plt.axhline(0, color='red', linestyle='--')

# DDS Delta 1–3
plt.subplot(2, 2, 3)
sns.boxplot(x='therapy_effective', y='DDS_Delta_1_3', data=df)
plt.title("DDS Change (Visit 1 → 3) by Therapy Effectiveness")
plt.axhline(0, color='red', linestyle='--')

# HbA1c Trend Visit 2 → 3
plt.subplot(2, 2, 4)
sns.boxplot(x='therapy_effective', y='HbA1c_Trend_2_3', data=df)
plt.title("HbA1c Trend (Visit 2 → 3) by Therapy Effectiveness")
plt.axhline(0, color='red', linestyle='--')

plt.tight_layout()
plt.show()

# FVG Trend Visit 2 → 3 (new)
plt.figure(figsize=(6, 4))
sns.boxplot(x='therapy_effective', y='FVG_Trend_2_3', data=df)
plt.title("FVG Trend (Visit 2 → 3) by Therapy Effectiveness")
plt.axhline(0, color='red', linestyle='--')
plt.tight_layout()
plt.show()

# --- Step 4: Correlation Matrix of Numeric Features and Target ---

numeric_feats = ['HbA1c1', 'HbA1c2', 'HbA1c3', 'HbA1c_Delta_1_2',
                 'Gap from initial visit (days)', 'Gap from first clinical visit (days)',
                 'eGFR', 'Reduction (%)', 'FVG1', 'FVG2', 'FVG3', 'FVG_Delta_1_2',
                 'DDS1', 'DDS3', 'DDS_Trend_1_3']

corr_matrix = df[numeric_feats + ['therapy_effective']].corr()

plt.figure(figsize=(14, 10))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix of Numeric Features and Target (therapy_effective)')
plt.show()
