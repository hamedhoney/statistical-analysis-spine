import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
from statsmodels.graphics.factorplots import interaction_plot
import pandas as pd
plt.rc('font', family='serif',size=20)
matplotlib.rc('text', usetex=True)
matplotlib.rc('legend', fontsize=20)
# matplotlib.rcParams['text.latex.preamble'] = r'\boldmath'
output_path = "D:/Dissetation/overleaf/dissertation/pics"
def plotBoxplot(variable, data):
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='Decade', y=f'{variable}', hue='Sex', data=data, palette='coolwarm')
    plt.title(f'{variable} by Decade and Sex')
    plt.xlabel('Decade')
    plt.ylabel(f'{variable}')
    plt.legend(title='Sex')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

def plotBarplot(variable, data):
    plt.figure(figsize=(16, 9))
    palette = sns.color_palette("Blues", 6)
    sns.barplot(x='Sex', y=f'Superior{variable}', hue='Decade', data=data, errorbar="ci", capsize=.4,
                err_kws={"color": "0.2", "linewidth": 1},
                palette=palette,
            )
    # palette = sns.color_palette("Blues", 2)
    # sns.barplot(x='Decade', y=f'Superior{variable}', hue='Sex', data=data, errorbar="ci", capsize=.4,
    #             err_kws={"color": "0.2", "linewidth": 1},
    #             palette=palette,
    #         )
    plt.xlabel(r'\textbf{Sex}', fontsize=22)
    # plt.ylabel(f'\\textbf{{Normalized {variable} Force (N/(kg/m^2))}}', fontsize=22)
    plt.ylabel(r'\textbf{Normalized Resultant Force ($\frac{N}{\mathrm{kg/m}^2}$)}', fontsize=22)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(f'{variable.lower()}_age.png', format="png", bbox_inches="tight")
    plt.show()

def plotKinematicsBarplot(variable, data):
    plt.figure(figsize=(16, 9))
    palette = sns.color_palette("Blues", 6)
    sns.barplot(x='Sex', y=f'{variable}', hue='Decade', data=data, errorbar="ci", capsize=.4,
                err_kws={"color": "0.2", "linewidth": 1},
                palette=palette,
            )
    # palette = sns.color_palette("Blues", 2)
    # sns.barplot(x='Decade', y=f'Superior{variable}', hue='Sex', data=data, errorbar="ci", capsize=.4,
    #             err_kws={"color": "0.2", "linewidth": 1},
    #             palette=palette,
    #         )
    plt.xlabel(r'\textbf{Sex}', fontsize=22)
    plt.ylabel(f'\\textbf{{{variable} (deg)}}', fontsize=22)
    # plt.ylabel(r'\textbf{Position (deg)}', fontsize=22)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(f'{variable.lower()}_age.png', format="png", bbox_inches="tight")
    plt.show()

def plotBarplotMuscleForce(variable, data):
    plt.figure(figsize=(16, 9))
    palette = sns.color_palette("Blues", 6)
    sns.barplot(x='Muscle', y=f'{variable}', hue='Decade', data=data, errorbar="ci", capsize=.4,
                err_kws={"color": "0.2", "linewidth": 1},
                palette=palette,
            )
    # plt.xlabel(r'\textbf{Age Group}', fontsize=22)
    # plt.ylabel(f'\\textbf{{{variable} (N)}}', fontsize=22)
    plt.xlabel(r'\textbf{Muscle}', fontsize=22)
    plt.ylabel(r'\textbf{Normalized Total Force ($\frac{N}{\mathrm{kg/m}^2}$)}', fontsize=22)
    plt.legend(fontsize=16)#, loc="upper left", bbox_to_anchor=(1, 1))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(f'{output_path}/{variable.lower()}_age_normalzied.png', format="png", bbox_inches="tight")
    plt.show()

def plotBarplotMuscleMoment(variable, data):
    plt.figure(figsize=(16, 9))
    palette = sns.color_palette("Blues", 6)
    sns.barplot(x='Type', y=f'Value', hue='Decade', data=data, errorbar="ci", capsize=.4,
                err_kws={"color": "0.2", "linewidth": 1},
                palette=palette,
            )
    # plt.xlabel(r'\textbf{Decade}', fontsize=22)
    plt.xlabel(r'\textbf{Plane}', fontsize=22)
    plt.ylabel(r'\textbf{Normalized Moment ($\frac{Nm}{\mathrm{kg/m}^2}$)}', fontsize=22)
    # plt.ylabel(f'\\textbf{{Moment (Nm)}}', fontsize=22)
    plt.legend(fontsize=16)#, loc="upper left", bbox_to_anchor=(1, 1))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(f'{variable.lower()}_age.png', format="png", bbox_inches="tight")
    plt.show()


