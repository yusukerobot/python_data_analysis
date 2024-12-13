import numpy as np
import matplotlib.pyplot as plt

# グラフのフォントとサイズ設定
plt.rcParams["font.family"] = "TeX Gyre Termes"  # フォント設定
plt.rcParams['font.size'] = 35  # フォントサイズ設定

# グラフの寸法設定（cmからインチに変換）
width_cm = 14.5  # 幅の設定（cm）
height_cm = width_cm / 1.6  # 高さを幅の1.6倍に設定
width_inch = width_cm * 2 / 2.54  # cmからインチに変換
height_inch = width_inch * 2 / 2.54  # cmからインチに変換

# 親の遺伝子の値（p1, p2）
p1 = 0.5
p2 = 0.7

# 異なるetaの値
eta_values = [5, 10, 20, 50, 100]  # etaの異なる値

# uの範囲（0.1から1までの範囲）
u_values = np.linspace(0.1, 1, 100)

# グラフのサイズを設定
plt.figure(figsize=(width_inch, height_inch))  # 指定されたサイズで設定

# 異なるetaに対してc1, c2を計算してプロット
for i, eta in enumerate(eta_values):
    c1_values = []
    c2_values = []
    
    for u in u_values:
        # SBXの計算（簡単化した式）
        c1 = 0.5 * (p1 + p2) - 0.5 * (p2 - p1) * np.cos(np.pi * u)**(1 / (eta + 1))
        c2 = 0.5 * (p1 + p2) + 0.5 * (p2 - p1) * np.cos(np.pi * u)**(1 / (eta + 1))
        
        c1_values.append(c1)
        c2_values.append(c2)
    
    # 子個体c1, c2の遺伝子（色付き破線）
    plt.plot(u_values, c1_values, linestyle='--', color=plt.cm.viridis(i / len(eta_values)), linewidth=2, label=f'c1, η={eta}')
    plt.plot(u_values, c2_values, linestyle='--', color=plt.cm.viridis(i / len(eta_values)), linewidth=2, label=f'c2, η={eta}')
    
# 親の遺伝子p1, p2（黒実線）
plt.axhline(p1, color='black', linestyle='-', linewidth=3, label='p1 (parent)')
plt.axhline(p2, color='black', linestyle='-', linewidth=3, label='p2 (parent)')

# グラフのタイトルとラベル
plt.xlabel(r'$u$', fontsize=35)
plt.ylabel(r'Gene values ($c1$, $c2$, $p1$, $p2$)', fontsize=35)
plt.grid(True)
plt.legend(fontsize=20, loc='best')

plt.show()
