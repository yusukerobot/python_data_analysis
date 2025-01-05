import os
import glob
import pandas as pd
import matplotlib.pyplot as plt

# 描画設定
plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams["font.family"] = "TeX Gyre Termes"
plt.rcParams['font.size'] = 30

# グラフサイズの設定
width_cm = 14.5
height_cm = width_cm / 1.6
width_inch = width_cm / 2.54
height_inch = height_cm / 2.54

# CSVファイルの最終世代データを取得する関数
def get_final_generation_data(directory_path, file_pattern="eta*.csv", min_eta=None, max_eta=None, step=1):
    file_paths = glob.glob(os.path.join(directory_path, file_pattern))
    final_generation_data = {}
    
    # 指定範囲のetaを生成
    if min_eta is not None and max_eta is not None:
        valid_etas = set(range(min_eta, max_eta + 1, step))
    else:
        valid_etas = None  # 制約なし

    for file_path in file_paths:
        # ファイル名からeta値を取得
        try:
            eta_number = int(os.path.basename(file_path).replace("eta", "").replace(".csv", "").strip())
        except ValueError:
            continue

        # eta値が範囲外ならスキップ
        if valid_etas is not None and eta_number not in valid_etas:
            continue

        with open(file_path, 'r') as file:
            lines = file.readlines()

        current_generation = None
        data = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if line.startswith("第") and "世代" in line:
                current_generation = line
                data = []  # 新しい世代が始まったらデータをリセット
            elif ',' in line and current_generation:
                try:
                    # ヘッダ行をスキップ
                    if line.lower().startswith('f1'):
                        continue
                    # 数値データを追加
                    values = tuple(map(float, line.split(',')))
                    data.append(values)
                except ValueError:
                    continue
        
        # 最終世代のデータを保存
        final_generation_data[eta_number] = data

    return final_generation_data

# 散布図を描画する関数
def plot_final_generation_scatter(final_generation_data):
    colors = ['blue', 'black', 'red', 'orange', 'green', 'yellow']
    markers = ['o', 'x', '^', 'D', 'P', '*']

    plt.figure(figsize=(width_inch, height_inch))

    for idx, (eta, data) in enumerate(sorted(final_generation_data.items())):
        # f1, f2 を分離
        f1_values = [point[0] for point in data]
        f2_values = [point[1] for point in data]
        
        # 散布図を描画
        plt.scatter(
            f1_values, f2_values, 
            label=f"$\eta$ = {eta}", 
            color=colors[idx % len(colors)], 
            marker=markers[idx % len(markers)], 
            s=20  # マーカーサイズ
        )

    # 軸ラベルと凡例
    plt.xlabel("$f_1$")
    plt.ylabel("$f_2$")
    plt.legend(loc="best")
    plt.tight_layout()
    plt.show()

# メイン処理
directory_path = "../../data/sbx/"  # ディレクトリのパス
file_pattern = "eta*.csv"          # 読み込むファイルのパターン

# 数字の範囲を指定
min_eta = 0  # 最小のeta値
max_eta = 20  # 最大のeta値
step = 5      # ステップサイズ

# 最終世代データの取得
final_generation_data = get_final_generation_data(directory_path, file_pattern, min_eta, max_eta, step)

# 散布図を描画
plot_final_generation_scatter(final_generation_data)
