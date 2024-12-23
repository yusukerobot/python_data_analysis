import pandas as pd

# 元のCSVファイルのパス
input_file_path = '../../data/raw/data2.csv'

# 新しいCSVファイルのパス
output_file_path = '../../data/pareto2.csv'

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
            temp_data = [current_generation, "f1,f2"]
            i += 1
        elif line == "f1,f2,first_soc,front":
            # データブロックの開始
            header = line.split(",")
            i += 1
            while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith("第"):
                values = lines[i].strip().split(",")
                if len(values) == len(header):  # ヘッダーと同じ長さの行のみ処理
                    front_index = header.index("front")
                    if values[front_index] == "0":
                        temp_data.append(f"{values[0]},{values[1]}")
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

# 実行
process_csv(input_file_path, output_file_path)

print(f"データの処理が完了しました。新しいCSVファイルは {output_file_path} に保存されています。")
