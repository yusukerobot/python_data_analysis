import os
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# 描画設定
plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams["font.family"] = "TeX Gyre Termes"
plt.rcParams['font.size'] = 30

# グラフサイズの設定
width_cm = 16.5
height_cm = width_cm / 1.6
width_inch = width_cm / 2.54
height_inch = height_cm / 2.54

# CSVファイルの最終世代データをカウントする関数
def count_final_generation_data(directory_path, eta_values):
    eta_counts = {}

    for eta in eta_values:
        file_pattern = f"eta{eta}.csv"
        file_path = os.path.join(directory_path, file_pattern)

        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            eta_counts[eta] = 0  # データが見つからない場合は0に設定
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
def plot_pareto_solution_counts(eta_counts, eta_values, y_min=None, y_max=None, y_step=None):
    eta_values_sorted = sorted(eta_counts.keys())
    data_counts = [eta_counts[eta] for eta in eta_values_sorted]
    
    # 折れ線グラフの描画
    plt.figure(figsize=(width_inch, height_inch))
    plt.plot(eta_values_sorted, data_counts, marker='o', color='blue', label='Number of pareto solutions', linewidth=2, markersize=10)

    # 軸ラベルとタイトル
    plt.xlabel('$\eta$')
    plt.ylabel('Number of pareto solutions')
    
    # x軸の目盛りを指定したetaの値で表示
    plt.xticks(eta_values, rotation=0)
    
    # y軸の目盛りを整数に設定
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

    # y軸の範囲を指定する（手動設定の場合）
    if y_min is not None and y_max is not None:
        plt.ylim(y_min, y_max)
    
    # y軸の目盛りのステップ数を指定（y_stepがNoneでない場合）
    if y_step is not None:
        plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True, prune='lower', steps=[y_step]))
    
    # 自動設定の場合はy軸の範囲をデータに基づいて設定
    elif y_min is None and y_max is None:
        plt.ylim(min(data_counts) - 10, max(data_counts) + 10)

    # レイアウト調整
    plt.tight_layout()
    plt.show()

# メイン処理
directory_path = "../../data/mutation/"  # ディレクトリのパス

# ηの範囲を指定
eta_values_manual = [1, 5, 10, 15, 20]  # 手動で指定するetaの値のリスト

manual = True  # 手動設定する場合はTrue、CSVから自動取得する場合はFalse

if manual:
    # 手動でetaの値を設定
    eta_values = eta_values_manual
else:
    # 自動で計算する場合
    eta_min = 1
    eta_max = 20
    eta_step = 1
    eta_values = range(eta_min, eta_max + 1, eta_step)

# 自動で各etaに対してデータのカウントを実行
eta_counts = count_final_generation_data(directory_path, eta_values)

# 最終世代データのカウント結果を表示
for eta, count in sorted(eta_counts.items()):
    print(f"$\eta$ = {eta}: {count} unique data points")

# 最小値、最大値、ステップを設定して結果をプロット
y_min = 69  # y軸の最小値 (Noneの場合自動設定)
y_max = 150  # y軸の最大値 (Noneの場合自動設定)
y_step = 5  # y軸のステップ (指定する場合)

plot_pareto_solution_counts(eta_counts, eta_values, y_min, y_max, y_step)
