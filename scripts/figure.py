import numpy as np
import matplotlib.pyplot as plt
import csv

filename = 'data/2024-08-28/selected_data.csv'

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
plt.rcParams["font.family"] = " TeX Gyre Termes"   # 使用するフォント
plt.rcParams["font.size"] = 20

width_cm = 12.5
height_cm = width_cm / 1.6
width_inch = width_cm * 2 / 2.54  # Convert cm to inches
height_inch = width_inch * 2 / 2.54

plt.figure(figsize=(width_inch, height_inch))
plt.plot(time_data, battery_data, linestyle='-', color='b')
plt.xlabel('Time [min]')
plt.ylabel('Battery Level [%]')
plt.grid(True)

ax = plt.gca()
ax.tick_params(direction='in', length=6, width=1)
ax.set_xticks(np.arange(0, 301, 30))
plt.show()
