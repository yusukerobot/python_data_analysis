import pandas as pd

# 入力CSVファイルのパス
input_file = "../data/12-5/static-original.csv"
# 出力CSVファイルのパス
output_file = "../data/12-5/static.csv"

# CSVファイルを読み込む
df = pd.read_csv(input_file)

# 結果を格納するリスト
rows_to_extract = []

# 前回のtask [times]の値を追跡
prev_task = None
extracting = False  # `task`の間にデータを抽出するかどうかを管理

# データフレームを1行ずつ処理
for index, row in df.iterrows():
    current_task = row['task [times]']
    
    # taskが切り替わった時
    if current_task != prev_task:
        # 新しいtaskの開始前に、条件が合致する行を抽出する
        extracting = True  # 新しいtaskの間は抽出を始める
        prev_task = current_task  # prev_taskを現在のtaskに更新

    # C shortが8.6〜8.9の範囲にある場合に行を抽出
    if extracting and 8.6 <= row['C short'] <= 8.9:
        rows_to_extract.append(row)  # 該当する行をリストに追加
        extracting = False  # 次のtaskが始まるまで抽出を停止

# 結果をデータフレームに変換
extracted_df = pd.DataFrame(rows_to_extract)

# 新しいCSVファイルに保存
extracted_df.to_csv(output_file, index=False)

print(f"抽出したデータを {output_file} に保存しました。")
