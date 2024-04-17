import numpy as np
import cv2
from matplotlib import pyplot as plt

img1 = cv2.imread('data/samples/box1.jpg') # queryImage
img2 = cv2.imread('data/pano/pano.jpg') # trainImage
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
# Initiate SIFT detector
sift = cv2.xfeatures2d.SIFT_create()
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)

# BFMatcher with default params
bf = cv2.BFMatcher()
matches = bf.knnMatch(des1,des2, k=2)
# Apply ratio test
good = []
for m,n in matches:
  if m.distance < 0.75*n.distance:
    good.append([m])
# cv2.drawMatchesKnn expects list of lists as matches.
img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,img2,flags=2)
plt.imshow(img3),plt.show()