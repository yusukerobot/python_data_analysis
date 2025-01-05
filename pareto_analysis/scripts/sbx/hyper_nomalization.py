import os
import pandas as pd
import glob
import matplotlib.pyplot as plt
import numpy as np

# 描画設定
plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams["font.family"] = "TeX Gyre Termes"  # フォント設定
plt.rcParams['font.size'] = 30

# グラフサイズの設定
width_cm = 14.5
height_cm = width_cm / 1.6
width_inch = width_cm / 2.54
height_inch = height_cm / 2.54

# データの読み込みと整形
def load_csv_files_by_eta_range(directory_path, eta_min, eta_max, eta_step):
    """
    指定されたetaの範囲でCSVファイルを読み込みます。
    """
    datasets = {}
    eta_values = range(eta_min, eta_max + 1, eta_step)
    
    for eta in eta_values:
        file_name = f"eta{eta}.csv"
        file_path = os.path.join(directory_path, file_name)
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue
        
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
            
            current_generation = None
            for line in lines:
                line = line.strip()
                if line.startswith("第"):  # 世代名の検出
                    current_generation = line
                    datasets.setdefault(file_path, {}).setdefault(current_generation, [])
                elif line and not any(c.isalpha() for c in line):  # 数値データ
                    try:
                        valid_data = list(map(float, line.split(',')))
                        datasets[file_path][current_generation].append(valid_data)
                    except ValueError:
                        continue
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    
    # 各世代のデータをDataFrameに変換
    for file, generations in datasets.items():
        for gen, data in generations.items():
            datasets[file][gen] = pd.DataFrame(data, columns=["f1", "f2", "time_count"])
    
    return datasets

# ハイパーボリュームの計算
def calculate_hypervolume(points, reference_point):
    points = np.array(points)
    points = points[np.lexsort(np.rot90(points))]  # ソート
    points = np.vstack([points, reference_point])  # 参照点を追加

    hypervolume = 0.0
    prev = reference_point[0]
    for i in range(len(points) - 1, -1, -1):
        hypervolume += (prev - points[i, 0]) * (reference_point[1] - points[i, 1])
        prev = points[i, 0]

    return hypervolume

# 正規化関数の定義
def normalize(df, f1_min, f1_max, f2_min, f2_max):
    df["f1"] = (df["f1"] - f1_min) / (f1_max - f1_min)
    df["f2"] = (df["f2"] - f2_min) / (f2_max - f2_min)
    return df

# グラフプロット用の設定
def plot_combined_hypervolume(hv_data, line_width=3):
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    linestyles = ['--', '-.', ':', '--', '-.', ':']

    sorted_hv_data = dict(sorted(hv_data.items(), key=lambda item: int(item[0].split('=')[-1].strip())))

    for idx, (label, hv_changes) in enumerate(sorted_hv_data.items()):
        plt.plot(
            range(len(hv_changes)), hv_changes, 
            linestyle=linestyles[idx % len(linestyles)],
            color=colors[idx % len(colors)],
            label=label,
            linewidth=line_width
        )

    plt.xlabel("Generation")
    plt.ylabel("Hypervolume")
    plt.legend(loc="best")
    plt.tight_layout()
    plt.show()

# メイン処理
directory_path = "../../data/sbx/"  # CSVファイルが格納されているディレクトリのパス

# etaの範囲を指定
eta_min = 10  # 最小値
eta_max = 50  # 最大値
eta_step = 10  # ステップ数

# データ読み込み
datasets = load_csv_files_by_eta_range(directory_path, eta_min, eta_max, eta_step)

# f1, f2の最小値と最大値を計算
global_f1_min = float('inf')
global_f2_min = float('inf')
global_f1_max = float('-inf')
global_f2_max = float('-inf')

for file, generations in datasets.items():
    for gen, df in generations.items():
        global_f1_min = min(global_f1_min, df["f1"].min())
        global_f2_min = min(global_f2_min, df["f2"].min())
        global_f1_max = max(global_f1_max, df["f1"].max())
        global_f2_max = max(global_f2_max, df["f2"].max())

print(f"f1 最小値: {global_f1_min} 最大値: {global_f1_max}")
print(f"f2 最小値: {global_f2_min} 最大値: {global_f2_max}")

# 参照点の設定
reference_point = [1, 1]

# 各ファイルのハイパーボリュームを計算
hv_data = {}
for file, generations in datasets.items():
    print(f"Processing file: {file}")
    hv_changes = []
    for gen, df in generations.items():
        df_normalized = normalize(df, global_f1_min, global_f1_max, global_f2_min, global_f2_max)
        hv = calculate_hypervolume(df_normalized[["f1", "f2"]].to_numpy(), reference_point)
        hv_changes.append(hv)
    
    eta_number = os.path.basename(file).replace(".csv", "").replace("eta", "").strip()
    label = f"$\eta$ = {eta_number}"
    hv_data[label] = hv_changes

# ハイパーボリューム変化をプロット
plot_combined_hypervolume(hv_data)
