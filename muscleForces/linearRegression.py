import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Load dataset
path = "E:/Quanitifying EMG/Summary-motion.csv"
data = pd.read_csv(path)

sorted_decades = sorted(data['Decade'].unique())  # Ensures natural numeric order

# Ensure Decade is treated as a categorical variable in sorted order
data['Decade'] = pd.Categorical(data['Decade'], categories=sorted_decades, ordered=True)

# Fit a linear regression model with interaction terms
model = smf.ols('Velocity ~ Age * Sex * Status', data=data).fit()

# Summary of the model
print(model.summary())

# Perform Tukey HSD for Age Group
tukey = pairwise_tukeyhsd(endog=data['Velocity'], groups=data['Age Group'], alpha=0.05)
print(tukey)
tukey.plot_simultaneous()
