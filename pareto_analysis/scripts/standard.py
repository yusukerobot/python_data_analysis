import pandas as pd
import math
import matplotlib.pyplot as plt

# CSV file path
input_file_path = '../data/sbx_test.csv'

def calculate_stats_and_distances(input_path):
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
    generations_list = []  # Store generation names
    f1_means = []  # Store f1 mean values
    f1_stds = []  # Store f1 standard deviations
    f2_means = []  # Store f2 mean values
    f2_stds = []  # Store f2 standard deviations

    for gen in generations:
        if gen['name'] == '第0世代':  # Skip generation 0
            continue

        # Calculate f1 and f2 statistics
        f1_mean = sum(gen['f1']) / len(gen['f1']) if gen['f1'] else float('nan')
        f1_std = pd.Series(gen['f1']).std() if gen['f1'] else float('nan')
        f2_mean = sum(gen['f2']) / len(gen['f2']) if gen['f2'] else float('nan')
        f2_std = pd.Series(gen['f2']).std() if gen['f2'] else float('nan')

        f1_means.append(f1_mean)
        f1_stds.append(f1_std)
        f2_means.append(f2_mean)
        f2_stds.append(f2_std)
        generations_list.append(gen['name'])

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
    plt.rcParams["font.family"] = "TeX Gyre Termes"  # Set font for wider character support
    plt.rcParams['font.size'] = 25  # Set font size

    # Graph size settings (cm to inches conversion)
    width_cm = 14.5
    height_cm = width_cm / 1.6
    width_inch = width_cm * 2 / 2.54
    height_inch = width_inch * 2 / 2.54

    # Bar graph for mean and standard deviation
    fig, ax1 = plt.subplots(figsize=(width_inch, height_inch))

    ax1.bar(generations_list, f1_means, yerr=f1_stds, label='f1', alpha=0.6, color='b', capsize=5)
    ax1.bar(generations_list, f2_means, yerr=f2_stds, label='f2', alpha=0.6, color='g', capsize=5)

    ax1.set_xlabel('Generation', color='black')
    ax1.set_ylabel('Mean Value', color='black')
    ax1.tick_params(axis='y', labelcolor='black')
    ax1.set_xticklabels(generations_list, rotation=45, ha='right')
    ax1.set_xticks(generations_list[::10])  # Show ticks at intervals of 10 generations

    ax1.legend(loc='upper left')
    fig.tight_layout()  # Adjust layout

    plt.show()

    # Line graph for average Euclidean distance
    fig, ax2 = plt.subplots(figsize=(width_inch, height_inch))

    ax2.plot(generations_list, total_distances, marker='o', linestyle='-', color='r', label='Euclidean Distance Avg.')

    ax2.set_xlabel('Generation', color='black')
    ax2.set_ylabel('Euclidean Distance Avg.', color='black')
    ax2.tick_params(axis='y', labelcolor='black')

    # Set x-axis ticks every 10 generations
    ax2.set_xticks(generations_list[::10])  # Show ticks at intervals of 10 generations

    fig.tight_layout()  # Adjust layout
    plt.show()

# Run the function
calculate_stats_and_distances(input_file_path)
