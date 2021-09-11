import cv2
import HandTrackingModule as htm
import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]



wCam, hCam = 1980,1080

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4,hCam)
detector = htm.handDetector(detectionCon=0.8)
while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=False)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        x1,y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx,cy = (x1+x2)//2 , (y1+y2)//2
        cv2.circle(img, (x1,y1), 5, (255,0,255) , cv2.FILLED)
        cv2.circle(img, (x2, y2), 5, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (255,0,0),3)
        length = math.hypot(x2-x1, y2-y1)
        vcl = np.interp(length, [3,100], [minVol,maxVol])
        print(vcl)
        volume.SetMasterVolumeLevel(vcl, None)






    cv2.imshow("image", img)
    cv2.waitKey(1)
#100 and 3