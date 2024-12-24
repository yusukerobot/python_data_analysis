import matplotlib.pyplot as plt

# CSVファイルのパス
input_file_path = '../data/pareto2.csv'

# 描画設定
plt.rcParams["font.family"] = "TeX Gyre Termes"
plt.rcParams['font.size'] = 30

# グラフサイズの設定
width_cm = 14.5
height_cm = width_cm / 1.6
width_inch = width_cm * 2 / 2.54
height_inch = width_inch * 2 / 2.54

def plot_generations(input_file_path):
    # データの読み込み
    with open(input_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    data = {}
    current_generation = None

    # データを世代ごとに分けて辞書に保存
    for line in lines:
        line = line.strip()
        if line.startswith("第") and "世代" in line:
            # 新しい世代を開始
            current_generation = line
            data[current_generation] = {"f1": [], "f2": []}
        elif line and current_generation and "," in line:
            # データ行のチェック
            if line.lower().startswith("f1,f2"):  # ヘッダー行をスキップ
                continue
            try:
                f1, f2 = map(float, line.split(","))
                data[current_generation]["f1"].append(f1)
                data[current_generation]["f2"].append(f2)
            except ValueError:
                continue  # 数値に変換できない行をスキップ

    # グラフの作成
    plt.figure(figsize=(width_inch, height_inch))

    generations = list(data.keys())
    for idx, (generation, values) in enumerate(data.items()):
        if generation == generations[0]:  # 初期世代
            plt.scatter(values["f1"], values["f2"], color='blue', marker='x', label=generation, linewidths=2, s=100)
        elif generation == generations[-1]:  # 最終世代
            plt.scatter(values["f1"], values["f2"], color='red', marker='o', label=generation, linewidths=2, s=100)
        # else:  # 中間世代
        #     plt.scatter(values["f1"], values["f2"], color='black', marker='o', facecolors='none', linewidths=2, s=100)

    # ラベルの設定
    plt.xlabel("f1 [min]")
    plt.ylabel("f2 [min]")
    plt.tight_layout()

    # グラフの表示
    plt.show()

# 実行
plot_generations(input_file_path)
