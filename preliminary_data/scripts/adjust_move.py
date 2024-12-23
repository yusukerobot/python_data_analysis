import pandas as pd

# 入力ファイルと出力ファイルのパス
input_file = '../data/raw/Bcs_data.csv'
output_file = '../data/adjust_Bcs_data.csv'

# CSVファイルを読み込む
data = pd.read_csv(input_file)

# 必要な列が存在しているかを確認
required_columns = {'DistanceRemaining', 'ElapsedTime(s)', 'Battery(%)'}
if not required_columns.issubset(data.columns):
    raise ValueError(f"Input file must contain the following columns: {required_columns}")

# 結果を格納するリスト
selected_rows = []

# 最初の行を初期値として追加
start_index = 0

for i in range(1, len(data)):
    # `DistanceRemaining`の値が5.0以上増加したかどうかを判定
    if data['DistanceRemaining'].iloc[i] - data['DistanceRemaining'].iloc[i - 1] > 5.0:
        # 塊の最初と最後の行を取得
        start_row = data.iloc[start_index].copy()
        end_row = data.iloc[i - 1]
        
        # 時間差とバッテリー差を計算して新しい列として追加
        elapsed_time_diff = end_row['ElapsedTime(s)'] - start_row['ElapsedTime(s)']
        battery_diff = start_row['Battery(%)'] - end_row['Battery(%)']
        
        start_row['ElapsedTimeDiff(s)'] = elapsed_time_diff
        start_row['BatteryDiff(%)'] = battery_diff
        
        # 塊の行をリストに追加
        selected_rows.append(start_row)
        selected_rows.append(end_row)
        
        # 新しい塊の開始インデックスを設定
        start_index = i

# 最後の塊を処理
start_row = data.iloc[start_index].copy()
end_row = data.iloc[-1]

elapsed_time_diff = end_row['ElapsedTime(s)'] - start_row['ElapsedTime(s)']
battery_diff = end_row['Battery(%)'] - start_row['Battery(%)']

start_row['ElapsedTimeDiff(s)'] = elapsed_time_diff
start_row['BatteryDiff(%)'] = battery_diff

selected_rows.append(start_row)
selected_rows.append(end_row)

# 新しいデータフレームを作成
new_data = pd.DataFrame(selected_rows).drop_duplicates()

# 新しいCSVファイルに書き出し
new_data.to_csv(output_file, index=False)

print(f"Processed data with time differences and battery differences saved to {output_file}")
