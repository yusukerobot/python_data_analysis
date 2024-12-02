import numpy as np
import matplotlib.pyplot as plt
import csv

filename = '../data/overview_data/poster_task_data.csv'

# Initialize lists to store data
time_data = []
task_data = []

# Open and read the CSV file
with open(filename, newline='') as csv_file:
    csv_reader = csv.reader(csv_file)
    # Skip the header row
    next(csv_reader)
    
    # Read the rest of the rows
    for row in csv_reader:
        # Assuming the first column is time data and the second column is task data
        time_data.append(float(row[0]))
        task_data.append(float(row[7]))

# Plot settings
plt.rcParams["font.family"] = "TeX Gyre Termes"
plt.rcParams["font.size"] = 35

width_cm = 14.5
height_cm = width_cm / 1.6
width_inch = width_cm * 2 / 2.54  # Convert cm to inches
height_inch = width_inch * 2 / 2.54

# Define bins and left edges
bins = np.arange(0, 301, 60)  # Bins: 0-60, 60-120, ..., 240-300
bin_edges = bins[:-1]  # Start positions of each bin
bar_width = 60  # Full width of each bin

# Plot the data
plt.figure(figsize=(width_inch, height_inch))
plt.bar(bin_edges, task_data[:len(bin_edges)], width=bar_width, color='r', alpha=0.7, edgecolor='black', align='edge')

plt.xlabel('Time [min]')
plt.ylabel('Number of goals reached [times]')
plt.xticks(np.arange(0, 301, 60))  # Set x-axis ticks
# plt.yticks(np.arange(0, 170, 25))
plt.yticks([0, 25, 50, 75, 100, 125, 150, 175])
plt.grid(False)

ax = plt.gca()
ax.tick_params(direction='in', length=6, width=1)
plt.show()
