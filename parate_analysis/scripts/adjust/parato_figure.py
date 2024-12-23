import csv
import matplotlib.pyplot as plt

# 入力CSVファイルと出力CSVファイルのパス
input_file = '../../data/data1_first_end_pareto.csv'  # 入力CSVファイル名
output_file = '../../data/pareto_data.csv'  # 出力CSVファイル名

# 変数の準備
data_0th_gen = []  # 第0世代のデータ
data_100th_gen = []  # 第100世代のデータ

# CSVを読み込みデータを処理
with open(input_file, newline='') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)  # ヘッダー行をスキップ
    
    current_gen = None
    temp_data = []

    for row in reader:
        # 'f1', 'f2', 'first_soc', 'front' の行が来たとき
        if len(row) == 4 and row[0] not in ['f1', 'f2', 'first_soc', 'front']:  # ヘッダーを除く
            try:
                # f1, f2のデータを保存
                temp_data = [float(row[0]), float(row[1])]
            except ValueError:
                # 'time'などの無効なデータ行をスキップ
                continue
        # 'time' という文字列が来たとき
        elif row[0] == 'time' and temp_data:
            # 世代の判定がまだであれば
            if current_gen is None:
                # 最初に出てくるデータで世代を判定
                if float(temp_data[0]) > 100:
                    current_gen = 100
                else:
                    current_gen = 0
            # 世代ごとにデータを分ける
            if current_gen == 0:
                data_0th_gen.append(temp_data)
            elif current_gen == 100:
                data_100th_gen.append(temp_data)
            temp_data = []  # 次のデータに備えてリセット

# 新しいCSVファイルに書き込む
with open(output_file, mode='w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # ヘッダーの書き込み
    writer.writerow(['f1', 'f2'])
    # 第0世代のデータを書き込む
    for item in data_0th_gen:
        writer.writerow(item)
    # 第100世代のデータを書き込む
    for item in data_100th_gen:
        writer.writerow(item)

# プロット
plt.figure(figsize=(8, 6))
# 第0世代はxでプロット
plt.scatter([item[0] for item in data_0th_gen], [item[1] for item in data_0th_gen], c='blue', label='0th Generation', marker='x')
# 第100世代は丸でプロット
plt.scatter([item[0] for item in data_100th_gen], [item[1] for item in data_100th_gen], c='red', label='100th Generation', marker='o')

# グラフのラベル
plt.title('f1 vs f2 for Generations')
plt.xlabel('f1')
plt.ylabel('f2')
plt.legend()
plt.grid(True)

# プロットを表示
plt.show()
