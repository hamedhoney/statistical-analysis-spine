import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib


plt.rc('font', family='serif',size=20)
matplotlib.rc('text', usetex=True)
matplotlib.rc('legend', fontsize=20)
matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['text.latex.preamble'] = r'\boldmath'

path = "E:/Quanitifying EMG/demog.tsv"
data = pd.read_csv(path, sep='\t')

data['Series'].replace('Control', 'Asymptomatic', inplace=True)
data['Series'].replace('Low Back Pain Patient', 'Patient', inplace=True)
# Display the first few rows and column information to assess the data structure
data_info = {
    "head": data.head(),
    "columns": data.columns.tolist(),
    "dtypes": data.dtypes.to_dict(),
    "summary": data.describe(include='all').transpose()
}
output_path = "D:/Dissetation/overleaf/dissertation/pics"
# Set a style for the plots
sns.set(style="whitegrid")
palette = sns.color_palette("Blues", n_colors=2, as_cmap=False)

# Distribution plots for continuous variables: Height, Weight, BMI, Age
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
continuous_vars = ['Height', 'Weight', 'BMI', 'Age at Creation']
for ax, var in zip(axes.flat, continuous_vars):
    sns.histplot(data[var], kde=True, ax=ax, bins=10, palette=palette)
    ax.set_title(f"Distribution of {var}")
    ax.set_xlabel(var)
    ax.set_ylabel("Frequency")

plt.tight_layout()
plt.show()

# # Boxplot comparison: Height, Weight, BMI by Series and Birth Sex
# fig, axes = plt.subplots(2, 2, figsize=(16, 12))
# compare_vars = ['Height', 'Weight', 'BMI']
# categories = ['Series', 'Birth Sex']
# for i, (var, cat) in enumerate(zip(compare_vars * 2, categories * 2)):
#     sns.boxplot(data=data, x=cat, y=var, ax=axes.flat[i], palette="Set2")
#     axes.flat[i].set_title(f"{var} by {cat}")
#     axes.flat[i].set_xlabel(cat)
#     axes.flat[i].set_ylabel(var)

# plt.tight_layout()
# plt.show()

# # Scatter plots to explore relationships: Height vs Weight, BMI vs Age
# fig, axes = plt.subplots(1, 2, figsize=(14, 6))
# scatter_pairs = [('Height', 'Weight'), ('BMI', 'Age at Creation')]
# for ax, (x, y) in zip(axes, scatter_pairs):
#     sns.scatterplot(data=data, x=x, y=y, hue='Birth Sex', style='Series', ax=ax, palette="deep")
#     ax.set_title(f"{y} vs {x}")
#     ax.set_xlabel(x)
#     ax.set_ylabel(y)

# plt.tight_layout()
# plt.show()

# Category proportions: Series and Birth Sex
fig, axes = plt.subplots(1, 2, figsize=(16, 9))
for ax, cat in zip(axes, ['Series', 'Birth Sex']):
    category_counts = data[cat].value_counts()
    category_counts.plot.pie(
        autopct=lambda p: f'{int(round(p * sum(category_counts) / 100))}', 
        # autopct='%1.1f%%', 
        ax=ax, 
        colors=palette,
        labels=category_counts.index,
        textprops={'fontfamily': 'serif', 'fontsize': 20}
    )
    ax.set_ylabel("", fontweight='bold', family='serif')
    ax.set_title(f'\\textbf{{{cat}}}', )

plt.tight_layout()
plt.savefig(f'{output_path}/all_pie_chart.png', format="png", bbox_inches="tight", dpi=300)
plt.show()

# Splitting data into Healthy and Patient groups
healthy_data = data[data['Series'] == 'Asymptomatic']
patient_data = data[data['Series'] == 'Patient']

# Function to display raw counts in pie chart
def plot_pie(ax, group, title):
    category_counts = group['Birth Sex'].value_counts()
    category_counts.plot.pie(
        autopct=lambda p: f'{int(round(p * sum(category_counts) / 100))}', 
        ax=ax, 
        colors=palette,
        labels=category_counts.index,
        textprops={'fontfamily': 'serif', 'fontsize': 20}
    )
    ax.set_ylabel("", fontweight='bold', family='serif')
    ax.set_title(title)

# Creating subplots
fig, axes = plt.subplots(1, 2, figsize=(16, 9))

# Plotting pies
plot_pie(axes[0], healthy_data,  r"\textbf{Assymptomatic}")
plot_pie(axes[1], patient_data, r"\textbf{Patient}")

plt.tight_layout()
plt.savefig(f'{output_path}/demog_pie_chart.png', format="png", bbox_inches="tight", dpi=300)
plt.show()
