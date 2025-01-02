import pandas as pd
import matplotlib.pyplot as plt

# CSVファイルのパス
input_file_path = '../data/sbx/total_sbx.csv'

# 描画設定
plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams["font.family"] = "TeX Gyre Termes"
plt.rcParams['font.size'] = 30

# グラフサイズの設定
width_cm = 14.5
height_cm = width_cm / 1.6
width_inch = width_cm * 2 / 2.54
height_inch = width_inch * 2 / 2.54

# データの読み込みと整形
def load_data(file_path):
    data = {}
    with open(file_path, 'r') as f:
        lines = f.readlines()
        current_key = None
        for line in lines:
            line = line.strip()
            if not line:  # 空行をスキップ
                continue
            if line.startswith("f1,f2,time_count"):  # ヘッダー行をスキップ
                continue
            if any(char.isalpha() for char in line):  # セクション名の検出
                current_key = line
                data[current_key] = []  # 新しいセクションのデータを初期化
            else:
                try:
                    values = list(map(float, line.split(',')))  # 数値データを処理
                    data[current_key].append(values)
                except ValueError:
                    print(f"Skipping line: {line}")  # エラー行をスキップ
    for key in data.keys():
        data[key] = pd.DataFrame(data[key], columns=["f1", "f2", "time_count"])
    return data


# データ読み込み
data = load_data(input_file_path)

# プロット
fig, ax = plt.subplots(figsize=(width_inch, height_inch))

# 各データセットをプロット
colors = {"first_generation": 'k', "eta2": 'b', "eta5": 'g', "eta10": 'r', "eta20": 'c', "eta50": 'm'}
markers = {"first_generation": 'x', "eta2": 'o', "eta5": 'o', "eta10": 'o', "eta20": 'o', "eta50": 'o'}

for key, df in data.items():
    if key == "first_generation":
        ax.scatter(df["f1"], df["f2"], c=colors[key], marker=markers[key], label=key)
    else:
        ax.scatter(df["f1"], df["f2"], c=colors[key], marker=markers[key], label=key, edgecolors='k')

# 軸ラベルと凡例
ax.set_xlabel('$f_1$', fontsize=30)
ax.set_ylabel('$f_2$', fontsize=30)
ax.legend(fontsize=20)
ax.grid(True)

# グラフを保存
plt.tight_layout()
plt.savefig('scatter_plot.png')
plt.show()
