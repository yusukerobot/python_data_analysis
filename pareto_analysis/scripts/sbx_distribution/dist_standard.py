import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np

# CSV file path
input_file_path = '../../data/sbx_distribution/sbx_distribution.csv'

def calculate_stats_and_distances(input_path, xticks_labels=None, yticks_bar=None, yticks_line=None):
    with open(input_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    generations = []
    current_generation = None
    f1_values = []
    f2_values = []

    # Initial generation data storage
    initial_data = []

    for line in lines:
        line = line.strip()
        if not line:  # Skip empty lines
            continue
        if line.startswith('第') and '世代' in line:
            if current_generation:
                generations.append({
                    'name': current_generation,
                    'f1': f1_values,
                    'f2': f2_values
                })
            current_generation = line
            f1_values = []
            f2_values = []
        elif ',' in line and not line.startswith('f1,f2'):
            values = line.split(',')
            if len(values) == 2:
                try:
                    f1 = float(values[0])
                    f2 = float(values[1])
                    f1_values.append(f1)
                    f2_values.append(f2)
                    # Save initial generation data
                    if current_generation == "第0世代":
                        initial_data.append((f1, f2))
                except ValueError:
                    continue

    if current_generation:
        generations.append({
            'name': current_generation,
            'f1': f1_values,
            'f2': f2_values
        })

    # Euclidean distance function
    def euclidean_distance(x1, y1, x2, y2):
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    # Calculate statistics and Euclidean distances
    total_distances = []  # Store total Euclidean distances for each generation
    generations_list = []  # Store generation indices
    f1_means = []  # Store f1 mean values
    f1_stds = []  # Store f1 standard deviations
    f2_means = []  # Store f2 mean values
    f2_stds = []  # Store f2 standard deviations

    for i, gen in enumerate(generations):
        if gen['name'] == '第0世代':  # Skip generation 0
            continue

        # Calculate f1 and f2 statistics
        f1_mean = sum(gen['f1']) / len(gen['f1']) if gen['f1'] else float('nan')
        f1_std = pd.Series(gen['f1']).std(ddof=0) if gen['f1'] else float('nan')
        f2_mean = sum(gen['f2']) / len(gen['f2']) if gen['f2'] else float('nan')
        f2_std = pd.Series(gen['f2']).std(ddof=0) if gen['f2'] else float('nan')

        f1_means.append(f1_mean)
        f1_stds.append(f1_std)
        f2_means.append(f2_mean)
        f2_stds.append(f2_std)
        generations_list.append(i)  # Skip generation 0, hence add +1

        # Calculate the average Euclidean distance for this generation
        total_distance = 0  # Initialize total distance for this generation
        for i, (f1, f2) in enumerate(zip(gen['f1'], gen['f2'])):
            distances = [
                euclidean_distance(f1, f2, init_f1, init_f2) for init_f1, init_f2 in initial_data
            ]
            closest_distance = min(distances)  # Get minimum distance
            total_distance += closest_distance  # Add to total distance
        average_distance = total_distance / len(gen['f1']) if gen['f1'] else 0  # Average distance
        total_distances.append(average_distance)  # Append average distance for this generation

    # Graph settings
    plt.rcParams['mathtext.fontset'] = 'cm'
    plt.rcParams["font.family"] = "TeX Gyre Termes"  # Set font for wider character support
    plt.rcParams['font.size'] = 30  # Set font size

    # Graph size settings (cm to inches conversion)
    width_cm = 16.5
    height_cm = width_cm / 1.6
    width_inch = width_cm * 2 / 2.54
    height_inch = width_inch * 2 / 2.54

    # If xticks_labels is not specified, use all generations
    if xticks_labels is None:
        xticks_labels = generations_list

    # Bar graph for mean and standard deviation
    fig, ax1 = plt.subplots(figsize=(width_inch, height_inch))

    ax1.bar(generations_list, f1_means, yerr=f1_stds, label='f1', alpha=0.7, color='blue', capsize=5)
    ax1.bar(generations_list, f2_means, yerr=f2_stds, label='f2', alpha=0.7, color='green', capsize=5)

    ax1.set_xlabel('$\eta$', color='black')
    ax1.set_ylabel('Objective function value [min]', color='black')
    ax1.tick_params(axis='y', labelcolor='black')
    
    # Set x-ticks to the specified generation labels
    ax1.set_xticks(xticks_labels)  # Custom x-ticks
    ax1.set_xticklabels([str(x) for x in xticks_labels])  # Display corresponding labels

    # Set custom y-ticks if provided
    if yticks_bar:
        min_val, max_val, step_size = yticks_bar
        ax1.set_yticks(np.arange(min_val, max_val + step_size, step_size))

    ax1.legend(loc='upper right', bbox_to_anchor=(1.1,1.0))
    fig.tight_layout()  # Adjust layout

    plt.show()

    # Line graph for average Euclidean distance
    fig, ax2 = plt.subplots(figsize=(width_inch, height_inch))

    ax2.plot(generations_list, total_distances, marker='o', linestyle='-', color='r', label='Euclidean Distance Avg.')

    ax2.set_xlabel('$\eta$', color='black')
    ax2.set_ylabel('Distance to parents in the objective space [min]', color='black')
    ax2.tick_params(axis='y', labelcolor='black')

    # Set x-axis ticks to match the generation numbers and custom labels
    ax2.set_xticks(xticks_labels)  # Set custom x-ticks
    ax2.set_xticklabels([str(x) for x in xticks_labels])  # Display corresponding labels

    # Set custom y-ticks if provided
    if yticks_line:
        min_val, max_val, step_size = yticks_line
        ax2.set_yticks(np.arange(min_val, max_val + step_size, step_size))

    ax1.legend(loc='upper right')
    fig.tight_layout()  # Adjust layout
    plt.show()

# Example: Specify custom x-tick labels and y-tick labels for both graphs (min, max, step)
custom_xticks = [1, 5, 10, 15, 20]  # Custom x-axis labels
yticks_bar = (0, 160, 20)  # Custom y-ticks for the bar graph (min, max, step)
yticks_line = (0.7, 0.9, 0.1)  # Custom y-ticks for the line graph (min, max, step)
calculate_stats_and_distances(input_file_path, xticks_labels=custom_xticks, yticks_bar=yticks_bar, yticks_line=yticks_line)
