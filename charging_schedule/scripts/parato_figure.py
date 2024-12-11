import matplotlib.pyplot as plt
import csv

# グラフのフォントとサイズ設定
plt.rcParams["font.family"] = "TeX Gyre Termes"
plt.rcParams['font.size'] = 35
width_cm = 14.5
height_cm = width_cm / 1.6
width_inch = width_cm * 2 / 2.54
height_inch = width_inch * 2 / 2.54

# CSVファイルの読み込み
file_path = "../data/p1.csv"  # 実際のCSVファイルのパスを指定してください

# データ格納用の辞書
generations = {}
current_generation = None

# CSVを解析
with open(file_path, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        if row[0].startswith("第") and "世代" in row[0]:
            current_generation = row[0]
            generations[current_generation] = []
        elif row[0].lower() == "f1":  # ヘッダ行はスキップ
            continue
        elif current_generation and len(row) == 2:
            f1, f2 = map(float, row)
            generations[current_generation].append((f1, f2))

# プロットの作成
plt.figure(figsize=(width_inch, height_inch))

for i, (generation, points) in enumerate(generations.items()):
    f1, f2 = zip(*points)
    if i == 2:  # 第1世代（青丸）
        plt.scatter(f1, f2, edgecolor='blue', label=generation, s=100)
    elif i == len(generations) - 1:  # 最終世代（赤丸）
        plt.scatter(f1, f2, edgecolor='red', label=generation, s=100)
    else:  # その他の世代（黒丸塗りつぶしなし）
        plt.scatter(f1, f2, edgecolor='black', facecolors='none', label=generation, s=100)

plt.xlabel("f1 [min]")
plt.ylabel("f2 [min]")
# plt.xlim(145, 147)
# plt.ylim(10, 30)
plt.grid(True)
plt.show()
