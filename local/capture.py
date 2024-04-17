import cv2
from local import panorama

camera = cv2.VideoCapture(0)
ret, pano = camera.read()
for i in range(200):
    print(i)
    try:
        ret, frame = camera.read()
        new = panorama.makePano(pano, frame)
        cv2.imshow("out", new)
        pano = new
    except Exception as e:
        print(e)
        print("Skipping frame")
    cv2.waitKey(1)
del(camera)