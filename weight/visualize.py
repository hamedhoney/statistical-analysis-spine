import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.graphics.factorplots import interaction_plot
import pandas as pd
# Load dataset
path = "E:/Quanitifying EMG/Summary-Spinal Loads.csv"
# path = "E:/Quanitifying EMG/Summary-motion.csv"
data = pd.read_csv(path)
variable = 'Weight'
sorted_decades = sorted(data['Decade'].unique())  # Ensures natural numeric order

# Ensure Decade is treated as a categorical variable in sorted order
data['Decade'] = pd.Categorical(data['Decade'], categories=sorted_decades, ordered=True)
# Normalizze by weight
# data[variable] = data[variable]/data['Weight']
controls_data = data[data['Status'] == 'Control']
# Boxplot by Decade and Sex
plt.figure(figsize=(12, 6))
sns.boxplot(x='Decade', y=f'{variable}', hue='Sex', data=controls_data, palette='coolwarm')
plt.title(f'{variable} by Decade and Sex')
plt.xlabel('Decade')
plt.ylabel(f'{variable}')
plt.legend(title='Sex')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
