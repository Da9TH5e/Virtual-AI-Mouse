import cv2
import time
import numpy as np
import HandTrackingModule as htm
import pyautogui

wCam, hCam = 1280, 720
frameRed = 100
smooth = 4

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0
pLocX, pLocY = 0, 0
cLocX, cLocY = 0, 0

detector = htm.handDetector(maxHands=1)
wScr, hScr = pyautogui.size()
print(wScr, hScr)

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    
    if len(lmList)!= 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        x4, y4 = lmList[16][1:]
        
        #print(x1, y1, x2, y2)
        
        fingers = detector.fingersUp()
        #print(fingers)
        cv2. rectangle(img, (frameRed, frameRed), 
                        (wCam - frameRed, hCam - frameRed),
                        (255, 0, 255), 1)
        
        if fingers[1]==1 and fingers[2]==0:
            
            cv2. rectangle(img, (frameRed, frameRed), (wCam - frameRed, hCam - frameRed), (255, 0, 255))
            x3 = np.interp(x1, (frameRed, wCam - frameRed), (0, wScr))
            y3 = np.interp(y1, (frameRed, hCam - frameRed), (0, hScr))
            
            cLocX = pLocX + (x3 - pLocX) / smooth
            cLocY = pLocY + (y3 - pLocY) / smooth

            pyautogui.moveTo(wScr-cLocX, cLocY)
            pLocX, pLocY = cLocX, cLocY

        elif fingers[1]==1 and fingers[2]==1:
            length, img, infoLine = detector.findDistance(8, 12, img)
            #print(length)
            
            if length < 35:
                cv2.line(img, (infoLine[4], infoLine[5]), 
                            (x2, y2), (0, 0, 255), 2)
                pyautogui.click()
                time.sleep(1)

            elif y1 < pLocY:
                pyautogui.scroll(20)
            
            elif y1 > pLocY:
                pyautogui.scroll(-20)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)