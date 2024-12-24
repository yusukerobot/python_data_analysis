import csv

# 元のCSVファイルのパス
input_file_path = '../../data/raw/data1.csv'

# 新しいCSVファイルのパス
output_file_path = '../../data/output_data.csv'

# 新しいCSVファイルを書き込むための準備
with open(output_file_path, 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    
    # 元のCSVファイルを読み込む
    with open(input_file_path, 'r') as input_file:
        reader = csv.reader(input_file)
        
        generation_counter = -1  # 世代カウンター
        generation_data = []  # 現在の世代のf1, f2データを格納するリスト
        in_generation = False  # 世代データが開始されたかを追跡

        for row in reader:
            if not row:
                continue  # 空行をスキップ

            # 行のデータが "f1,f2,first_soc,front" の場合
            if len(row) >= 4 and row[0] == 'f1' and row[1] == 'f2' and row[2] == 'first_soc' and row[3] == 'front':
                if in_generation:
                    # 現在の世代のデータがあれば、CSVに書き込む
                    writer.writerow([f"第{generation_counter}世代"])
                    writer.writerow(['f1', 'f2'])
                    writer.writerows(generation_data)  # 現世代のf1, f2データを一括で書き込む

                # 新しい世代の開始
                generation_counter += 1
                generation_data = []  # 現世代のデータをリセット
                in_generation = True  # 世代のデータが開始されたことを記録

            # "front" が 0 の行において f1 と f2 のデータを抽出
            elif len(row) >= 4 and row[3] == '0':
                # f1, f2の値を抽出
                f1 = float(row[0])
                f2 = float(row[1])
                
                # 現世代のデータリストにf1とf2を追加
                generation_data.append([f1, f2])

        # 最後の世代のデータをCSVに書き込む
        if generation_data:
            writer.writerow([f"第{generation_counter}世代"])
            writer.writerow(['f1', 'f2'])
            writer.writerows(generation_data)

print(f"データ処理が完了しました。新しいCSVファイルは {output_file_path} に保存されました。")
