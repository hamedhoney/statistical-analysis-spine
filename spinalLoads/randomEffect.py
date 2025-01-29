import pandas as pd
from statsmodels.regression.mixed_linear_model import MixedLM
from statsmodels.stats.anova import anova_lm, AnovaRM
from statsmodels.regression.mixed_linear_model import MixedLMResults
from statsmodels.formula.api import ols
from statsmodels.formula.api import mixedlm
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib.pyplot as plt

path = "E:/Quanitifying EMG/Summary-Spinal Loads.csv"
# Load data
data = pd.read_csv(path)

# Ensure Decade is categorical with natural order
sorted_decades = sorted(data['Decade'].unique())
data['Decade'] = pd.Categorical(data['Decade'], categories=sorted_decades, ordered=True)

# Ensure categorical variables are properly formatted
data['Sex'] = data['Sex'].astype('category')
data['Status'] = data['Status'].astype('category')
model = mixedlm('SuperiorResultant ~ C(Decade)+C(Sex)+C(Status)', data, groups=data['Subject']).fit()
print(model.summary())
print(model.cov_re)
# Fit a mixed-effects model with Subject as a random effect
mixed_model = MixedLM.from_formula(
    'SuperiorLateralShear ~ C(Decade) + C(Status) + C(Sex) +C(Decade)*C(Status) + C(Status)*C(Sex) + C(Decade)*C(Sex)',
    groups=data['Subject'],
    data=data,
).fit()
print(mixed_model.summary())

# Extract random effect variance
# random_effect_variance = model.cov_re.iloc[0, 0]
# print(f"Random Effect Variance: {random_effect_variance:.4f}")

# # Confidence intervals for random effects
# print(model.random_effects)  # Random effects for each group
# # Perform ANOVA
# my_model_fit = AnovaRM(data, 'SuperiorResultant', 'Subject', within=['Decade', 'Status'], aggregate_func='mean').fit()
# print(my_model_fit.anova_table)

# # Subset for Tukey's HSD
# controls_data = data[data['Status'] == 'Control']
# female_data = controls_data[controls_data['Sex'] == 'FEMALE']

# # Perform Tukey's HSD
# tukey = pairwise_tukeyhsd(endog=female_data['SuperiorResultant'], 
#                           groups=female_data['Decade'], alpha=0.05)
# print(tukey)
# tukey.plot_simultaneous(figsize=(10, 6))
# plt.title("Tukey's HSD: Superior Resultant Across Decades (Females)")
# plt.grid()
# plt.show()
