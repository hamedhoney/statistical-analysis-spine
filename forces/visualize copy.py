import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

path = "E:/Quanitifying EMG/Summary-Muscle Forces.csv"
# Read the data
data = pd.read_csv(path)

# Variable of interest
variable = 'Total'

# Ensure decades are sorted in natural numeric order
sorted_decades = sorted(data['Decade'].unique())

# Treat Decade as an ordered categorical variable
data['Decade'] = pd.Categorical(data['Decade'], categories=sorted_decades, ordered=True)

# Filter for control data
controls_data = data[data['Status'] == 'Control']

# Create figure with increased height to accommodate multiple muscle groups
unique_muscles = controls_data['Muscle'].unique()
plt.figure(figsize=(16, 4 * len(unique_muscles)))

# Create subplot for each muscle
for i, muscle in enumerate(unique_muscles, 1):
    plt.subplot(len(unique_muscles), 1, i)
    
    # Filter data for specific muscle
    muscle_controls = controls_data[controls_data['Muscle'] == muscle]
    
    # Create boxplot
    sns.boxplot(x='Decade', y=variable, hue='Sex', data=muscle_controls, palette='coolwarm')
    
    # Set title to indicate muscle
    plt.title(f'Boxplot of {variable} by Decade and Sex for {muscle}')
    
    # Rotate x-axis labels if needed
    plt.xticks(rotation=45)

# Adjust layout and show plot
plt.tight_layout()
plt.show()