import pandas as pd

# Load the uploaded file to understand its structure and contents

import matplotlib.pyplot as plt
import seaborn as sns

path = "E:/Quanitifying EMG/demog.tsv"
data = pd.read_csv(path, sep='\t')

# Display the first few rows and column information to assess the data structure
data_info = {
    "head": data.head(),
    "columns": data.columns.tolist(),
    "dtypes": data.dtypes.to_dict(),
    "summary": data.describe(include='all').transpose()
}
data_info
# Set a style for the plots
sns.set(style="whitegrid")

# Distribution plots for continuous variables: Height, Weight, BMI, Age
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
continuous_vars = ['Height', 'Weight', 'BMI', 'Age at Creation']
for ax, var in zip(axes.flat, continuous_vars):
    sns.histplot(data[var], kde=True, ax=ax, bins=10, color="skyblue")
    ax.set_title(f"Distribution of {var}")
    ax.set_xlabel(var)
    ax.set_ylabel("Frequency")

plt.tight_layout()
plt.show()

# Boxplot comparison: Height, Weight, BMI by Series and Birth Sex
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
compare_vars = ['Height', 'Weight', 'BMI']
categories = ['Series', 'Birth Sex']
for i, (var, cat) in enumerate(zip(compare_vars * 2, categories * 2)):
    sns.boxplot(data=data, x=cat, y=var, ax=axes.flat[i], palette="Set2")
    axes.flat[i].set_title(f"{var} by {cat}")
    axes.flat[i].set_xlabel(cat)
    axes.flat[i].set_ylabel(var)

plt.tight_layout()
plt.show()

# Scatter plots to explore relationships: Height vs Weight, BMI vs Age
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
scatter_pairs = [('Height', 'Weight'), ('BMI', 'Age at Creation')]
for ax, (x, y) in zip(axes, scatter_pairs):
    sns.scatterplot(data=data, x=x, y=y, hue='Birth Sex', style='Series', ax=ax, palette="deep")
    ax.set_title(f"{y} vs {x}")
    ax.set_xlabel(x)
    ax.set_ylabel(y)

plt.tight_layout()
plt.show()

# Category proportions: Series and Birth Sex
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
for ax, cat in zip(axes, ['Series', 'Birth Sex']):
    category_counts = data[cat].value_counts()
    category_counts.plot.pie(autopct='%1.1f%%', ax=ax, colors=sns.color_palette("pastel"))
    ax.set_ylabel("")
    ax.set_title(f"Proportion of {cat}")

plt.tight_layout()
plt.show()

