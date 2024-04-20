import pickle
import math
import cv2
import numpy as np
from PIL import Image
from scipy.ndimage.filters import gaussian_filter

# 1 pixel per cm
with open('../data/maps/map.pickle', 'rb') as handle:
    black_map = pickle.load(handle)

with open('../data/maps/gradients.pickle', 'rb') as handle:
    gradients = pickle.load(handle)

rad = 180 / math.pi

vec = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 305, 292, 281, 280, 282, 284, 286, 289, 292, 294, 297, 300, 304, 307, 311, 315, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 117, 115, 115, 114, 114, 113, 113, 113, 112, 112, 112, 112, 112, 111, 111, 111, 111, 111, 111, 111, 112, 112, 112, 112, 112, 113, 113, 113, 115, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 126, 124, 123, 121, 120, 118, 117, 116, 115, 113, 112, 111, 110, 109, 108, 108, 109, 110, 114, 120, 126, 132, 140, 148, 157, 168, 180, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

points = []
X = []
Y = []
rad = 180 / math.pi

FACTOR = 1.72
THETA = math.pi
for i in range(0, 360):
    phi = i / rad
    dist = vec[i] / FACTOR
    if dist == 0 or dist > 200:
        continue
    x1 = int(dist * math.cos(phi))
    y1 = int(dist * math.sin(phi))
    X.append(x1)
    Y.append(y1)
    points.append((y1, x1))

x_max, x_min = max(X), min(X)
y_max, y_min = max(Y), min(Y)


img = np.zeros((y_max - y_min + 1, x_max - x_min + 1))
for point in points:
    img[point[0] - y_min, point[1] - x_min] = 255

img = cv2.blur(img,(5,5))
img = cv2.blur(img,(5,5))
# img = cv2.GaussianBlur(img,(5,5),1)
# img = cv2.GaussianBlur(img,(5,5),1)
ret, img = cv2.threshold(img, 0.1, 255, cv2.THRESH_BINARY)
# print(img.shape)
# gray = np.float32(img)
# dst = cv2.cornerHarris(gray,2,7,0.01)
# # result is dilated for marking the corners, not important
# dst = cv2.dilate(dst, None)
# print(dst.shape)
#
# # Threshold for an optimal value, it may vary depending on the image.
# img[dst > 0.1 * dst.max()] = 0.5
#
img = np.uint8(img)
# cv2.imshow("img", img)
# cv2.waitKey(10000)

lsd = cv2.createLineSegmentDetector(1)


print(img.shape)
lines = lsd.detect(img)[0] # [0] # Position 0 of the returned tuple are the detected lines
print(lines)
drawn_img = lsd.drawSegments(img,lines)
cv2.imshow("LSD",drawn_img )

cv2.waitKey(10000)
