import os
import pandas as pd

# 元のCSVファイルがあるディレクトリ
input_directory = '../../data/raw/mutation/'

# 新しいCSVファイルを保存するディレクトリ
output_directory = '../../data/mutation/'

def process_csv(input_path, output_path):
    # 新しいCSV内容を保存するリスト
    output_data = []

    with open(input_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    current_generation = None
    temp_data = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("第") and "世代" in line:
            # 現在の世代を記録
            if temp_data:
                output_data.append(temp_data)
            current_generation = line
            temp_data = [current_generation, "f1,f2,time_count"]  # f1, f2, time_countをヘッダに追加
            i += 1
        elif line == "f1,f2,first_soc,front":
            # データブロックの開始
            header = line.split(",")
            i += 1
            while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith("第"):
                values = lines[i].strip().split(",")
                if len(values) == len(header):  # ヘッダーと同じ長さの行のみ処理
                    front_index = header.index("front")
                    if values[front_index] == "0":  # frontが0のデータのみ
                        # f1, f2の値を追加
                        f1_f2 = f"{values[0]},{values[1]}"
                        # timeの要素数をカウント
                        time_count = 0
                        i += 1
                        while i < len(lines) and lines[i].strip() == "time":
                            time_count += len(lines[i+1].strip().split(","))
                            i += 2  # 次の行に移動（socと次のtimeを処理）
                        # 出力データにf1, f2, time_countを追加
                        temp_data.append(f"{f1_f2},{time_count}")
                    else:
                        i += 1
                else:
                    i += 1
        else:
            i += 1

    if temp_data:
        output_data.append(temp_data)

    # 新しいCSVファイルを書き出す
    with open(output_path, 'w', encoding='utf-8') as file:
        for block in output_data:
            for line in block:
                file.write(line + "\n")
            file.write("\n")

# ディレクトリ内のすべてのCSVファイルを処理
def process_all_csv_files(input_directory, output_directory):
    # ディレクトリ内のファイルを取得
    for filename in os.listdir(input_directory):
        if filename.endswith('.csv') and filename.startswith('eta'):
            input_file_path = os.path.join(input_directory, filename)
            output_file_path = os.path.join(output_directory, filename)

            # CSV処理を実行
            process_csv(input_file_path, output_file_path)

            print(f"処理が完了しました: {filename}")

# 実行
process_all_csv_files(input_directory, output_directory)

print(f"すべてのCSVファイルの処理が完了しました。")
