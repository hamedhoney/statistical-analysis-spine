import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.graphics.factorplots import interaction_plot
import pandas as pd
# Load dataset
path = "E:/Quanitifying EMG/Summary-Muscle Forces.csv"
# path = "E:/Quanitifying EMG/Summary-motion.csv"
data = pd.read_csv(path)
variable = 'Total'
sorted_decades = sorted(data['Decade'].unique())  # Ensures natural numeric order
data.columns
# Ensure Decade is treated as a categorical variable in sorted order
data['Decade'] = pd.Categorical(data['Decade'], categories=sorted_decades, ordered=True)
# Normalizze by weight
# data[variable] = data[variable]/data['Weight']
# data[variable] = data[variable]/data['BMI']
controls_data = data[data['Status'] == 'Control']
# Filter data for specific muscle
muscle = 'LeftErectorSpinae'
muscle_controls = controls_data[controls_data['Muscle'] == muscle]

# Create boxplot
sns.boxplot(x='Decade', y=variable, hue='Sex', data=muscle_controls, palette='coolwarm')

# Set title to indicate muscle
plt.title(f'Boxplot of {variable} by Decade and Sex for {muscle}')

# Rotate x-axis labels if needed
plt.xticks(rotation=45)

# Boxplot by Decade and Sex
plt.figure(figsize=(12, 6))
sns.boxplot(x='Decade', y=f'{variable}', hue='Sex', data=controls_data, palette='coolwarm')
plt.title(f'{variable} by Decade and Sex')
plt.xlabel('Decade')
plt.ylabel(f'{variable}')
plt.legend(title='Sex')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
