import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

# 描画設定
plt.rcParams["font.family"] = "TeX Gyre Termes"
plt.rcParams['font.size'] = 40

width_cm = 16.5
height_cm = width_cm / 1.6
width_inch = width_cm * 2 / 2.54
height_inch = width_inch * 2 / 2.54

# パラメータ設定
etas = [1, 5, 10, 15, 20]  # etaの異なる値
u_values = np.linspace(0, 1, 500)  # uの値は0から1までの範囲で500分割
line_styles = ['-', '--', '-.', ':', '--']  # 異なる線のスタイル
colors = ['red', 'blue', 'green', 'orange', 'purple']  # 明るい色の設定
linewidth = 5  # 線の太さ

# グラフの描画
plt.figure(figsize=(8, 6))

# 異なるetaに対してデルタを計算
for i, eta in enumerate(etas):
    delta_values = np.piecewise(u_values, 
                                [u_values <= 0.5, u_values > 0.5],
                                [lambda u: (2*u)**(1/(eta+1)) - 1, 
                                 lambda u: 1 - (2*(1-u))**(1/(eta+1))])

    # 線のスタイルと色を変更
    plt.plot(u_values, delta_values, label=f'$\eta$ = {eta}', linestyle=line_styles[i], color=colors[i], linewidth=linewidth)

# グラフの設定
plt.xlabel('$u$')
plt.ylabel('$\delta$')
plt.legend(fontsize=32)
plt.grid(True)

# 縦軸の目盛りを小数点第1位までに設定
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

# グラフ表示
plt.show()
