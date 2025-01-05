import pandas as pd
import math
import matplotlib.pyplot as plt

# CSV file path
input_file_path = '../../data/sbx_distribution/sbx_distribution.csv'

def calculate_centroid_distances(input_path):
    with open(input_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    generations = []
    current_generation = None
    f1_values = []
    f2_values = []

    # Initial generation data storage
    initial_f1_values = []
    initial_f2_values = []

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
                        initial_f1_values.append(f1)
                        initial_f2_values.append(f2)
                except ValueError:
                    continue

    if current_generation:
        generations.append({
            'name': current_generation,
            'f1': f1_values,
            'f2': f2_values
        })

    # Calculate initial centroid
    initial_centroid = (
        sum(initial_f1_values) / len(initial_f1_values) if initial_f1_values else float('nan'),
        sum(initial_f2_values) / len(initial_f2_values) if initial_f2_values else float('nan')
    )

    # Euclidean distance function
    def euclidean_distance(x1, y1, x2, y2):
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    # Calculate centroid distances
    centroid_distances = []  # Store Euclidean distances for each generation
    generations_list = []  # Store generation names

    for gen in generations:
        if gen['name'] == '第0世代':  # Skip generation 0
            continue

        # Calculate centroid for the current generation
        centroid = (
            sum(gen['f1']) / len(gen['f1']) if gen['f1'] else float('nan'),
            sum(gen['f2']) / len(gen['f2']) if gen['f2'] else float('nan')
        )

        # Calculate the Euclidean distance from the initial centroid
        distance = euclidean_distance(
            initial_centroid[0], initial_centroid[1], centroid[0], centroid[1]
        )
        centroid_distances.append(distance)
        generations_list.append(gen['name'])

    # Plot the Euclidean distance changes
    plt.rcParams['mathtext.fontset'] = 'cm'
    plt.rcParams["font.family"] = "TeX Gyre Termes"
    plt.rcParams['font.size'] = 25

    # Graph size settings (cm to inches conversion)
    width_cm = 14.5
    height_cm = width_cm / 1.6
    width_inch = width_cm * 2 / 2.54
    height_inch = width_inch * 2 / 2.54

    fig, ax = plt.subplots(figsize=(width_inch, height_inch))

    ax.plot(generations_list, centroid_distances, marker='o', linestyle='-', color='r', label='Centroid Distance')
    ax.set_xlabel('Generation', color='black')
    ax.set_ylabel('Euclidean Distance', color='black')
    ax.tick_params(axis='y', labelcolor='black')

    # Set x-axis ticks every 10 generations
    ax.set_xticks(range(0, len(generations_list), 10))
    ax.set_xticklabels(generations_list[::10], rotation=45, ha='right')

    ax.legend(loc='upper left')
    fig.tight_layout()
    plt.show()

# Run the function
calculate_centroid_distances(input_file_path)
