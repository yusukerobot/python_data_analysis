import matplotlib.pyplot as plt
import pandas as pd

# CSVファイルのパス
input_file_path = '../data/sbx_test.csv'

# 描画設定
plt.rcParams["font.family"] = "TeX Gyre Termes"  # 広範囲の文字をサポートするフォントに変更
plt.rcParams['font.size'] = 25

# グラフサイズの設定
width_cm = 14.5
height_cm = width_cm / 1.6
width_inch = width_cm * 2 / 2.54
height_inch = width_inch * 2 / 2.54

# CSVファイルの読み込みと整形
try:
    # 空行を区切りとして世代ごとに分割
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 世代ごとのデータをリスト化
    generations = content.strip().split('\n\n')

    # データフレームの作成
    data = []
    for generation_data in generations:
        lines = generation_data.strip().split('\n')
        generation_label = lines[0]  # 世代ラベル
        header = lines[1].split(',')  # ヘッダー
        for line in lines[2:]:
            f1, f2 = map(float, line.split(','))
            data.append({'Generation': generation_label, 'f1': f1, 'f2': f2})

    df = pd.DataFrame(data)

    # グラフ描画
    plt.figure(figsize=(width_inch, height_inch))
    
    # 第0世代は黒バツ
    first_gen_data = df[df["Generation"] == "第0世代"]
    plt.scatter(first_gen_data['f1'], first_gen_data['f2'], c='black', marker='x', label="第0世代")
    
    # その他の世代は丸
    for generation in df["Generation"].unique():
        if generation != "第0世代":
            gen_data = df[df["Generation"] == generation]
            plt.scatter(gen_data['f1'], gen_data['f2'], label=generation)
    
    plt.title("f1 vs f2 Scatter Plot by Generation")
    plt.xlabel("f1")
    plt.ylabel("f2")
    plt.grid(True)
    plt.legend(title="Generation")
    plt.show()

except FileNotFoundError:
    print("CSVファイルが見つかりませんでした。パスを確認してください。")
except Exception as e:
    print(f"エラーが発生しました: {e}")
