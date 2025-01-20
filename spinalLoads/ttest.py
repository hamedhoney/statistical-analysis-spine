import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.weightstats import ttest_ind

# Example dataset
# Load dataset
path = "E:/Quanitifying EMG/Summary-Spinal Loads.csv"
# path = "E:/Quanitifying EMG/Summary-motion.csv"
data = pd.read_csv(path)
variable = 'SuperiorCompression'
# Split data into groups
controls_data = data[data['Status'] == 'Control'][variable]
patient_data = data[data['Status'] == 'Low Back Pain Patient'][variable]

# Perform t-test
t_stat, p_value, df = ttest_ind(controls_data, patient_data, usevar='pooled')
print(f"T-statistic: {t_stat}, P-value: {p_value}, Degrees of Freedom: {df}")

# Plot data
plt.figure(figsize=(8, 5))
sns.boxplot(data=data, x='Status', y=variable, palette='Set2')
sns.swarmplot(data=data, x='Status', y=variable, color='black', alpha=0.7)

# Add mean and standard deviation
control_mean, patient_mean = controls_data.mean(), patient_data.mean()
plt.axhline(y=control_mean, color='blue', linestyle='--', label=f'Control Mean: {control_mean:.2f}')
plt.axhline(y=patient_mean, color='red', linestyle='--', label=f'Patient Mean: {patient_mean:.2f}')

# Add annotations for p-value
plt.title(f"T-Test Results: P-value = {p_value:.3f}", fontsize=14)
plt.legend()
plt.tight_layout()
plt.show()
