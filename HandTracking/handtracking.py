import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands= mpHands.Hands(False)
mpDraw = mp.solutions.drawing_utils

pTime=0
cTime=0

while True:
    success, img = cap.read()
    # Converting the image to RGB as required
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:
            for id,lm in enumerate(handlms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                print(id, cx, cy)
                # if id == 0:
                #     cv2.circle(img,(cx,cy), 15, (255,0,255), cv2.FILLED)
            mpDraw.draw_landmarks(img, handlms, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10,60), cv2.FONT_HERSHEY_PLAIN,3, (102,123,155), 3)

    cv2.imshow("image", img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break


