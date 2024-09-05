import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
from IPython.display import display

filename = 'data/2024-08-28/task_data.csv'

colum = ["1", "2", "3", "4", "5"]
index = ["Conventional system", "Proposed system"]
task_completion_amount_data1 =[]
task_completion_amount_data2 =[]

with open(filename, newline='') as csv_file:
    csv_reader = csv.reader(csv_file)
    # Skip the header row
    next(csv_reader)
    
    # Read the rest of the rows
    for row in csv_reader:
        # Assuming the first column is time data and the second column is battery data
        task_completion_amount_data1.append(int(row[0]))
        task_completion_amount_data2.append(int(row[1]))

# pd.rcParams["font.family"] = " TeX Gyre Termes"   # 使用するフォント
# pd.rcParams["font.size"] = 10

data_list =[task_completion_amount_data1, task_completion_amount_data2]

df = pd.DataFrame(data=data_list, index = index, columns = colum)

display(df)

width_cm = 12.5
height_cm = width_cm / 1.6
width_inch = width_cm * 2 / 2.54  # Convert cm to inches
height_inch = width_inch * 2 / 2.54



