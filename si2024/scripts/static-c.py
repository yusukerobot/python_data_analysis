import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import matplotlib
import csv

# CSVファイルのパス
filename = '../data/12-5/static-v1.csv'

# データ格納リストの初期化
time_data = []
task_data = []
cost_short_data = []
cost_charge_data = []

# CSVファイルを開く
with open(filename, newline='') as csv_file:
    csv_reader = csv.reader(csv_file)
    # ヘッダ行をスキップ
    next(csv_reader)
    
    # データの読み込み
    for row in csv_reader:
        # 必要な列を取得
        time_data.append(float(row[0]))
        task_data.append(float(row[2]))
        cost_short_data.append(float(row[7]))
        cost_charge_data.append(float(row[8]))

# グラフの設定
plt.rcParams["font.family"] = "TeX Gyre Termes"   # 使用するフォント
# font_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
# font_prop = FontProperties(fname=font_path)
# matplotlib.rcParams["font.family"] = font_prop.get_name()
plt.rcParams["font.size"] = 35

# グラフサイズの設定
width_cm = 14.5
height_cm = width_cm / 1.6
width_inch = width_cm / 2.54  # cmをインチに変換
height_inch = height_cm / 2.54

plt.figure(figsize=(width_inch, height_inch))

# データのプロット
plt.plot(task_data, cost_short_data, linestyle='-', color='b', linewidth=4, label='$c_{short}$')  # 優先度ショート
plt.plot(task_data, cost_charge_data, linestyle='-', color='r', linewidth=4, label='$c_{charge}$')  # 優先度チャージ
# plt.scatter(time_data, cost_short_data, color='b', s=20, label='Priority Short')  # 青色の散布図
# plt.scatter(time_data, cost_charge_data, color='r', s=20, label='Priority Charge')  # 赤色の散布図
# 軸ラベルの設定
plt.xlabel('Number of work [times]')
plt.ylabel('$C$ [m]')

# グリッド非表示
plt.grid(False)

# 凡例の設定
# plt.legend(loc='best', fontsize=10)

# 軸の目盛設定
ax = plt.gca()
ax.tick_params(direction='in', length=6, width=1)
ax.set_xticks(np.arange(0, 201, 50))  # x軸の目盛を設定
ax.set_yticks(np.arange(8, 21, 2))    # y軸の目盛を設定

plt.xlim(-1, 200)
plt.ylim(7, 20)

# グラフの表示
plt.tight_layout()  # レイアウトの調整
plt.show()
