import matplotlib.pyplot as plt
import pandas as pd

# CSVファイルのパス
file_path = '../data/c1.csv'  # 実際のファイルパスに合わせてください

# ファイルを読み込む
with open(file_path, 'r') as f:
    lines = f.readlines()

# 親集団と子集団の行を分割
parents_data = []
children_data = []
is_parent = False

for line in lines:
    # "parents" または "children" ラベルを見つけたらその後のデータを格納
    if 'parents' in line:
        is_parent = True
        continue  # 親集団のラベルをスキップ
    elif 'children' in line:
        is_parent = False
        continue  # 子集団のラベルをスキップ

    # f1, f2 のデータを格納
    # ヘッダー行（f1, f2）をスキップ
    if ',' in line:
        # ヘッダー行をスキップ
        if 'f1' not in line:
            columns = line.strip().split(',')
            if len(columns) > 2:
                columns = columns[:2]  # 最初の2列のみを残す
            if is_parent:
                parents_data.append(','.join(columns))
            else:
                children_data.append(','.join(columns))

# 親集団と子集団のデータフレームを作成
# f1, f2 の列をカンマで分割して DataFrame に変換
df_parent = pd.DataFrame([list(map(float, item.split(','))) for item in parents_data], columns=['f1', 'f2'])
df_child = pd.DataFrame([list(map(float, item.split(','))) for item in children_data], columns=['f1', 'f2'])

# プロット
# plt.figure(figsize=(8, 6))

# 親集団（黒丸）
plt.scatter(df_parent['f1'], df_parent['f2'], color='black', label='Parents', marker='o')

# 子集団（赤丸）
plt.scatter(df_child['f1'], df_child['f2'], color='red', label='Children', marker='o')

# グラフのラベル設定
plt.xlabel('f1')
plt.ylabel('f2')
plt.title('Parent and Child Populations (f1 vs f2)')

# 凡例を表示
plt.legend()

# 表示
plt.grid(True)
plt.show()
