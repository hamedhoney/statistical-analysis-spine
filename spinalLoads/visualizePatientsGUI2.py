import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np
import ipywidgets as widgets
from ipywidgets import Layout
from IPython.display import display
import os

plt.rc('font', family='serif', size=20)
matplotlib.rc('text', usetex=True)
matplotlib.rc('legend', fontsize=20)
output_path = "D:/Dissetation/overleaf/dissertation/pics"
os.makedirs(output_path, exist_ok=True)

def plot(data, x, y, hue, filter_column1, filter_values1, filter_column2, filter_values2, endplate, normalize_by_bmi, normalize_by_moment, output_path):
    filtered_data = data.copy()
    if filter_column1 and filter_values1:
        filtered_data = filtered_data[filtered_data[filter_column1].isin(filter_values1)]
    if filter_column2 and filter_values2:
        filtered_data = filtered_data[filtered_data[filter_column2].isin(filter_values2)]
    
    if y in ['Axial', 'Lateral', 'Sagittal', 'Total']:
        y_column = y
        unit = 'Nm'
    else:
        y_column = f"{endplate}{y}"
        unit = 'N'
    
    if normalize_by_bmi and 'BMI' in filtered_data.columns:
        filtered_data[y_column] = filtered_data[y_column] / filtered_data['BMI']
        y_label = r'\textbf{Normalized ' + y.replace('AnteriorPosteriorShear', 'AP Shear').replace('LateralShear', 'Lateral Shear') + r' ($\frac{N}{\mathrm{kg/m}^2}$)}'
    elif normalize_by_moment and 'Total' in filtered_data.columns:
        filtered_data[y_column] = filtered_data[y_column] / filtered_data['Total']
        y_label = r'\textbf{Normalized ' + y.replace('AnteriorPosteriorShear', 'AP Shear').replace('LateralShear', 'Lateral Shear') + r' ($\frac{N}{Nm}$)}'
    else:
        y_label = f'\\textbf{{{y.replace("AnteriorPosteriorShear", "AP Shear").replace("LateralShear", "Lateral Shear")} ({unit})}}'
    
    fig, ax = plt.subplots(figsize=(16, 9))
    hue_unique = filtered_data[hue].nunique()
    palette = sns.color_palette("Blues", hue_unique)
    
    sns.barplot(
        x=x, y=y_column, hue=hue, data=filtered_data, errorbar="ci", capsize=.4,
        err_kws={"color": "0.2", "linewidth": 1}, palette=palette
    )
    
    plt.xlabel(f'\\textbf{{{x.replace("Decade", "Age Group")}}}', fontsize=22)
    plt.ylabel(y_label, fontsize=22)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    filename = f"barplot_{y.lower()}_by_{hue.lower()}"
    if normalize_by_bmi:
        filename += "_normalized_by_bmi"
    elif normalize_by_moment:
        filename += "_normalized_by_moment"
    if filter_column1 and filter_values1:
        filename += f"_filtered_by_{filter_column1.lower()}_{'_'.join(map(str, filter_values1)).lower()}"
    if filter_column2 and filter_values2:
        filename += f"_filtered_by_{filter_column2.lower()}_{'_'.join(map(str, filter_values2)).lower()}"
    filename += f"_{endplate.lower()}_endplate.png"
    
    plt.savefig(os.path.join(output_path, filename), bbox_inches='tight', dpi=300)
    plt.show()
    plt.close()


path = "E:/Quanitifying EMG/Summary-Spinal Loads.csv"
data = pd.read_csv(path)
sorted_decades = sorted(data['Decade'].unique())
data['Status'] = data['Status'].replace('Control', 'Asymptomatic')
data['Decade'] = pd.Categorical(data['Decade'], categories=sorted_decades, ordered=True)

x_options = ['Status', 'Decade', 'Level']
y_options = ['Resultant', 'Compression', 'AnteriorPosteriorShear', 'LateralShear', 'Axial', 'Lateral', 'Sagittal', 'Total']
hue_options = ['Status', 'Decade']
filter_column_options = ['Status', 'Decade', 'Trial Name', 'Trial Type', 'Level', None]
endplate_options = ['Superior', 'Inferior']

default_filter_column1 = 'Level'
unique_levels = data[default_filter_column1].unique()
default_filter_values1 = unique_levels
default_filter_column2 = 'Trial Name'
unique_trials = data[default_filter_column2].unique()
default_filter_values2 = unique_trials

