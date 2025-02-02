import numpy as np
import matplotlib.pyplot as plt
import csv

filename = '../data/overview_data/selected_data_dynamic.csv'

# Initialize lists to store data
time_data = []
battery_data = []

# Open and read the CSV file
with open(filename, newline='') as csv_file:
    csv_reader = csv.reader(csv_file)
    # Skip the header row
    next(csv_reader)
    
    # Read the rest of the rows
    for row in csv_reader:
        # Assuming the first column is time data and the second column is battery data
        time_data.append(float(row[0]))
        battery_data.append(float(row[1])* 100 / 19.98)

# Plot the data
plt.rcParams["font.family"] = "TeX Gyre Termes"   # 使用するフォント
plt.rcParams["font.size"] = 35

width_cm = 14.5
height_cm = width_cm / 1.6
width_inch = width_cm * 2 / 2.54  # Convert cm to inches
height_inch = width_inch * 2 / 2.54

plt.figure(figsize=(width_inch, height_inch))
plt.plot(time_data, battery_data, linestyle='-', color='b', linewidth = 4)
plt.xlabel('Time [min]')
plt.ylabel('Battery Level [%]')
# plt.ylim(0, 100)
plt.grid(False)

ax = plt.gca()
ax.tick_params(direction='in', length=6, width=1)
ax.set_xticks(np.arange(0, 301, 60))
ax.set_yticks(np.arange(0, 101, 20))
plt.show()
