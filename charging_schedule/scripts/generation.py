import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import pandas as pd
import csv

csv_file = '../data/g1.csv'

# 最初の2行をスキップ
data = pd.read_csv(csv_file, skiprows=1, sep=",")

f1 = data['f1']
f2 = data['f2']
f3 = data['front']  # 三列目のデータ

plt.rcParams["font.family"] = "TeX Gyre Termes"
plt.rcParams['font.size'] = 25

width_cm = 12.5
height_cm = width_cm / 1.6
width_inch = width_cm * 2 / 2.54
height_inch = width_inch * 2 / 2.54

plt.figure(figsize=(width_inch, height_inch))

# 全データポイントを青色でプロット
plt.scatter(f1, f2, color='b', marker='o', facecolors='none', edgecolors='b', s=100, label="Data Points")

# 三列目が0のデータポイントを抽出して赤色でプロット
f1_red = f1[data['front'] == 0]
f2_red = f2[data['front'] == 0]
plt.scatter(f1_red, f2_red, color='r', marker='o', facecolors='none', edgecolors='r', s=100, label="f3 = 0")

plt.xlabel('f1 [min]')
plt.ylabel('f2 [min]')

plt.grid(False)
plt.show()
