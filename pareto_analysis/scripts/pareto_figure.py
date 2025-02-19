import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np

# CSVファイルのパス
input_file_path = '../data/sbx/eta1.csv'

# 描画設定
plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams["font.family"] = "TeX Gyre Termes"
plt.rcParams['font.size'] = 55

# グラフサイズの設定
width_cm = 16.5
height_cm = width_cm / 1.6
width_inch = width_cm * 2 / 2.54
height_inch = width_inch * 2 / 2.54

# データ読み取り関数
def read_generations(input_path):
    generations = {}
    with open(input_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    current_generation = None
    current_data = []
    for line in lines:
        stripped = line.strip()

        # 空行またはヘッダー行（f1,f2,time_count）をスキップ
        if not stripped or stripped.startswith("f1"):
            continue

        # 世代の開始（"第"が含まれる行）
        if stripped.startswith("第") and "世代" in stripped:
            if current_generation and current_data:
                generations[current_generation] = pd.DataFrame(
                    current_data, columns=["f1", "f2", "time_count"]
                )
            current_generation = stripped
            current_data = []
        elif ',' in stripped:
            # f1, f2, time_countの値をfloatに変換して追加
            values = stripped.split(",")
            try:
                f1, f2, time_count = map(float, values)
                current_data.append([f1, f2, time_count])
            except ValueError as e:
                # 数値変換エラー時に警告を表示
                print(f"データ読み取りエラー: {stripped}（エラー内容: {e}）")

    # 最後の世代も追加
    if current_generation and current_data:
        generations[current_generation] = pd.DataFrame(
            current_data, columns=["f1", "f2", "time_count"]
        )

    return generations

# プロット関数
def plot_generations(generations):
    initial_generation_label = list(generations.keys())[0]
    final_generation_label = list(generations.keys())[-1]

    initial_generation = generations[initial_generation_label]
    final_generation = generations[final_generation_label]

    # グラフ1: 初期世代を黒、最終世代を赤でプロット
    plt.figure(figsize=(width_inch, height_inch))
    plt.scatter(initial_generation["f1"], initial_generation["f2"],
                color='black', marker='x', label=f'Initial Generation',
                linewidths=2, s=80)  # 初期世代は黒のバツ
    plt.scatter(final_generation["f1"], final_generation["f2"],
                color='red', marker='o', label=f'Pareto Solution',
                linewidths=2, s=80, edgecolors='black')  # 最終世代は赤の丸
    plt.xlim(103, 118)
    plt.ylim(10, 24)
    plt.xlabel("$f_1$ [min]")
    plt.ylabel("$f_2$ [min]")
    # ax = plt.gca()
    # ax.xaxis.set_major_locator(MultipleLocator(2))

    # 軸目盛りを整数に設定
    plt.xticks(np.arange(103, 118, 4))  # Y軸の目盛りを10から24まで2刻みで設定
    plt.yticks(np.arange(11, 24, 4))  # Y軸の目盛りを10から24まで2刻みで設定
    plt.legend()
    plt.tight_layout()
    plt.show()

    # グラフ2: 初期世代と最終世代を time_count ごとに色分けしてプロット
    plt.figure(figsize=(width_inch, height_inch))
    colors = {1: 'red', 2: 'blue', 3: 'green'}
    labels = {1: "Charging number: 1", 2: "Charging number: 2", 3: "Charging number: 3"}
    markers = {1: 'o', 2: '^', 3: 'x'}

    # 最終世代のデータを time_count ごとに色分けしてプロット
    for time_val, group_data in final_generation.groupby("time_count"):
        # 色がない場合、デフォルト色（灰色）を使用
        color = colors.get(time_val, 'gray')
        plt.scatter(group_data["f1"], group_data["f2"],
                    color=color, label=f"{labels.get(time_val, 'Other')}",
                    marker=markers.get(time_val, 'o'), linewidths=2, s=80, edgecolors='black')
    
    plt.xlabel("$f_1$ [min]")
    plt.ylabel("$f_2$ [min]")
    # ax = plt.gca()
    # ax.xaxis.set_major_locator(MultipleLocator(2))
    # 軸範囲を設定
    plt.xlim(103, 118)
    plt.ylim(10, 24)

    # 軸目盛りを整数に設定
    plt.xticks(np.arange(103, 118, 4))  # Y軸の目盛りを10から24まで2刻みで設定
    plt.yticks(np.arange(11, 24, 4))  # Y軸の目盛りを10から24まで2刻みで設定
    plt.legend()
    plt.tight_layout()
    plt.show()

# 実行
generations = read_generations(input_file_path)
if generations:
    plot_generations(generations)
else:
    print("世代情報が見つかりません。データ形式を確認してください。")
