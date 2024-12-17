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
path = "E:/Quanitifying EMG/Summary-Spinal Loads.csv"
# path = "E:/Quanitifying EMG/Summary-motion.csv"
data = pd.read_csv(path)
variable = 'Compression'
variable = 'AnteriorPosterorShear'
# variable = 'LateralShear'
# sorted_decades = sorted(data['Decade'].unique())  # Ensures natural numeric order

# Ensure Decade is treated as a categorical variable in sorted order
# data['Decade'] = pd.Categorical(data['Decade'], categories=sorted_decades, ordered=True)
# Normalizze by weight
# data[variable] = data[variable]/data['Weight']
# data[variable] = data[variable]/data['BMI']
# controls_data = data[data['Status'] == 'Control']
# Boxplot by Decade and Sex
plt.figure(figsize=(12, 6))
palette = sns.color_palette("ch:s=.25,rot=-.25")
# my_cmap = ListedColormap(palette.as_hex())
sns.barplot(x='Level', y=f'Superior{variable}', hue='Status', data=data, ci="sd", capsize=.4,
            err_kws={"color": "0.4", "linewidth": 1},
            palette=palette,
        )
# sns.boxplot(x='Level', y=f'{variable}', hue='Status', data=data, palette='coolwarm')
# plt.title(f'{variable}')
plt.xlabel('Levels')
plt.ylabel(f'{variable}')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.savefig(f'{variable.lower()}.png', format="png", bbox_inches="tight")
plt.show()
