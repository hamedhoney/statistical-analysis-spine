import statsmodels.api as sm
import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.genmod.bayes_mixed_glm as glmm
from sklearn.preprocessing import StandardScaler
from statsmodels.stats.outliers_influence import variance_inflation_factor

path = 'S:/SRI/SRI_Research/Protocols (1 - Current)/2021 - Mechanistic Model Validation/2024-09 Mechmodel v1.0.0-pre.61/Summary-Spinal Loads.xlsx'
data = pd.read_excel(path, sheet_name='Summary-Spinal Loads')
data['Age'] = data['Age'].astype(str)
data['Subject'] = data['Subject'].astype(str)
# drop 2022MFORCE
data = data[data.Project=='2023LBPEMG']
nSubjects = data.Subject.unique().size
def calculate_vif(df):
    vif_data = pd.DataFrame()
    vif_data["feature"] = df.columns
    vif_data["VIF"] = [variance_inflation_factor(df.values, i) for i in range(len(df.columns))]
    return vif_data


model = smf.mixedlm(
    "SuperiorResultant ~ C(Sex) * C(Status)", 
    data, 
    groups=data["Subject"],
    # family=sm.families.Poisson(),
)

result = model.fit()
print(result.summary())

fixed_effects = data[['Sex', 'Age', 'Status']]

# Define the response variable (dependent variable, assuming count data)
y = data['SuperiorResultant']  # Replace with your actual dependent variable

# Random effects design (subject-specific random effects)
# Here we assume 'subject_id' represents the random effect grouping
random_effects = pd.get_dummies(data['Subject'], drop_first=True)


model = glmm.PoissonBayesMixedGLM(
    y,
    fixed_effects,
    random_effects,
    vcp_p=1,
    ident=[1] * (nSubjects-1)
)

result = model.fit_vb()
print(result.summary())