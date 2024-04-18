import numpy as np
import cv2
from matplotlib import pyplot as plt

img1 = cv2.imread('data/samples/box2.jpg') # queryImage
img2 = cv2.imread('data/pano/pano.jpg') # trainImage
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
# Initiate SIFT detector
sift = cv2.xfeatures2d.SIFT_create()
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)

# BFMatcher with default params
bf = cv2.BFMatcher()
matches = bf.knnMatch(des1, des2, k=2)
# Apply ratio test
good = []
for m,n in matches:
  if m.distance < 0.9*n.distance:
    good.append([m])
# cv2.drawMatchesKnn expects list of lists as matches.
print(good)

# src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1, 1, 2)
# dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1, 1, 2)
# M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
# print(M)
# print(mask)


img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,img2,flags=2)
plt.imshow(img3),plt.show()
cv2.waitKey(5000)



# Initiate SIFT detector
# orb = cv2.ORB_create()
#
# # find the keypoints and descriptors with ORB
# kp1, des1 = orb.detectAndCompute(img1,None)
# kp2, des2 = orb.detectAndCompute(img2,None)

# create BFMatcher object
# bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Match descriptors.
# matches = bf.match(des1,des2)

# Sort them in the order of their distance.
# matches = sorted(matches, key = lambda x:x.distance)

# good_matches = matches[:10]
#
# src_pts = np.float32([ kp1[m.queryIdx].pt for m in good_matches]).reshape(-1,1,2)
# dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good_matches ]).reshape(-1,1,2)
M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
matchesMask = mask.ravel().tolist()
h,w = img1.shape[:2]
pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)

dst = cv2.perspectiveTransform(pts,M)
dst += (w, 0)  # adding offset

draw_params = dict(matchColor = (0,255,0), # draw matches in green color
               singlePointColor = None,
               matchesMask = matchesMask, # draw only inliers
               flags = 2)


img3 = cv2.drawMatches(img1,kp1,img2,kp2,good, None,**draw_params)

# Draw bounding box in Red
img3 = cv2.polylines(img3, [np.int32(dst)], True, (0,0,255),3, cv2.LINE_AA)

cv2.imshow("result", img3)
cv2.waitKey(10000)
# or another option for display output
#plt.imshow(img3, 'result'), plt.show()