# Load dataset
path = "E:/Quanitifying EMG/Summary-Spinal Loads.csv"
data = pd.read_csv(path)
variable = 'Resultant'
variable = 'Compression'
variable = 'LateralShear'
variable = 'AnteriorPosterorShear'
data['Status'] = data['Status'].replace('Control', 'Asymptomatic')
sorted_decades = sorted(data['Decade'].unique())
data['Decade'] = pd.Categorical(data['Decade'], categories=sorted_decades, ordered=True)
# data = data[data['Trial Weighted'] == True]
# data = data[data['Trial Weighted'] == False]
# data = data[data['Trial Pace'] == 'Slow']
# data = data[data['Trial Pace'] == 'Fast']
# data[variable] = data[variable]/data['Weight']
for variable in ['Resultant', 'Compression', 'LateralShear', 'AnteriorPosterorShear']:
    data[f'Inferior{variable}'] = data[f'Inferior{variable}']/data['BMI']
    data[f'Superior{variable}'] = data[f'Superior{variable}']/data['BMI']
data.to_csv('E:/Quanitifying EMG/Summary-Spinal Loads bmi normalized.csv', index=False)
control_data = data[data['Status'] == 'Asymptomatic']
lbp_data = data[data['Status'] == 'Low Back Pain Patient']
plotBarplot(variable, data)

# path = "E:/Quanitifying EMG/Summary-motion.csv"
# data = pd.read_csv(path)
# variable = 'Position'
# # variable = 'Velocity'
# # variable = 'Acceleration'
# # data['Status'] = data['Status'].replace('Control', 'Asymptomatic')
# sorted_decades = sorted(data['Decade'].unique())
# data['Decade'] = pd.Categorical(data['Decade'], categories=sorted_decades, ordered=True)
# # # data = data[data['Trial Weighted'] == True]
# # # data = data[data['Trial Weighted'] == False]
# # # data = data[data['Trial Pace'] == 'Slow']
# # # data = data[data['Trial Pace'] == 'Fast']
# # data[variable] = data[variable]/data['Weight']
# # data[f'{variable}'] = data[f'{variable}']/data['BMI']
# control_data = data[data['Status'] == 'Asymptomatic']
# lbp_data = data[data['Status'] == 'Low Back Pain Patient']
# plotKinematicsBarplot(variable, data)

# path = "E:/Quanitifying EMG/Summary-Muscle Forces.csv"
# data = pd.read_csv(path)
# sorted_decades = sorted(data['Decade'].unique())
# data['Decade'] = pd.Categorical(data['Decade'], categories=sorted_decades, ordered=True)
# data['Muscle'] = data['Muscle'].replace('RightErectorSpinae', 'RES')
# data['Muscle'] = data['Muscle'].replace('LeftErectorSpinae', 'LES')
# data['Muscle'] = data['Muscle'].replace('RightInternalOblique', 'RIO')
# data['Muscle'] = data['Muscle'].replace('LeftInternalOblique', 'LIO')
# data['Muscle'] = data['Muscle'].replace('RightLatissimusDorsi', 'RLD')
# data['Muscle'] = data['Muscle'].replace('LeftLatissimusDorsi', 'LLD')
# data['Muscle'] = data['Muscle'].replace('RightExternalOblique', 'REO')
# data['Muscle'] = data['Muscle'].replace('LeftExternalOblique', 'LEO')
# data['Muscle'] = data['Muscle'].replace('RightRectusAbdominis', 'RRA')
# data['Muscle'] = data['Muscle'].replace('LeftRectusAbdominis', 'LRA')

# data['Total'] = data[f'Total']/data['BMI']
# # data.to_csv('E:/Quanitifying EMG/Summary-Muscle Forces bmi normalized.csv', index=False)
# plotBarplotMuscleForce('Total', data)

# path = "E:/Quanitifying EMG/Summary-Muscle Moments.csv"
# data = pd.read_csv(path)
# sorted_decades = sorted(data['Decade'].unique())
# data['Decade'] = pd.Categorical(data['Decade'], categories=sorted_decades, ordered=True)
# variable_columns = [f'Sagittal', f'Lateral', f'Axial']#, f'Weighted']
# for v in variable_columns:
#     data[f'{v}'] = data[f'{v}']/data['BMI']
# data_melted = data.melt(id_vars=['Decade'], value_vars=variable_columns,
#                         var_name='Type', value_name='Value')
# data_melted['Type'] = data_melted['Type'].str.replace(f'', '', regex=False)
# # Plot configuration
# plotBarplotMuscleMoment('Moment', data_melted)