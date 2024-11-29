import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import pandas as pd
import csv

csv_file = '../data/parents.csv'

# 最初の2行をスキップ
data = pd.read_csv(csv_file, skiprows=1, sep=",")

f1 = data['f1']
f2 = data['f2']

plt.rcParams["font.family"] = "TeX Gyre Termes"
plt.rcParams['font.size'] = 25

width_cm = 12.5
height_cm = width_cm / 1.6
width_inch = width_cm * 2 / 2.54
height_inch = width_inch * 2 / 2.54

plt.figure(figsize=(width_inch, height_inch))
plt.scatter(f1, f2, color='b', marker='o', facecolors='none', edgecolors='b', s=100, label="Data Points")
plt.xlabel('f1 [min]')
plt.ylabel('f2 [min]')

# 目盛り設定、MaxNLocatorで整数表示
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True, prune='lower'))
plt.xticks(np.arange(int(min(f1)//10)*10, int(max(f1)//10)*10 + 10, 10))  # 10の倍数
plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True, prune='lower'))
plt.yticks(np.arange(int(min(f2)//5)*5, int(max(f2)//5)*5 + 5, 5))  # 5の倍数
plt.tick_params(axis='both', labelsize=20)

plt.grid(False)

plt.show()
