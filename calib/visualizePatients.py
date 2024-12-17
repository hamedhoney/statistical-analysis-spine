import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
from statsmodels.graphics.factorplots import interaction_plot
import pandas as pd

plt.rc('font', family='serif',size=20)
matplotlib.rc('text', usetex=True)
matplotlib.rc('legend', fontsize=20)
matplotlib.rcParams['text.latex.preamble'] = r'\boldmath'

# Load dataset
path = "E:/Quanitifying EMG/Summary-Moment Matching.csv"
# path = "E:/Quanitifying EMG/Summary-motion.csv"
data = pd.read_csv(path)
data.columns
# Set up variable
variable = 'R2'  # Options: RMSE, AAE, R2 or other metrics

# Normalize if needed
# data[variable] = data[variable]/data['Weight']
# data[variable] = data[variable]/data['BMI']

# Calculate RMSE means and standard deviations by 'Level'
variable_columns = [f'Sagittal {variable}', f'Lateral {variable}', f'Axial {variable}', f'Weighted {variable}']
data_melted = data.melt(id_vars=['Level'], value_vars=variable_columns,
                        var_name=f'{variable} Type', value_name=f'{variable} Value')
data_melted[f'{variable} Type'] = data_melted[f'{variable} Type'].str.replace(f' {variable}', '', regex=False)
# Plot configuration
plt.figure(figsize=(14, 8))
palette = sns.color_palette("ch:s=.25,rot=-.25")[:4]

# Seaborn barplot
sns.barplot(
    x='Level',
    y=f'{variable} Value',
    hue=f'{variable} Type',
    data=data_melted,
    errorbar="sd",
    capsize=0.4,
    err_kws={"color": "0.4", "linewidth": 1},
    palette=palette
)

# Labels and aesthetics
plt.xlabel(r'\textbf{Levels}', fontsize=22)
plt.ylabel(f'\\textbf{{{variable} (Nm)}}', fontsize=22)
plt.legend()
# plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Save and show plot
plt.tight_layout()
plt.savefig(f'{variable.lower()}_barplot.png', format="png", bbox_inches="tight", dpi=300)
plt.show()