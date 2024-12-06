import pandas as pd

# 入力CSVファイルのパス
input_file = "../data/overview_data/selected_data_static.csv"
# 出力CSVファイルのパス
output_file = "../data/12-5/static-original.csv"

# CSVファイルを読み込む
df = pd.read_csv(input_file)

# 指定列を変換
columns_to_transform = ['battery [Wh]', 'B short', 'B charg', 'short total cons [wh]', 'charg total cons [wh]']
for col in columns_to_transform:
    df[col] = (df[col] / 19.98) * 100

# 4列目と5列目を再計算
df['P short'] = df['B short'] / df['C short']  # 4列目の計算
df['P charg'] = df['B charg'] / df['C charg']  # 5列目の計算

# 値を丸める
for col in df.select_dtypes(include=['float']).columns:
    df[col] = df[col].round(2)

# 変換後のデータを新しいCSVファイルに保存
df.to_csv(output_file, index=False)

print(f"変換後のデータを {output_file} に保存しました。")
