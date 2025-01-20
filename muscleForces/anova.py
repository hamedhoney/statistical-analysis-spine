import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import matplotlib.pyplot as plt
# Load dataset
path = "E:/Quanitifying EMG/Summary-Spinal Loads.csv"
data = pd.read_csv(path)

sorted_decades = sorted(data['Decade'].unique())  # Ensures natural numeric order

# Ensure Decade is treated as a categorical variable in sorted order
data['Decade'] = pd.Categorical(data['Decade'], categories=sorted_decades, ordered=True)

# Ensure categorical variables are properly formatted
data['Sex'] = data['Sex'].astype('category')
data['Status'] = data['Status'].astype('category')
data['Decade'] = data['Decade'].astype('category')  # Use Decade instead of continuous age

controls_data = data[data['Status'] == 'Control']
female_data = controls_data[controls_data['Sex'] == 'FEMALE']

# Fit a three-way ANOVA model
model = ols('SuperiorResultant ~ C(Decade)', data=data).fit()

# Perform ANOVA
anova_results = anova_lm(model, typ=2)
print(anova_results)

from statsmodels.stats.multicomp import pairwise_tukeyhsd

tukey = pairwise_tukeyhsd(endog=female_data['SuperiorResultant'], groups=female_data['Decade'], alpha=0.05)
print(tukey)
tukey.plot_simultaneous(figsize=(10, 6))
plt.show()