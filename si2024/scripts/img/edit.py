import cv2
import numpy as np

# 画像を読み込む
image = cv2.imread('../../data/figure/dynamic_charging_path.png')

# BGRからHSVに変換（色を扱いやすくするため）
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# 検出したい色の範囲を定義（例: 赤色）
lower_bound = np.array([0, 100, 100])  # 色相(H), 彩度(S), 明度(V)の下限
upper_bound = np.array([10, 255, 255])  # 色相(H), 彩度(S), 明度(V)の上限

# 色範囲でマスクを作成
mask = cv2.inRange(hsv_image, lower_bound, upper_bound)

# 膨張処理で太くする
kernel = np.ones((4, 4), np.uint8)
dilated_mask = cv2.dilate(mask, kernel, iterations=1)

# 元の画像に色を強調して重ねる
highlighted_image = image.copy()
highlighted_image[dilated_mask > 0] = [0, 0, 255]  # 強調色（例: 赤）で塗る

# 結果を保存
cv2.imwrite('dynamic.png', highlighted_image)

# 結果を表示
cv2.imshow('Highlighted Image', highlighted_image)
# cv2.waitKey(0)
cv2.destroyAllWindows()
