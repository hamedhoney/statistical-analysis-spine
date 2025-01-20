import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np
import ipywidgets as widgets
from ipywidgets import Layout
from IPython.display import display
import os

# Set up plot styling
plt.rc('font', family='serif', size=20)
matplotlib.rc('text', usetex=True)
matplotlib.rc('legend', fontsize=20)

# Define output path for saving plots
output_path = "D:/Dissetation/overleaf/dissertation/pics"
os.makedirs(output_path, exist_ok=True)

# Function to create the main scatter plot
def plot(data, x, y, hue, filter_column1, filter_values1, filter_column2, filter_values2, endplate, normalize_by_bmi, normalize_by_moment, output_path):
    # Filter data based on the selected columns and values
    filtered_data = data.copy()
    if filter_column1 and filter_values1:
        filtered_data = filtered_data[filtered_data[filter_column1].isin(filter_values1)]
    if filter_column2 and filter_values2:
        filtered_data = filtered_data[filtered_data[filter_column2].isin(filter_values2)]
    
    # Define the y-column based on the endplate
    y_column = f"{endplate}{y}"
    
    # Normalize the y-axis values if requested
    if normalize_by_bmi and 'BMI' in filtered_data.columns:
        filtered_data[y_column] = filtered_data[y_column] / filtered_data['BMI']
        normalization = "bmi"
    elif normalize_by_moment and 'Moment' in filtered_data.columns:
        filtered_data[y_column] = filtered_data[y_column] / filtered_data['Moment']
        normalization = "moment"
    else:
        normalization = "none"
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(16, 9))
    
    hue_unique = filtered_data[hue].nunique()
    palette = sns.color_palette("Blues", hue_unique)
    scatter = sns.scatterplot(
        data=filtered_data,
        x=x,
        y=y_column,
        hue=hue,
        style=hue,
        palette=palette,
        s=200,
        ax=ax
    )
    
    # Format axis labels
    x_label = x.replace("Decade", "Age Group")
    y_label = y.replace('AnteriorPosterorShear', 'AP Shear').replace('LateralShear', 'Lateral Shear')
    
    ax.set_xlabel(f'\\textbf{{{x_label}}}', fontsize=22)
    if normalize_by_bmi:
        ax.set_ylabel(r'\textbf{Normalized ' + f'{y_label}' + r' ($\frac{N}{\mathrm{kg/m}^2}$)}', fontsize=22)
    elif normalize_by_moment:
        ax.set_ylabel(r'\textbf{Normalized ' + f'{y_label}' + r' ($\frac{N}{Nm}$)}', fontsize=22)
    else:
        ax.set_ylabel(f'\\textbf{{{y_label} (N)}}', fontsize=22)
    
    # Create a title based on normalization and filters
    title_parts = []
    if normalize_by_bmi:
        title_parts.append("Normalized by BMI")
    if normalize_by_moment:
        title_parts.append("Normalized by Moment")
    if filter_column1 and filter_values1:
        title_parts.append(f"Filtered by {filter_column1}: {', '.join(map(str, filter_values1))}")
    if filter_column2 and filter_values2:
        title_parts.append(f"Filtered by {filter_column2}: {', '.join(map(str, filter_values2))}")
    
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Generate a filename based on the selected controls
    filename_parts = []
    filename_parts.append(y.lower())
    filename_parts.append(f"by_{hue.lower()}")
    if normalization != "none":
        filename_parts.append(f"normalized_by_{normalization}")
    if filter_column1 and filter_values1:
        filter_str = "_".join([f"{filter_column1.lower()}_{str(v).lower()}" for v in filter_values1])
        filename_parts.append(f"filtered_by_{filter_str}")
    if filter_column2 and filter_values2:
        filter_str = "_".join([f"{filter_column2.lower()}_{str(v).lower()}" for v in filter_values2])
        filename_parts.append(f"filtered_by_{filter_str}")
    filename_parts.append(f"{endplate.lower()}_endplate")
    filename = "_".join(filename_parts) + ".png"
    filepath = os.path.join(output_path, filename)
    
    plt.savefig(filepath, bbox_inches='tight', dpi=300)
    plt.show()
    plt.close()

    # Return the filtered data for use in the distribution plot
    return filtered_data

