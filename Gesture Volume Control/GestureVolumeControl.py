import cv2
import mediapipe as mp
import time
import numpy as np
import HandTrackingModule as htm
import math
import pycaw
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


ptime=0
vol=0
volbar=400
volper=0
cap = cv2.VideoCapture(0)

detector= htm.handDetector(detectionCon=0.55)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volrange = volume.GetVolumeRange()


minvol= volrange[0]
maxvol = volrange[1]

while True:
    suc, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2] # tip of thumb
        x2, y2 = lmList[8][1], lmList[8][2] # tip of index
        cx,cy = (x1 + x2)//2, (y1 + y2)//2

        cv2.circle(img, (x1, y1), 10, (255, 0, 244), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 244), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (254,0,244), 4)
        cv2.circle(img, (cx,cy), 7, (230,0,215), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        # print(length)

        # Hand Range - 50 -> 320
        # Volume Range - -96 -> 0

        vol = np.interp(length, [50,300], [minvol,maxvol])
        volbar = np.interp(length, [50, 300], [400, 150])
        volper = np.interp(length, [50, 300], [0, 100])
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length< 50:
            cv2.circle(img, (cx,cy), 7, (0,235,5), cv2.FILLED)



    cv2.rectangle(img, (50, 150), (85, 400), (45, 9, 23), 4)
    cv2.rectangle(img, (50, int(volbar)), (85, 400), (45, 9, 23), cv2.FILLED)
    cv2.putText(img, f'{int(volper)}%', (40,450),
                cv2.FONT_HERSHEY_COMPLEX, 1,
                (154,29,199), 2)
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime

    cv2.putText(img, f'FPS:{int(fps)}', (20,70),
                cv2.FONT_HERSHEY_COMPLEX, 1,
                (124,21,189), 3)
    cv2.imshow("image",img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



