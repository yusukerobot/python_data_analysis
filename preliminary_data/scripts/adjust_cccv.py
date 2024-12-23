import pandas as pd

# 入力ファイルと出力ファイルのパス
input_file = '../data/raw/cc-cv.csv'
output_file = '../data/adjust_cc-cv.csv'

# CSVファイルを読み込む
data = pd.read_csv(input_file, delimiter=',')  # デリミタがタブであることを想定
data.columns = [col.strip() for col in data.columns]  # 列名の空白を除去

# 必要な列が存在しているかを確認
required_columns = {'ElapsedTime(s)', 'Battery(%)'}
if not required_columns.issubset(data.columns):
    raise ValueError(f"Input file must contain the following columns: {required_columns}")

# 結果を格納するリスト
processed_rows = []

# バッテリー状態をトラックするための変数
charging = False

for i in range(1, len(data)):
    prev_battery = data['Battery(%)'].iloc[i - 1]
    current_battery = data['Battery(%)'].iloc[i]

    # バッテリーが増加し始めたら充電モードに切り替え
    if not charging and current_battery > prev_battery:
        charging = True
        processed_rows.append(data.iloc[i - 1].copy())  # 増加直前の行を保持

    # バッテリーが減少し始めたら充電モードを終了
    elif charging and current_battery < prev_battery:
        charging = False
        processed_rows.append(data.iloc[i - 1].copy())  # 減少直前の行を保持

    # 充電中のデータを記録
    if charging:
        row = data.iloc[i].copy()
        elapsed_diff = (data['ElapsedTime(s)'].iloc[i] - data['ElapsedTime(s)'].iloc[i - 1]) / 60
        battery_diff = current_battery - prev_battery
        charge_rate = battery_diff / elapsed_diff if elapsed_diff != 0 else None
        row['ChargeRate(%/min)'] = charge_rate
        processed_rows.append(row)

# 抽出したデータを新しいDataFrameに変換
processed_data = pd.DataFrame(processed_rows)

# 最初の行の充電速度はなし
processed_data.loc[processed_data.index[0], 'ChargeRate(%/min)'] = None

# 新しいCSVファイルに書き出し
processed_data.to_csv(output_file, index=False)

print(f"Processed data saved to {output_file}")
