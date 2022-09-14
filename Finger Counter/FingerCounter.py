import cv2
import os
import mediapipe as mp
import HandTrackingModule as htm

cap = cv2.VideoCapture(0)

folderpath = "FingerImages"
mylist = os.listdir(folderpath)
print(mylist)

overlaylist =[]
for impath in mylist:
    image = cv2.imread(f'{folderpath}/{impath}')
    overlaylist.append(image)
#print(len(overlaylist))

detector = htm.handDetector(detectionCon=0.65)
tipids = [4, 8, 12, 16, 20]

while True:
    suc, img = cap.read()
    img = detector.findHands(img,draw=False)

    lmList = detector.findPosition(img,draw=False)
    # print(lmList)
    if len(lmList) != 0:
        fingers = []
        #thumb
        if lmList[4][1] > lmList[3][1]: # for right hand only
            fingers.append(1)
        else:
            fingers.append(0)
        # other fingers
        for id in range(1,5):
            if lmList[tipids[id]][2] <= lmList[tipids[id]-1][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        # print(fingers)

        totalFingers = fingers.count(1)
        # print(totalFingers)
        h, w, c = overlaylist[totalFingers-1 ].shape
        img[0:h, 0:w] = overlaylist[totalFingers-1]

        cv2.rectangle(img, (20,225), (170,425), (129,205,234), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (45,375), cv2.FONT_HERSHEY_COMPLEX,5,
                    (237,89,120),10)

    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

