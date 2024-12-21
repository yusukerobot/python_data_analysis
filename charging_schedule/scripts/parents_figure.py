import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ファイルのパス
csv_file = '../data/sbx_test/parents.csv'

# CSVファイルを読み込み（header=1で2行目をヘッダとして指定）
df = pd.read_csv(csv_file, header=1)

# カラム名を確認
print(df.columns)  # カラム名を表示して確認

# 描画設定
plt.rcParams["font.family"] = "TeX Gyre Termes"
plt.rcParams['font.size'] = 30

width_cm = 14.5
height_cm = width_cm / 1.6
width_inch = width_cm * 2 / 2.54
height_inch = width_inch * 2 / 2.54

plt.figure(figsize=(width_inch, height_inch))

# f1 と f2 を使って散布図を描画
# linewidthsで丸の太さを指定
plt.scatter(df['f1'], df['f2'], color='black', marker='o', label='Parents', s=100, linewidths=2)

# 軸ラベルの設定
plt.xlabel('f1 [min]')
plt.ylabel('f2 [min]')

# x軸とy軸の目盛りを5刻みに設定
f1_min, f1_max = df['f1'].min(), df['f1'].max()
f2_min, f2_max = df['f2'].min(), df['f2'].max()
x_range = (np.floor(f1_min / 5) * 5, np.ceil(f1_max / 5) * 5)  # 5刻み
y_range = (np.floor(f2_min / 10) * 10, np.ceil(f2_max / 10) * 10)  # 10刻み
x_ticks = np.arange(x_range[0], x_range[1] + 5, 5)  # 5刻み
y_ticks = np.arange(y_range[0], y_range[1] + 10, 10)  # 10刻み

plt.xticks(x_ticks)  
plt.yticks(y_ticks)

# 凡例の設定
plt.legend()

# グラフの表示
# plt.grid(True)
plt.show()
