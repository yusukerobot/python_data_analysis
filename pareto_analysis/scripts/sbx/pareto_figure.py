import os
import glob
import matplotlib.pyplot as plt
import numpy as np

# 描画設定
plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams["font.family"] = "TeX Gyre Termes"
plt.rcParams['font.size'] = 30

# グラフサイズの設定
width_cm = 16.5
height_cm = width_cm / 1.6
width_inch = width_cm / 2.54
height_inch = height_cm / 2.54

# 第0世代データを取得する関数
def get_initial_generation_data(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        initial_data = []
        is_initial_generation = False
        for line in lines:
            line = line.strip()
            if line.startswith("第0世代"):
                is_initial_generation = True  # 第0世代のセクションに到達
            elif line.startswith("第") and "世代" in line:
                is_initial_generation = False  # 第0世代を抜けたら終了
            elif is_initial_generation and ',' in line:
                try:
                    values = tuple(map(float, line.split(',')))
                    initial_data.append(values)
                except ValueError:
                    continue

        return initial_data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []

# 最終世代データを取得する関数
def get_final_generation_data(directory_path, file_pattern="eta*.csv", eta_values=None):
    file_paths = glob.glob(os.path.join(directory_path, file_pattern))
    final_generation_data = {}

    # etaの範囲を設定
    valid_etas = set(eta_values) if eta_values else None

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
        if data:  # 最後に収集した世代データを使用
            final_generation_data[eta_number] = data

    return final_generation_data

# 散布図を描画する関数
def plot_generation_scatter(initial_data, final_generation_data):
    colors = ['red', 'blue', 'green']
    markers = ['o', 'o', 'o']

    plt.figure(figsize=(width_inch, height_inch))

    # 第0世代のデータを描画
    if initial_data:
        f1_values = [point[0] for point in initial_data]
        f2_values = [point[1] for point in initial_data]
        plt.scatter(
            f1_values, f2_values,
            label="Initial generation",
            color='black',
            marker='x',
            s=80
        )

    # 各etaの最終世代データを描画
    for idx, (eta, data) in enumerate(sorted(final_generation_data.items())):
        f1_values = [point[0] for point in data]
        f2_values = [point[1] for point in data]
        
        plt.scatter(
            f1_values, f2_values, 
            label=f"Pareto solution ($\eta$ = {eta})", 
            color=colors[idx % len(colors)], 
            marker=markers[idx % len(markers)], 
            s=80, 
            edgecolors='black'
        )

    # 軸ラベル
    plt.xlabel("$f_1$ [min]")
    plt.ylabel("$f_2$ [min]")

    # 軸範囲を設定
    plt.ylim(10, 24)

    # 軸目盛りを整数に設定
    plt.yticks(np.arange(11, 24, 2))  # Y軸の目盛りを10から24まで2刻みで設定

    # 凡例
    plt.legend(loc="best")
    plt.tight_layout()
    plt.show()

# メイン処理
directory_path = "../../data/sbx/"  # ディレクトリのパス
file_pattern = "eta*.csv"          # 読み込むファイルのパターン

# etaの指定方法を手動で設定する場合（Trueなら手動指定）
manual_eta = True  # 手動でetaを設定する場合はTrue、それ以外は自動設定
if manual_eta:
    # 手動で指定するetaの値（リスト）
    eta_values = [1, 20]
    final_generation_data = get_final_generation_data(directory_path, file_pattern, eta_values=eta_values)
else:
    print("Eta range specification is not supported for this script.")
    final_generation_data = {}

# 最初のファイルから第0世代のデータを取得
first_file = sorted(glob.glob(os.path.join(directory_path, file_pattern)))[0]
initial_data = get_initial_generation_data(first_file)

# 散布図を描画
plot_generation_scatter(initial_data, final_generation_data)
