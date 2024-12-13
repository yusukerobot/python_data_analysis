import numpy as np
import matplotlib.pyplot as plt

# グラフのフォントとサイズ設定
plt.rcParams["font.family"] = "TeX Gyre Termes"
plt.rcParams['font.size'] = 25

# グラフの寸法設定（cmからインチに変換）
width_cm = 14.5
height_cm = width_cm / 2.0
width_inch = width_cm / 2.54
height_inch = height_cm / 2.54

# SBX crossover function
def sbx_crossover(p1, p2, beta):
    c1 = 0.5 * ((1 + beta) * p1 + (1 - beta) * p2)
    c2 = 0.5 * ((1 - beta) * p1 + (1 + beta) * p2)
    return c1, c2

# 親の値とベータ値を定義
p1, p2 = 3, 7  # Parents
betas = [0.1, 0.5, 1, 1.5, 2]  # β values

# 各ベータ値に対する子を生成
children = {}
for beta in betas:
    c1, c2 = sbx_crossover(p1, p2, beta)
    children[beta] = (c1, c2)

# プロットのセットアップ
plt.figure(figsize=(width_inch, height_inch))
plt.axhline(0, color='gray', linewidth=1.0)  # 数直線の基準線

# 親を点線でプロット
plt.axvline(p1, color='black', linestyle='--', linewidth=2.0, zorder=1)  # p1 の点線
plt.axvline(p2, color='black', linestyle='--', linewidth=2.0, zorder=1)  # p2 の点線

# 各ベータ値ごとに子をプロット
colors = ['red', 'blue', 'green', 'purple', 'orange']
markers = ['o', 's', '^', 'D', 'x']
for beta, color, marker in zip(betas, colors, markers):
    c1, c2 = children[beta]
    plt.scatter(c1, 0, color=color, marker=marker, label=rf'$\beta={beta}$', s=100, zorder=5)  # 点のサイズを大きく
    plt.scatter(c2, 0, color=color, marker=marker, s=100, zorder=5)  # 点のサイズを大きく

# プロットのカスタマイズ
plt.xlim(0, 10)  # 数直線の範囲を [0, 10] に設定
plt.xlabel('Offspring Value', loc='center', labelpad=20)  # 横軸ラベルを中央に
plt.yticks([])  # Y軸の目盛りを非表示に
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.show()
