import pandas as pd

# CSVファイルを読み込む
file_path = '../data/goal_monitoring_data.csv'  # CSVファイルのパス
data = pd.read_csv(file_path)

# 経過時間、バッテリー充電率を取得
time = data['Accumulated Time [min]']
battery = data['Battery [%]']

# 各行の時間差を計算
time_diff = time.diff().fillna(0)  # 最初の行のdiffはNaNなので0で埋める

# 条件に基づく時間を計算
time_above_80 = time_diff[battery >= 80].sum()  # バッテリー充電率80%以上の時間
time_below_20 = time_diff[battery <= 20].sum()  # バッテリー充電率20%以下の時間
total_time = time_above_80 + time_below_20

# 結果を出力
print(f"バッテリー充電率が80%以上の総稼働時間: {time_above_80:.2f} 分")
print(f"バッテリー充電率が20%以下の総稼働時間: {time_below_20:.2f} 分")
print(f"上記条件の合計時間: {total_time:.2f} 分")
