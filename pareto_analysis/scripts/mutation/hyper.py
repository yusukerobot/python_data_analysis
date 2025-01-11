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
width_cm = 16.5
height_cm = width_cm / 1.6
width_inch = width_cm / 2.54
height_inch = height_cm / 2.54

# データの読み込みと整形
def load_multiple_csv_files(directory_path, eta_values=None, min_eta=None, max_eta=None, step=1, file_pattern="eta*.csv"):
    """
    指定されたディレクトリ内のファイルパターンに一致するCSVファイルを読み込みます。
    - eta_values: 手動で指定したeta値のリスト
    - min_eta: 読み込む最小eta値
    - max_eta: 読み込む最大eta値
    - step: 読み込むetaの間隔
    """
    file_paths = glob.glob(os.path.join(directory_path, file_pattern))
    datasets = {}

    # eta値の決定
    if eta_values is not None:
        valid_etas = set(eta_values)
    elif min_eta is not None and max_eta is not None:
        valid_etas = set(range(min_eta, max_eta + 1, step))
    else:
        valid_etas = None  # 範囲を指定しない場合

    for file_path in file_paths:
        try:
            # ファイル名からeta値を取得
            eta_number = int(os.path.basename(file_path).replace("eta", "").replace(".csv", "").strip())
            if valid_etas is not None and eta_number not in valid_etas:
                continue  # 範囲外の場合スキップ

            # ファイル全体を行単位で読み込む
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
    """
    ハイパーボリュームを計算します。
    - points: パレートフロントの点群
    - reference_point: 参照点
    """
    points = np.array(points)
    points = points[np.lexsort(np.rot90(points))]  # ソート
    points = np.vstack([points, reference_point])  # 参照点を追加

    hypervolume = 0.0
    prev = reference_point[0]
    for i in range(len(points) - 1, -1, -1):
        hypervolume += (prev - points[i, 0]) * (reference_point[1] - points[i, 1])
        prev = points[i, 0]

    return hypervolume

# グラフプロット用の設定
def plot_combined_hypervolume(hv_data, line_width=4):
    """
    複数ファイルのハイパーボリューム変化を1つのグラフにまとめてプロットします。
    - hv_data: ファイル名とハイパーボリューム変化の辞書
    - line_width: 線の太さ（デフォルトは3）
    """
    # 論文でよく使われる色
    colors = ['red', 'blue', 'green', 'orange', 'purple', '#8c564b']
    linestyles = ['-', '--', '-.', '--', '-.', '--']

    # etaの数値を基にファイル名をソート（etaの数字が小さい順）
    sorted_hv_data = dict(sorted(hv_data.items(), key=lambda item: int(item[0].split('=')[-1].strip())))

    for idx, (label, hv_changes) in enumerate(sorted_hv_data.items()):
        plt.plot(
            range(len(hv_changes)), hv_changes, 
            linestyle=linestyles[idx % len(linestyles)],
            color=colors[idx % len(colors)],
            label=label,
            linewidth=line_width  # 線の太さを指定
        )

    plt.xlabel("Generation")
    plt.ylabel("Hypervolume [$\mathrm{min}^2$]")

    # 任意で指定した横軸の目盛り
    custom_xticks = [1, 20, 40, 60, 80, 100]  # ここで希望する目盛りを指定
    plt.xticks(custom_xticks)  # 横軸の目盛りをカスタマイズ

    plt.legend(loc="best")
    plt.tight_layout()
    plt.show()

# メイン処理
directory_path = "../../data/mutation/"  # CSVファイルが格納されているディレクトリのパス

# etaの指定方法を手動で設定する場合（Trueなら手動指定）
manual_eta = True  # 手動でetaを設定する場合はTrue、それ以外は自動設定
if manual_eta:
    # 手動で指定するetaの値（リスト）
    eta_values = [1, 5, 10, 15, 20]
    datasets = load_multiple_csv_files(directory_path, eta_values=eta_values)
else:
    # 自動でetaの範囲を指定
    min_eta = 1  # 最小のeta値
    max_eta = 20  # 最大のeta値
    step = 1      # ステップサイズ
    datasets = load_multiple_csv_files(directory_path, min_eta=min_eta, max_eta=max_eta, step=step)

# すべてのデータから共通の参照点を計算（最初に計算し、計算後は変更しない）
global_f1_max = float('-inf')
global_f2_max = float('-inf')

# 各ファイルの最大f1, f2値を計算
for file, generations in datasets.items():
    for gen, df in generations.items():
        global_f1_max = max(global_f1_max, df["f1"].max())
        global_f2_max = max(global_f2_max, df["f2"].max())

# 参照点を固定（計算後に変更しない）
reference_point = [global_f1_max + 1, global_f2_max + 1]
reference_point = [140, 50]
print(f"Reference Point: {reference_point}")  # 参照点を出力

# 各ファイルのハイパーボリュームを計算
hv_data = {}
for file, generations in datasets.items():
    print(f"Processing file: {file}")
    hv_changes = []
    for gen, df in generations.items():
        hv = calculate_hypervolume(df[["f1", "f2"]].to_numpy(), reference_point)
        hv_changes.append(hv)
    
    # ファイル名からetaの値を抽出してラベルに使用
    eta_number = os.path.basename(file).replace(".csv", "").replace("eta", "").strip()
    label = f"$\eta$ = {eta_number}"
    hv_data[label] = hv_changes

# ハイパーボリューム変化をプロット
plot_combined_hypervolume(hv_data)
