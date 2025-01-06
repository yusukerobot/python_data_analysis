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

# uの範囲を0から1に設定
u = np.linspace(0, 1, 500)

# いくつかのetaの値
eta_values = [5, 10, 20, 50]

# グラフのサイズを設定
plt.figure(figsize=(width_inch, height_inch))  # 指定されたサイズで設定

# 各etaに対するbetaを計算してプロット
for eta in eta_values:
    beta = np.where(u <= 0.5, (2 * u) ** (1 / (eta + 1)), (1 / (2 * (1 - u))) ** (1 / (eta + 1)))
    
    # etaに基づいて色と線種を変更
    if eta == 5:
        color = 'r'  # 赤
        linestyle = '--'  # 破線
    elif eta == 10:
        color = 'g'  # 緑
        linestyle = ':'  # 点線
    elif eta == 20:
        color = 'b'  # 青
        linestyle = '-'  # 実線
    elif eta == 50:
        color = 'm'  # マゼンタ
        linestyle = '-.'  # 一点差線

    # プロット
    plt.plot(u, beta, label=f'$\eta$ = {eta}', color=color, linestyle=linestyle, linewidth=3)

# グラフのタイトルとラベル
plt.xlabel('$u$', fontsize=35)
plt.ylabel(r'$\beta$', fontsize=35)
plt.grid(True)
plt.legend(fontsize=30)

plt.show()
