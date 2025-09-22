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

# Define features used in your therapy effectiveness model
features = [
    'INSULIN REGIMEN', 'HbA1c1', 'HbA1c2', 'HbA1c3', 'HbA1c_Delta_1_2',
    'Gap from initial visit (days)', 'Gap from first clinical visit (days)',
    'eGFR', 'Reduction (%)', 'FVG1', 'FVG2', 'FVG3', 'FVG_Delta_1_2',
    'DDS1', 'DDS3', 'DDS_Trend_1_3'
]

# --- Overview ---
print(f"Dataset Shape: {df.shape}")
print("\nMissing Values:\n", df.isnull().sum())

print("\nTarget Variable Distribution:\n", df['therapy_effective'].value_counts(normalize=True))

# --- Summary Statistics for Numeric Features ---
print("\nSummary Statistics for Selected Features:")
print(df[features].describe())

# --- Visualizations ---

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

# --- Correlation Matrix of Numeric Features and Target ---

numeric_feats = ['HbA1c1', 'HbA1c2', 'HbA1c3', 'HbA1c_Delta_1_2',
                 'Gap from initial visit (days)', 'Gap from first clinical visit (days)',
                 'eGFR', 'Reduction (%)', 'FVG1', 'FVG2', 'FVG3', 'FVG_Delta_1_2',
                 'DDS1', 'DDS3', 'DDS_Trend_1_3']

corr_matrix = df[numeric_feats + ['therapy_effective']].corr()

plt.figure(figsize=(14, 10))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix of Numeric Features and Target (therapy_effective)')
plt.show()
