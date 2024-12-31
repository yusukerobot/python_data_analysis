import pandas as pd
import matplotlib.pyplot as plt

# CSVファイルを読み込む
file_path = '../data/goal_monitoring_data.csv'  # CSVファイルのパス
data = pd.read_csv(file_path)

# グラフ用のデータを取得
time = data['Accumulated Time [min]']
battery = data['Battery [%]']

# グラフのフォントとサイズ設定
plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams["font.family"] = "TeX Gyre Termes"  # フォント設定
plt.rcParams['font.size'] = 30  # フォントサイズ設定

# グラフの寸法設定（cmからインチに変換）
width_cm = 14.5  # 幅の設定（cm）
height_cm = width_cm / 1.6  # 高さを幅の1.6倍に設定
width_inch = width_cm / 2.54  # cmからインチに変換
height_inch = height_cm / 2.54  # cmからインチに変換

# グラフの作成
fig, ax = plt.subplots(figsize=(width_inch, height_inch))
ax.plot(time, battery, label='Battery Charge (%)', color='blue', linewidth=2)

# 軸ラベルとタイトルの設定
ax.set_xlabel('Time [min]', fontsize=30)
ax.set_ylabel(r'Battery Charge [%]', fontsize=30)

# グリッドと凡例の設定
ax.grid(True, linestyle='--', alpha=0.7)
ax.legend(fontsize=25)

# レイアウト調整と表示
plt.tight_layout()
plt.show()
