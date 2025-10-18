# Therapy Effectiveness Synthetic Dataset Generator
# Author: Anjanaa Lyan
# Dataset: 500 patients, 3 visits, 30+ clinical fields + binary label
# --------------------------------------------

import numpy as np
import pandas as pd

np.random.seed(42)
n = 500  # number of synthetic patients

# 1. Demographics
patient_ids = np.arange(1001, 1001 + n)
ages = np.random.normal(loc=55, scale=10, size=n).round(1)
sexes = np.random.choice(['M', 'F'], size=n)
ethnicities = np.random.choice(['Malay', 'Chinese', 'Indian', 'Others'], size=n, p=[0.4, 0.3, 0.2, 0.1])

# 2. Anthropometrics
heights_cm = np.random.normal(165, 10, size=n).round(1)
weight1 = np.random.normal(75, 15, size=n).round(1)
weight2 = weight1 - np.random.normal(1.5, 1.0, size=n).round(1)
weight3 = weight2 - np.random.normal(1.0, 0.8, size=n).round(1)
bmi1 = (weight1 / (heights_cm / 100) ** 2).round(1)
bmi3 = (weight3 / (heights_cm / 100) ** 2).round(1)

# 3. Glycemic markers
hba1c1 = np.random.normal(8.5, 1.0, size=n).round(2)
hba1c2 = hba1c1 - np.random.normal(0.3, 0.3, size=n).round(2)
hba1c3 = hba1c2 - np.random.normal(0.4, 0.3, size=n).round(2)

fpg1 = np.random.normal(9.0, 1.2, size=n).round(2)
fpg2 = fpg1 - np.random.normal(0.7, 0.5, size=n).round(2)
fpg3 = fpg2 - np.random.normal(0.6, 0.4, size=n).round(2)

# 4. Renal function
egfr1 = np.random.normal(80, 15, size=n).round(1)
egfr3 = egfr1 + np.random.normal(1.0, 5.0, size=n).round(1)
uacr1 = np.random.normal(25, 10, size=n).round(1)
uacr3 = uacr1 - np.random.normal(2, 5, size=n).round(1)

# 5. Blood pressure
sbp = np.random.normal(130, 15, size=n).round(1)
dbp = np.random.normal(80, 10, size=n).round(1)

# 6. Psychosocial (DDS)
dds1 = np.clip(np.random.normal(3.0, 1.0, size=n), 1.0, 6.0).round(2)
dds3 = np.clip(dds1 - np.random.normal(0.6, 0.5, size=n), 1.0, 6.0).round(2)

# 7. Visit timing
visit1 = pd.to_datetime('2023-01-01') + pd.to_timedelta(np.random.randint(0, 60, size=n), unit='D')
gap_1_2 = np.random.randint(85, 100, size=n)
gap_2_3 = np.random.randint(85, 100, size=n)
visit2 = visit1 + pd.to_timedelta(gap_1_2, unit='D')
visit3 = visit2 + pd.to_timedelta(gap_2_3, unit='D')

# 8. Regimen exposure
regimen_types = ['PBD', 'BB', 'GLP1', 'SGLT2']
regimen1 = np.random.choice(regimen_types, size=n)
regimen2 = np.random.choice(regimen_types, size=n)
regimen3 = np.random.choice(regimen_types, size=n)

# 9. Label: therapy effective if HbA1c drop ≥0.5%, FPG drop ≥1.0 mmol/L, and DDS improved
therapy_effective = ((hba1c3 <= hba1c1 - 0.5) & (fpg3 <= fpg1 - 1.0) & (dds3 < dds1)).astype(int)

# 10. Assemble DataFrame
df = pd.DataFrame({
    'Patient_ID': patient_ids,
    'Age': ages,
    'Sex': sexes,
    'Ethnicity': ethnicities,
    'Height_cm': heights_cm,
    'Weight1': weight1,
    'Weight2': weight2,
    'Weight3': weight3,
    'BMI1': bmi1,
    'BMI3': bmi3,
    'HbA1c1': hba1c1,
    'HbA1c2': hba1c2,
    'HbA1c3': hba1c3,
    'FPG1': fpg1,
    'FPG2': fpg2,
    'FPG3': fpg3,
    'eGFR1': egfr1,
    'eGFR3': egfr3,
    'UACR1': uacr1,
    'UACR3': uacr3,
    'SBP': sbp,
    'DBP': dbp,
    'DDS1': dds1,
    'DDS3': dds3,
    'VisitDate1': visit1,
    'VisitDate2': visit2,
    'VisitDate3': visit3,
    'Gap_1_2_days': gap_1_2,
    'Gap_2_3_days': gap_2_3,
    'Regimen1': regimen1,
    'Regimen2': regimen2,
    'Regimen3': regimen3,
    'Therapy_Effective': therapy_effective
})

# 11. Save to CSV
df.to_csv("therapy_effectiveness_synthetic.csv", index=False)
print("Dataset saved as therapy_effectiveness_synthetic.csv")
