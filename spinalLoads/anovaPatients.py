import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import numpy as np
from statsmodels.stats.weightstats import ttest_ind
import matplotlib.pyplot as plt
# Load dataset
path = "E:/Quanitifying EMG/Summary-Spinal Loads.csv"
data = pd.read_csv(path)

# Ensure categorical variables are properly formatted
data['Sex'] = data['Sex'].astype('category')
data['Status'] = data['Status'].astype('category')
data['Decade'] = data['Decade'].astype('category')  # Use Decade instead of continuous age

# controls_data = data[data['Status'] == 'Control']
# female_data = controls_data[controls_data['Sex'] == 'FEMALE']

# Fit a three-way ANOVA model
model = ols('SuperiorResultant ~ C(Status) + C(Sex) + C(Status)*C(Sex)', data=data).fit()

# Perform ANOVA
anova_results = anova_lm(model, typ=2)
print(anova_results)

from statsmodels.stats.multicomp import pairwise_tukeyhsd

# tukey = pairwise_tukeyhsd(endog=data['SuperiorResultant'], groups=data['Status'], alpha=0.05)
# print(tukey)
# tukey.plot_simultaneous(figsize=(10, 6))
# plt.show()

controls_data = data[data['Status'] == 'Control']
patient_data = data[data['Status'] == 'Patient']
# Perform t-test
t_stat, p_value, df = ttest_ind(controls_data, patient_data, usevar='pooled')  # Use 'pooled' for equal variance
print(f"T-statistic: {t_stat}, P-value: {p_value}, Degrees of Freedom: {df}")
