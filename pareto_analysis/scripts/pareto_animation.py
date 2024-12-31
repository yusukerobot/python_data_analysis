import matplotlib.pyplot as plt
import matplotlib.animation as animation

# CSVファイルのパス
input_file_path = '../data/pareto1.csv'

# 描画設定
plt.rcParams["font.family"] = "TeX Gyre Termes"  # Change to a font that supports a wide range of characters
plt.rcParams['font.size'] = 25

# グラフサイズの設定
width_cm = 14.5
height_cm = width_cm / 1.6
width_inch = width_cm * 2 / 2.54
height_inch = width_inch * 2 / 2.54

# プロットの設定（点のサイズ、線の太さを変更可能）
scatter_size = 80  # 散布図の点のサイズ
line_width = 2      # 線の太さ

def parse_csv(input_file_path):
    """CSVファイルを解析し、世代ごとのデータを返す"""
    with open(input_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    data = {}
    current_generation = None

    for line in lines:
        line = line.strip()
        if line.startswith("第") and "世代" in line:
            # 新しい世代を開始
            current_generation = line
            data[current_generation] = {"f1": [], "f2": []}  # f1, f2のみ追加
        elif line and current_generation and "," in line:
            if line.lower().startswith("f1,f2"):  # ヘッダー行をスキップ
                continue
            try:
                values = list(map(float, line.split(",")))
                f1, f2 = values[0], values[1]  # f1とf2だけ使用
                data[current_generation]["f1"].append(f1)
                data[current_generation]["f2"].append(f2)
            except ValueError:
                continue  # 数値に変換できない行をスキップ
    return data

def animate_generations(data):
    """世代データをアニメーション表示する"""
    fig, ax = plt.subplots(figsize=(width_inch, height_inch))

    generations = list(data.keys())
    initial_gen = generations[0]
    final_gen = generations[-1]

    # 初期世代と最終世代のf1, f2の最小値と最大値を取得
    min_f1 = min(min(data[initial_gen]["f1"]), min(data[final_gen]["f1"]))
    max_f1 = max(max(data[initial_gen]["f1"]), max(data[final_gen]["f1"]))
    min_f2 = min(min(data[initial_gen]["f2"]), min(data[final_gen]["f2"]))
    max_f2 = max(max(data[initial_gen]["f2"]), max(data[final_gen]["f2"]))

    # グラフの範囲を設定（f1は最小値0にする）
    ax.set_xlim(min_f1 - 1, max_f1 + 1)  # f1の範囲
    ax.set_ylim(min_f2 - 0.5, max_f2 + 1)  # f2の範囲
    ax.set_xlabel("$f_1$ [min]")
    ax.set_ylabel("$f_2$ [min]")  # 軸ラベルの設定

    # 初期世代を青丸で表示（点のサイズを変更）枠線は黒に設定
    scat_initial = ax.scatter(data[initial_gen]["f1"], data[initial_gen]["f2"],
                               color='blue', label=f'Initial Generation', s=scatter_size, edgecolors='black')

    # 現在の世代の散布図（初期状態は空）
    scat_current, = ax.plot([], [], 'o', color='black', markerfacecolor='none', markersize=scatter_size // 10, lw=line_width)

    # 最終世代用の散布図（初期状態は空）枠線は黒に設定
    scat_final = ax.scatter([], [], color='red', s=scatter_size, edgecolors='black')  # 最初は凡例なし

    # 凡例の位置を右上に設定
    ax.legend(loc='upper right')

    def update(frame):
        # 初期世代は常に表示されるようにする
        scat_initial.set_offsets(list(zip(data[initial_gen]["f1"], data[initial_gen]["f2"])))

        if frame == 0:
            # 初期世代のみ表示（変更なし）
            return scat_initial, scat_current

        elif frame < len(generations):
            # 現在の世代を黒丸で一時的に表示
            current_gen = generations[frame]
            scat_current.set_data(data[current_gen]["f1"], data[current_gen]["f2"])

            # 現在の世代の凡例ラベルを設定
            scat_current.set_label(f'Generation: {frame}')  # 英語で「Generation X」を表示

            # 凡例を更新
            ax.legend(loc='upper right')

            return scat_initial, scat_current

        elif frame == len(generations):
            # 最終世代を赤丸で表示
            current_gen = final_gen
            scat_final.set_offsets(list(zip(data[current_gen]["f1"], data[current_gen]["f2"])))

            # 最終世代の凡例ラベルを設定
            scat_final.set_label(f'Generation: {frame - 1}')  # 最終世代のみ表示

            # 現在の世代の凡例ラベルを削除
            scat_current.set_label('')

            # 凡例を更新
            ax.legend(loc='upper right')

            return scat_initial, scat_final

    # アニメーションの作成
    ani = animation.FuncAnimation(
        fig, update, frames=len(generations) + 1, interval=150, blit=True, repeat=False  # repeat=Falseで最終世代で停止
    )

    # アニメーションを保存する場合
    ani.save("generations_animation.mp4", writer="ffmpeg", dpi=200)  # Make sure ffmpeg is installed

    plt.show()

# メイン処理
data = parse_csv(input_file_path)
animate_generations(data)
