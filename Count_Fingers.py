import cv2
import time
import os
import HandTrackingModule as htm

wCam, hCam = 1980, 1080
cap = cv2.VideoCapture(0)

cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector()
tipIds = [4,8,12,16,20]
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        fingers = []

        #thumb
        if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1,5):
            #four fingers
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        print(fingers)
        totalFingers = fingers.count(1)
        cv2.putText(img, str(totalFingers), (100, 170), cv2.FONT_HERSHEY_PLAIN, 15, (0, 0, 255), 15)
    cv2.imshow("Finger Count", img)
    cv2.waitKey(1)
