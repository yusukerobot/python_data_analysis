import csv

input_file_path = '../../data/raw/no_mutation_first_sbx.csv'
output_file_path = '../../data/sbx_test.csv'

def process_csv(input_path, output_path):
    output_data = []
    
    with open(input_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    current_generation = None
    temp_data = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("第") and "世代" in line:
            if temp_data:
                output_data.append(temp_data)
            current_generation = line
            temp_data = [current_generation, "f1,f2"]
            i += 1
        elif line == "f1,f2,first_soc,front":
            i += 1
            if i < len(lines):
                next_line = lines[i].strip().split(",")
                if len(next_line) >= 2:
                    temp_data.append(f"{next_line[0]},{next_line[1]}")
            i += 1
        else:
            i += 1
    
    if temp_data:
        output_data.append(temp_data)
    
    with open(output_path, 'w', encoding='utf-8') as file:
        for block in output_data:
            for line in block:
                file.write(line + "\n")
            file.write("\n")

# 実行
process_csv(input_file_path, output_file_path)

print(f"データの処理が完了しました。新しいCSVファイルは {output_file_path} に保存されています。")
