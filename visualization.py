import pandas as pd
import seaborn as sns
import statsmodels.api as sm
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib.pyplot as plt
from scipy.stats import f_oneway

# Load dataset
path = "E:/Quanitifying EMG/Summary-motion.csv"
data = pd.read_csv(path)

sorted_decades = sorted(data['Decade'].unique())  # Ensures natural numeric order

# Ensure Decade is treated as a categorical variable in sorted order
data['Decade'] = pd.Categorical(data['Decade'], categories=sorted_decades, ordered=True)

# EDA: Boxplot for Velocity by Age Group
# sns.boxplot(x='Decade', y='Velocity', data=data)
sns.boxplot(x='Decade', y='Position', data=data)
plt.title('Velocity by Age Group')
plt.show()

# ANOVA to compare Velocity across Age Groups
groups = [data[data['Age Group'] == group]['Velocity'] for group in sorted(data['Age Group'].unique())]
f_stat, p_val = f_oneway(*groups)
print(f"F-statistic: {f_stat}, P-value: {p_val}")

# Regression Analysis
import statsmodels.api as sm
X = sm.add_constant(data['Age'])
y = data['Velocity']
model = sm.OLS(y, X).fit()
print(model.summary())

# Perform Tukey's HSD test
tukey = pairwise_tukeyhsd(endog=data['Velocity'],  # Dependent variable
                          groups=data['Decade'],  # Independent categorical variable
                          alpha=0.05)            # Significance level

# Print the results
print(tukey)

# Plot the Tukey HSD results
fig = tukey.plot_simultaneous(comparison_name='60s', figsize=(10, 6))  # Optional comparison baseline
plt.title('Tukey HSD Pairwise Comparisons for Decades')
plt.xlabel('Mean Difference')
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.show()