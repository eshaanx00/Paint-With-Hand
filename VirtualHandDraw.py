import cv2
import mediapipe
import HandTracker as htm
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detector = htm.HandDetector()

xp,yp = 0,0
imageCanvas = np.zeros((720,1280,3),np.uint8)

while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    img = detector.drawHands(img=img)

    lmlist=detector.findPosition(img=img,draw=False)
    if(len(lmlist))!=0:
        #print(lmlist)

        x1,y1 = lmlist[8][1:]
        x2,y2 = lmlist[12][1:]

        fingers = detector.fingerUp()
        #print(fingers)
        if fingers[1] and fingers[2]:
            xp,yp = 0,0
            #print("Normal")
            cv2.rectangle(img,(x1,y1-25),(x2,y2+45),(255,255,0),cv2.FILLED)

        if fingers[1] and fingers[2] == False and fingers[0]==False:
            #print("Draw")
            cv2.circle(img,(x1,y1),15,(57,255,20),cv2.FILLED)
            if xp == 0and yp == 0:
                xp,yp = x1,y1

            cv2.line(imageCanvas,(xp,yp),(x1,y1),(57,255,20),10)

            xp,yp = x1,y1
        if fingers[1] and fingers[0]:
            #print("Draw")
            cv2.circle(img,(x1,y1),15,(0,0,0),cv2.FILLED)
            if xp == 0and yp == 0:
                xp,yp = x1,y1
            cv2.line(imageCanvas,(xp,yp),(x1,y1),(0,0,0),40)
            xp,yp = x1,y1

    imgGray = cv2.cvtColor(imageCanvas,cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img,imgInv)
    img = cv2.bitwise_or(img,imageCanvas)

    cv2.imshow("Image",img)
    #cv2.imshow("Canvas",imageCanvas)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break