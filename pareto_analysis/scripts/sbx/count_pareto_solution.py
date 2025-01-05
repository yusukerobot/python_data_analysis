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

# CSVファイルの最終世代データをカウントする関数
def count_final_generation_data(directory_path, eta_min, eta_max, eta_step):
    eta_values = range(eta_min, eta_max + 1, eta_step)
    eta_counts = {}

    for eta in eta_values:
        file_pattern = f"eta{eta}.csv"
        file_path = os.path.join(directory_path, file_pattern)

        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
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
        
        # 最終世代のデータをカウント（重複排除）
        unique_data = set(data)
        eta_counts[eta] = len(unique_data)

    return eta_counts

# グラフプロット関数
def plot_pareto_solution_counts(eta_counts):
    eta_values = sorted(eta_counts.keys())
    data_counts = [eta_counts[eta] for eta in eta_values]
    
    # 折れ線グラフの描画
    plt.figure(figsize=(width_inch, height_inch))
    plt.plot(eta_values, data_counts, marker='o', color='blue', label='Number of pareto solutions', linewidth=2, markersize=10)

    # 軸ラベルとタイトル
    plt.xlabel('$\eta$')
    plt.ylabel('Number of pareto solutions')
    
    # x軸ラベルを回転して表示
    plt.xticks(rotation=0)
    
    # レイアウト調整
    plt.tight_layout()
    plt.show()

# メイン処理
directory_path = "../../data/sbx/"  # ディレクトリのパス

# ηの範囲を指定
eta_min = 10  # 最小値
eta_max = 50  # 最大値
eta_step = 10 # ステップ数

# 最終世代データのカウント
eta_counts = count_final_generation_data(directory_path, eta_min, eta_max, eta_step)

# カウント結果を表示
for eta, count in sorted(eta_counts.items()):
    print(f"$\eta$ = {eta}: {count} unique data points")

# 結果をプロット
plot_pareto_solution_counts(eta_counts)
