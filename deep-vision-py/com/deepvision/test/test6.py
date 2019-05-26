# 2018.01.17 20:39:17 CST
# 2018.01.17 20:50:35 CST
import numpy as np
import cv2

from com.deepvision.util.displayutil import displayImageOutput, draw_multiple_points

img = cv2.imread("D:\\github-repos\\dream-projects\\deep-vision-py\\DATA\\robot.jpg")
# pts = np.array([[10, 150], [150, 100], [300, 150], [350, 100], [310, 20], [35, 10]])
# pts = np.array([[100, 300], [400, 300], [400, 100], [100, 100]])
pts = np.array([[100, 300], [400, 300], [250, 100]])
xpoint = [100, 400, 250]
ypoint = [300, 300, 100]
draw_multiple_points(xpoint, ypoint, "fghd")

## (1) Crop the bounding rect
rect = cv2.boundingRect(pts)
x, y, w, h = rect
croped = img[y:y + h, x:x + w].copy()

## (2) make mask
pts = pts - pts.min(axis=0)

mask = np.zeros(croped.shape[:2], np.uint8)
cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)

## (3) do bit-op
dst = cv2.bitwise_and(croped, croped, mask=mask)

## (4) add the white background
bg = np.ones_like(croped, np.uint8) * 255
cv2.bitwise_not(bg, bg, mask=mask)
dst2 = bg + dst

cv2.imwrite("croped.png", croped)
cv2.imwrite("mask.png", mask)
cv2.imwrite("dst.png", dst)
cv2.imwrite("dst2.png", dst2)

displayImageOutput(main_img=img, main_img_title="main_image", result_img=dst2,
                   result_img_title="result_image", title="Triangle Cropping")
