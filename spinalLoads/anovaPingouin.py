import pandas as pd
import pingouin as pg
path = "E:/Quanitifying EMG/Summary-Spinal Loads.csv"
# Load data
data = pd.read_csv(path)

# Ensure Decade is categorical with natural order
sorted_decades = sorted(data['Decade'].unique())
data['Decade'] = pd.Categorical(data['Decade'], categories=sorted_decades, ordered=True)

# Ensure categorical variables are properly formatted
data['Sex'] = data['Sex'].astype('category')
data['Status'] = data['Status'].astype('category')
# Perform mixed ANOVA
anova_results = pg.mixed_anova(
    data=data,
    dv='SuperiorLateralShear',
    between='Status',
    within='Decade',  
    subject='Subject',
)

print(anova_results)