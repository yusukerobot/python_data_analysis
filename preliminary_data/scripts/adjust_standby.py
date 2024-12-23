import pandas as pd

# 入力CSVファイルパス
input_file = '../data/raw/standby.csv'
output_file = '../data/adjust_standby.csv'

# CSVファイルを読み込む
data = pd.read_csv(input_file)

# 必要な列を確認
if not {'ElapsedTime(s)', 'Battery(%)'}.issubset(data.columns):
    raise ValueError("Input file must contain 'ElapsedTime(s)' and 'Battery(%)' columns")

# データを整理
processed_data = []
last_time = None  # 最後に抽出した時間を追跡
previous_battery = None

for index, row in data.iterrows():
    current_time = row['ElapsedTime(s)']
    current_battery = row['Battery(%)']

    # 最初の行は無条件に抽出
    if last_time is None:
        processed_data.append([current_time, current_battery, None])  # 最初は充電速度なし
        last_time = current_time
        previous_battery = current_battery
        continue

    # 60秒以上経過した行を抽出
    if current_time - last_time >= 60:
        # 充電速度を計算 (%/min)
        charge_rate = (previous_battery - current_battery) / ((current_time - last_time) / 60)

        # 新しい行を追加
        processed_data.append([current_time, current_battery, charge_rate])

        # 時間とバッテリー値を更新
        last_time = current_time
        previous_battery = current_battery

# データフレームとして整理
processed_df = pd.DataFrame(processed_data, columns=['ElapsedTime(s)', 'Battery(%)', 'ChargeRate(%/min)'])

# 結果をCSVファイルに書き込む
processed_df.to_csv(output_file, index=False)

print(f"Processed data saved to: {output_file}")