# Function to create the distribution plot
def plot_distribution(data, motion_index_column, hue_column, output_path):
    """
    Plot the distribution of the motion index for the two groups.
    
    Parameters:
        data (pd.DataFrame): The dataset.
        motion_index_column (str): The column name for the motion index.
        hue_column (str): The column name for grouping (e.g., 'Status').
        output_path (str): The directory to save the plot.
    """
    plt.figure(figsize=(16, 9))
    
    # Create the distribution plot
    sns.histplot(
        data=data,
        x=motion_index_column,
        hue=hue_column,
        kde=True,  # Add kernel density estimate
        # palette="viridis",
        alpha=0.5,
        multiple="layer",  # Overlay the distributions
    )
    
    # Format axis labels
    plt.xlabel(f'\\textbf{{{motion_index_column}}}', fontsize=22)
    plt.ylabel(r'\textbf{Frequency}', fontsize=22)
    
    # Add a title
    plt.title(f'Distribution of {motion_index_column} by {hue_column}', fontsize=24)
    
    # Save the plot
    filename = f"distribution_{motion_index_column.lower()}_by_{hue_column.lower()}.png"
    filepath = os.path.join(output_path, filename)
    plt.savefig(filepath, bbox_inches='tight', dpi=300)
    
    plt.show()
    plt.close()

# Load data
path = "E:/Quanitifying EMG/Summary-Spinal Loads.csv"
data = pd.read_csv(path)
path = "E:/Quanitifying EMG/tscores.tsv"
tscores = pd.read_csv(path, sep='\t')
tscores['Subject'] = tscores['Participant ID'].str.replace('2023LBPEMG-', '').astype(int)
tscores['Subject'] = tscores['Subject'].astype('category')
merged_data = pd.merge(
    data,
    tscores[['Subject', 'Linear Motion Index', 'Linear Motion Index (Streamlined)']],
    on='Subject',
    how='inner'
)
sorted_decades = sorted(merged_data['Decade'].unique())
merged_data['Status'] = merged_data['Status'].replace('Control', 'Asymptomatic')
merged_data['Decade'] = pd.Categorical(merged_data['Decade'], categories=sorted_decades, ordered=True)

# Widgets setup
x_options = ['Linear Motion Index', 'Linear Motion Index (Streamlined)']
y_options = ['Resultant', 'Compression', 'AnteriorPosterorShear', 'LateralShear']
hue_options = ['Status', 'Decade']
filter_column_options = ['Status', 'Decade', 'Trial Name', 'Trial Type', 'Level', None]
endplate_options = ['Superior', 'Inferior']

# Set default filter column and values
default_filter_column1 = 'Level'
unique_levels = merged_data[default_filter_column1].unique()
default_filter_values1 = unique_levels
# default_filter_values1 = ['L5S1']  # Ensure this is a list, even with a single value
default_filter_column2 = 'Trial Name'
unique_values = merged_data[default_filter_column2].unique()
default_filter_values2 = unique_values

# Initialize widgets with default filtering
x_dropdown = widgets.Dropdown(options=x_options, value='Linear Motion Index', description='X-axis:')
y_dropdown = widgets.Dropdown(options=y_options, value='Resultant', description='Y-axis:')
hue_dropdown = widgets.Dropdown(options=hue_options, value='Status', description='Hue:')
filter_column_dropdown1 = widgets.Dropdown(options=filter_column_options, value=default_filter_column1, description='Filter by:')
filter_values_select1 = widgets.SelectMultiple(options=default_filter_values1, value=[default_filter_values1[0]], description='Filter Values:', disabled=False)
filter_column_dropdown2 = widgets.Dropdown(options=filter_column_options, value=default_filter_column2, description='Filter by:')
filter_values_select2 = widgets.SelectMultiple(options=default_filter_values2, value=[default_filter_values2[0]], description='Filter Values:', disabled=False)
endplate_radio = widgets.RadioButtons(options=endplate_options, value='Superior', description='Endplate:')

normalize_by_bmi_checkbox = widgets.Checkbox(value=False, description='Normalize by BMI', disabled=False)
normalize_by_moment_checkbox = widgets.Checkbox(value=False, description='Normalize by Moment', disabled=False)

# Update filter values when filter column changes
def update_filter_values1(change):
    if change['new'] and change['new'] in merged_data.columns:
        unique_values = merged_data[change['new']].unique()
        sorted_values = sorted(unique_values, key=lambda x: str(x))
        filter_values_select1.options = sorted_values
        filter_values_select1.disabled = False
    else:
        filter_values_select1.options = []
        filter_values_select1.disabled = True

def update_filter_values2(change):
    if change['new'] and change['new'] in merged_data.columns:
        unique_values = merged_data[change['new']].unique()
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
    # Call the main scatter plot function and get the filtered data
    filtered_data = plot(merged_data, x, y, hue, filter_column1, filter_values1, filter_column2, filter_values2, endplate, normalize_by_bmi, normalize_by_moment, output_path)
    
    # Call the distribution plot function with the filtered data
    # plot_distribution(filtered_data, x, hue, output_path)

# Create individual widgets first with appropriate layouts
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

# Create horizontal groups for the controls
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

# Main container
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

# Display the container
display(widgets_container)

# Create an interactive output widget
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

# Display the output
display(out)