x_dropdown = widgets.Dropdown(options=x_options, value='Level', description='X-axis:')
y_dropdown = widgets.Dropdown(options=y_options, value='Resultant', description='Y-axis:')
hue_dropdown = widgets.Dropdown(options=hue_options, value='Status', description='Hue:')
filter_column_dropdown1 = widgets.Dropdown(options=filter_column_options, value=default_filter_column1, description='Filter by:')
filter_values_select1 = widgets.SelectMultiple(options=default_filter_values1, description='Filter Values:', disabled=False)
filter_column_dropdown2 = widgets.Dropdown(options=filter_column_options, value=default_filter_column2, description='Filter by:')
filter_values_select2 = widgets.SelectMultiple(options=default_filter_values2, description='Filter Values:', disabled=False)
endplate_radio = widgets.RadioButtons(options=endplate_options, value='Superior', description='Endplate:')

normalize_by_bmi_checkbox = widgets.Checkbox(value=False, description='Normalize by BMI', disabled=False)
normalize_by_moment_checkbox = widgets.Checkbox(value=False, description='Normalize by Moment', disabled=False)

def update_filter_values1(change):
    if change['new'] and change['new'] in data.columns:
        unique_values = data[change['new']].unique()
        sorted_values = sorted(unique_values, key=lambda x: str(x))
        filter_values_select1.options = sorted_values
        filter_values_select1.disabled = False
    else:
        filter_values_select1.options = []
        filter_values_select1.disabled = True

def update_filter_values2(change):
    if change['new'] and change['new'] in data.columns:
        unique_values = data[change['new']].unique()
        sorted_values = sorted(unique_values, key=lambda x: str(x))
        filter_values_select2.options = sorted_values
        filter_values_select2.disabled = False
    else:
        filter_values_select2.options = []
        filter_values_select2.disabled = True

filter_column_dropdown1.observe(update_filter_values1, names='value')
filter_column_dropdown2.observe(update_filter_values2, names='value')

# Function to update both plots
def update_plot(x, y, hue, filter_column1, filter_values1, filter_column2, filter_values2, endplate, normalize_by_bmi, normalize_by_moment):
    filtered_data = plot(data, x, y, hue, filter_column1, filter_values1, filter_column2, filter_values2, endplate, normalize_by_bmi, normalize_by_moment, output_path)
    # plot_distribution(filtered_data, x, hue, output_path)

x_dropdown.layout = Layout(width='200px', margin='5px')
y_dropdown.layout = Layout(width='200px', margin='5px')
hue_dropdown.layout = Layout(width='200px', margin='5px')
endplate_radio.layout = Layout(width='200px', margin='5px')
normalize_by_bmi_checkbox.layout = Layout(width='auto', margin='5px')
normalize_by_moment_checkbox.layout = Layout(width='auto', margin='5px')
filter_column_dropdown1.layout = Layout(width='200px', margin='5px')
filter_values_select1.layout = Layout(width='200px', height='100px', margin='5px')
filter_column_dropdown2.layout = Layout(width='200px', margin='5px')
filter_values_select2.layout = Layout(width='200px', height='100px', margin='5px')

controls_group1 = widgets.HBox([
    widgets.VBox([widgets.HTML('<b>Plot Controls</b>'), x_dropdown, y_dropdown, hue_dropdown])
], layout=Layout(margin='10px'))

controls_group2 = widgets.HBox([
    widgets.VBox([widgets.HTML('<b>Filtering 1</b>'), filter_column_dropdown1, filter_values_select1])
], layout=Layout(margin='10px'))

controls_group3 = widgets.HBox([
    widgets.VBox([widgets.HTML('<b>Filtering 2</b>'), filter_column_dropdown2, filter_values_select2])
], layout=Layout(margin='10px'))

controls_group4 = widgets.HBox([
    widgets.VBox([
        widgets.HTML('<b>Normalization</b>'), 
        endplate_radio,
        widgets.Box([normalize_by_bmi_checkbox], layout=Layout(align_items='flex-start', padding='0px')),
        widgets.Box([normalize_by_moment_checkbox], layout=Layout(align_items='flex-start', padding='0px'))
    ])
], layout=Layout(margin='10px'))

widgets_container = widgets.HBox(
    [controls_group1, controls_group2, controls_group3, controls_group4],
    layout=Layout(
        display='inline-flex',
        flex_flow='row nowrap',
        align_items='flex-start',
        justify_content='space-around',
        width='100%'
    )
)

display(widgets_container)

out = widgets.interactive_output(
    update_plot,
    {
        'x': x_dropdown,
        'y': y_dropdown,
        'hue': hue_dropdown,
        'filter_column1': filter_column_dropdown1,
        'filter_values1': filter_values_select1,
        'filter_column2': filter_column_dropdown2,
        'filter_values2': filter_values_select2,
        'endplate': endplate_radio,
        'normalize_by_bmi': normalize_by_bmi_checkbox,
        'normalize_by_moment': normalize_by_moment_checkbox
    }
)

display(out)