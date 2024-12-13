import numpy as np
import matplotlib.pyplot as plt

# グラフのフォントとサイズ設定
plt.rcParams["font.family"] = "TeX Gyre Termes"  # フォント設定
plt.rcParams['font.size'] = 30  # フォントサイズ設定

# グラフの寸法設定（cmからインチに変換）
width_cm = 14.5  # 幅の設定（cm）
height_cm = width_cm / 1.6  # 高さを幅の1.6倍に設定
width_inch = width_cm * 2 / 2.54  # cmからインチに変換
height_inch = width_inch * 2 / 2.54  # cmからインチに変換

# etaの範囲
eta_values = np.linspace(1, 100, 100)  # etaの範囲を1から100まで100個の点で設定

# 異なるuの値
u_values = [0.1, 0.3, 0.5, 0.7, 0.9]

# 色と線の種類を指定
colors = ['r', 'g', 'black', 'm', 'blue']  # 色のリスト
linestyles = ['-', '--', ':', '-.', '-']  # 線のスタイルのリスト

# グラフのサイズを設定
plt.figure(figsize=(width_inch, height_inch))  # 指定されたサイズで設定

# 異なるuに対してβを計算してプロット
for i, u in enumerate(u_values):
    beta_values = []
    for eta in eta_values:
        if u <= 0.5:
            beta = (2 * u) ** (1 / (eta + 1))  # u <= 0.5 の場合
        else:
            beta = (1 / (2 * (1 - u))) ** (1 / (eta + 1))  # u > 0.5 の場合
        beta_values.append(beta)
    
    # プロット（色と線種を指定）
    plt.plot(eta_values, beta_values, label=f'$u$ = {u}', color=colors[i], linestyle=linestyles[i], linewidth=3)

# グラフのタイトルとラベル
plt.xlabel(r'$\eta$', fontsize=35)
plt.ylabel(r'$\beta$', fontsize=35)
plt.grid(True)
plt.legend(fontsize=30)
plt.show()
