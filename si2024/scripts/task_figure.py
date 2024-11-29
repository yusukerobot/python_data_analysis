import numpy as np
import matplotlib.pyplot as plt
import csv

filename = 'data/overview_data/task_data.csv'

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
        # Assuming the first column is time data and the second column is battery data
        time_data.append(float(row[0]))
        task_data.append(float(row[3]))

# Plot the data
plt.rcParams["font.family"] = "TeX Gyre Termes"   # 使用するフォント
plt.rcParams["font.size"] = 30

width_cm = 12.5
height_cm = width_cm / 1.6
width_inch = width_cm * 2 / 2.54  # Convert cm to inches
height_inch = width_inch * 2 / 2.54

bins = np.arange(0, 301, 30)
bin_centers = bins[:-1] + 15

plt.figure(figsize=(width_inch, height_inch))
plt.bar(bin_centers, task_data, width=30, color='r', alpha=0.7, edgecolor='black')

plt.xlabel('Time [min]')
plt.ylabel('Number of goals reached [times]')
plt.xticks(np.arange(0, 301, 60))  # Set the x-axis ticks from 0 to 300, stepping by 30
plt.grid(False)

ax = plt.gca()
ax.tick_params(direction='in', length=6, width=1)
plt.show()
