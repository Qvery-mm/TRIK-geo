import cv2
import numpy as np
from sift_matcher import get_bounding_box

BOX_LEN_IN_PX = 50

pano = cv2.imread('data/pano/pano.jpg')

finish = cv2.imread('data/samples/finish.jpg')
box1 = cv2.imread('data/samples/box1.jpg')
box2 = cv2.imread('data/samples/box2.jpg')
tools = cv2.imread('data/samples/toolbox.jpg')


finish_bound = get_bounding_box(finish, pano)
box1_bound = get_bounding_box(box1, pano)
box2_bound = get_bounding_box(box2, pano)
toolbox_bound = get_bounding_box(tools, pano)


# Draw bounding box
img = cv2.polylines(pano, [finish_bound], True, (0,255,0),3, cv2.LINE_AA)
img = cv2.polylines(img, [box1_bound], True, (0,0,255),3, cv2.LINE_AA)
img = cv2.polylines(img, [box2_bound], True, (0,0,255),3, cv2.LINE_AA)
img = cv2.polylines(img, [toolbox_bound], True, (0,0,255),3, cv2.LINE_AA)


# ищем центр финиша
bound = finish_bound
center_x = np.sum([bound[0][0][0], bound[1][0][0], bound[2][0][0], bound[3][0][0]]) // 4
center_y = np.sum([bound[0][0][1], bound[1][0][1], bound[2][0][1], bound[3][0][1]]) // 4
print(center_x, center_y)

# масштабируем изображение до 1см/пиксель
p1 = toolbox_bound[0][0]
p2 = toolbox_bound[1][0]
p3 = toolbox_bound[2][0]

v1 = p1 - p2
v2 = p2 - p3
v3 = p1 - p3

l1 = np.linalg.norm(v1)
l2 = np.linalg.norm(v2)
l3 = np.linalg.norm(v3)

m = sorted([l1, l2, l3])[1]

factor = BOX_LEN_IN_PX / m




img = cv2.circle(img, (center_x, center_y), 5, (0, 255, 0), 4)

img = cv2.resize(img, (0, 0), fx=factor, fy=factor)
cv2.imwrite("data/maps/bounding_boxes.jpg", img)
cv2.imshow("result", img)

cv2.waitKey(5000)