import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv

# グラフのフォントとサイズ設定
plt.rcParams["font.family"] = "TeX Gyre Termes"
plt.rcParams['font.size'] = 35
width_cm = 14.5
height_cm = width_cm / 1.6
width_inch = width_cm * 2 / 2.54
height_inch = width_inch * 2 / 2.54

# CSVファイルの読み込み
file_path = "../data/p7.csv"  # 実際のCSVファイルのパスを指定してください

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

# アニメーションの作成
fig, ax = plt.subplots(figsize=(width_inch, height_inch))

def animate(i):
    ax.clear()
    for j, (generation, points) in enumerate(generations.items()):
        f1, f2 = zip(*points)
        if j < i:  # 過去の世代は青で塗りつぶし
            ax.scatter(f1, f2, edgecolor='blue', facecolor='blue', label=generation if j == 0 else "", s=100)
        elif j == i:  # 現在の世代は赤で塗りつぶし
            ax.scatter(f1, f2, edgecolor='red', facecolor='red', label=generation if j == len(generations) - 1 else "", s=100)
    
    ax.set_xlabel("f1 [min]")
    ax.set_ylabel("f2 [min]")
   #  ax.grid(True)
   #  ax.legend()

# interval パラメータで描写時間を設定（ここでは500ミリ秒）
ani = animation.FuncAnimation(fig, animate, frames=len(generations), interval=500, repeat=False)
plt.show()
