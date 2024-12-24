import matplotlib.pyplot as plt
import csv

# CSVファイルのパス
input_file_path = '../data/pareto.csv'

# 描画設定
plt.rcParams["font.family"] = "TeX Gyre Termes"
plt.rcParams['font.size'] = 30

width_cm = 14.5
height_cm = width_cm / 1.6
width_inch = width_cm * 2 / 2.54
height_inch = width_inch * 2 / 2.54

# CSVファイルを読み込んでデータを抽出する関数
def read_data(input_file_path):
    generations = []
    f1_values = []
    f2_values = []
    
    with open(input_file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        current_generation = None
        
        for row in reader:
            # 空行をスキップ
            if not row:
                continue

            # 世代名が現れた場合
            if '世代' in row[0]:
                current_generation = row[0]  # 世代名を取得
            elif row[0] == 'f1':  # f1,f2行はスキップ
                continue
            else:
                try:
                    # f1, f2の値をリストに追加
                    f1 = float(row[0])
                    f2 = float(row[1])
                    f1_values.append(f1)
                    f2_values.append(f2)
                    generations.append(current_generation)  # それに対応する世代も追加
                except ValueError:
                    continue  # 数値でない場合はスキップ

    return generations, f1_values, f2_values

# データを読み込む
generations, f1_values, f2_values = read_data(input_file_path)

# 初期世代と最終世代のインデックスを特定
initial_generation = '第0世代'
final_generation = '第100世代'

# 初期世代と最終世代のデータを分ける
initial_gen_indices = [i for i, g in enumerate(generations) if g == initial_generation]
final_gen_indices = [i for i, g in enumerate(generations) if g == final_generation]

# 初期世代と最終世代のデータを抽出
initial_f1 = [f1_values[i] for i in initial_gen_indices]
initial_f2 = [f2_values[i] for i in initial_gen_indices]

final_f1 = [f1_values[i] for i in final_gen_indices]
final_f2 = [f2_values[i] for i in final_gen_indices]

# プロット
plt.figure(figsize=(width_inch, height_inch))

# 初期世代を黒いバツ（'x'）でプロット
plt.scatter(initial_f1, initial_f2, color='black', marker='x', s=30, linewidths=2, label=initial_generation)

# 最終世代を赤い丸（'o'）でプロット
plt.scatter(final_f1, final_f2, color='red', marker='o', edgecolor='red', facecolors='none', s=30, linewidths=2, label=final_generation)

# 軸ラベル
plt.xlabel('f1')
plt.ylabel('f2')

# グラフのタイトル
plt.title('Pareto Front of Generations')

# 凡例を表示
plt.legend()

# グリッドを表示
plt.grid(True)

# グラフの表示
plt.tight_layout()
plt.show()
