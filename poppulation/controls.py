import pandas as pd

# Load the uploaded file to understand its structure and contents

import matplotlib.pyplot as plt
import seaborn as sns

path = "E:/Quanitifying EMG/demog.tsv"
data = pd.read_csv(path, sep='\t')
# Filter data for females in the 'Control' series
female_control_data = data[(data['Birth Sex'] == 'FEMALE') & (data['Series'] == 'Control')]
female_control_data['Age Decade'] = (female_control_data['Age at Creation'] // 10) * 10
# Display the first few rows and column information to assess the data structure
data_info = {
    "head": data.head(),
    "columns": data.columns.tolist(),
    "dtypes": data.dtypes.to_dict(),
    "summary": data.describe(include='all').transpose()
}
data_info
# Set a style for the plots
sns.set_theme(style="whitegrid")

continuous_vars = ['Height', 'Weight', 'BMI', 'Age Decade']
# Distribution plots for continuous variables within the filtered data
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
for ax, var in zip(axes.flat, continuous_vars):
    sns.histplot(female_control_data[var], kde=True, ax=ax, bins=10, color="orchid")
    ax.set_title(f"Distribution of {var}")
    ax.set_xlabel(var)
    ax.set_ylabel("Frequency")

plt.tight_layout()
plt.show()

# Relationships for filtered data: Height vs Weight, BMI vs Age
scatter_pairs = [('Age Decade', 'Height'), ('Age Decade', 'BMI')]
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
for ax, (x, y) in zip(axes, scatter_pairs):
    sns.scatterplot(data=female_control_data, x=x, y=y, ax=ax, color="blue")
    ax.set_title(f"{y} vs {x} (Female Controls)")
    ax.set_xlabel(x)
    ax.set_ylabel(y)

plt.tight_layout()
plt.show()
