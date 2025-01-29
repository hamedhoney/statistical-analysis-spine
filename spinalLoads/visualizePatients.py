import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
from statsmodels.graphics.factorplots import interaction_plot
import pandas as pd
import numpy as np

plt.rc('font', family='serif',size=20)
matplotlib.rc('text', usetex=True)
matplotlib.rc('legend', fontsize=20)
# matplotlib.rcParams['text.latex.preamble'] = r'\boldmath'
output_path = "D:/Dissetation/overleaf/dissertation/pics"

def plot(data, variable, hue):
    plt.figure(figsize=(16, 9))
    palette = sns.color_palette("Blues", 2)
    # my_cmap = ListedColormap(palette.as_hex())
    sns.barplot(
        data=data, 
        x='Sex', 
        y=f'Superior{variable}', 
        hue=hue, 
        errorbar="ci", capsize=.4,
        err_kws={"color": "0.2", "linewidth": 1},
        palette=palette,
    )
    variable = variable.replace('AnteriorPosterorShear', 'AP Shear')
    variable = variable.replace('LateralShear', 'Lateral Shear')
    plt.xlabel(r'\textbf{Levels}', fontsize=22)
    plt.ylabel(f'\\textbf{{{variable} (N)}}', fontsize=22)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    variable = variable.replace(' ', '')
    plt.savefig(f'{variable.lower()}by{hue}.png', format="png", bbox_inches="tight")
    plt.show()

def plotMoment(data, variable, hue):
    plt.figure(figsize=(16, 9))
    palette = sns.color_palette("Blues", 6)
    # my_cmap = ListedColormap(palette.as_hex())
    sns.barplot(x='Level', y=f'{variable}', hue=hue, data=data, errorbar="ci", capsize=.4,
                err_kws={"color": "0.2", "linewidth": 1},
                palette=palette,
            )
    # plt.xlabel(r'\textbf{Decade}', fontsize=22)
    # plt.xlabel(r'\textbf{Plane}', fontsize=22)
    # plt.ylabel(r'\textbf{Normalized Moment ($\frac{Nm}{\mathrm{kg/m}^2}$)}', fontsize=22)
    # plt.ylabel(f'\\textbf{{Moment (Nm)}}', fontsize=22)
    plt.legend(fontsize=16)#, loc="upper left", bbox_to_anchor=(1, 1))
    plt.xlabel(r'\textbf{Levels}', fontsize=22)
    plt.ylabel(f'\\textbf{{{variable} (Nm)}}', fontsize=22)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    variable = variable.replace(' ', '')
    plt.savefig(f'{output_path}/{variable.lower()}by{hue}.png', format="png", bbox_inches="tight")
    plt.show()

# Load dataset
path = "E:/Quanitifying EMG/Summary-Spinal Loads.csv"
# path = "E:/Quanitifying EMG/Summary-motion.csv"
data = pd.read_csv(path)
variable = 'Resultant'
# variable = 'Compression'
# variable = 'AnteriorPosterorShear'
# variable = 'LateralShear'
sorted_decades = sorted(data['Decade'].unique())  # Ensures natural numeric order
data['Status'] = data['Status'].replace('Control', 'Asymptomatic')
# Ensure Decade is treated as a categorical variable in sorted order
data['Decade'] = pd.Categorical(data['Decade'], categories=sorted_decades, ordered=True)
# Normalizze by weight
# data[variable] = data[variable]/data['Weight']
data[f"Superior{variable}"] = data[f"Superior{variable}"]/data['BMI']
# controls_data = data[data['Status'] == 'Control']
plot(data, variable, 'Decade')

# path = "E:/Quanitifying EMG/Summary-Muscle Moments.csv"
# data = pd.read_csv(path)
# sorted_decades = sorted(data['Decade'].unique())
# data['Decade'] = pd.Categorical(data['Decade'], categories=sorted_decades, ordered=True)
# variable_columns = [f'Sagittal', f'Lateral', f'Axial', f'Magnitude']
# data['Magnitude'] = list(np.linalg.norm((data['Sagittal'], data['Lateral'], data['Axial']), axis=0))
# variable = 'Sagittal'
# # variable = 'Lateral'
# variable = 'Axial'
# variable = 'Magnitude'
# for v in variable_columns:
#     data[f'{v}'] = data[f'{v}']/data['BMI']
# data.to_csv("E:/Quanitifying EMG/Summary-Muscle-bmi-Normalized-Moments.csv", index=False)
# data_melted = data.melt(id_vars=['Decade'], value_vars=variable_columns,
#                         var_name='Type', value_name='Value')
# data_melted['Type'] = data_melted['Type'].str.replace(f'', '', regex=False)
# data = data[data['Trial Weighted'] == True]
# Plot configuration
# plotMoment(data, variable, 'Decade')
