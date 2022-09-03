import cv2
import mediapipe as mp
import time
import pyautogui
import math
import os
import ctypes

import sys

###########################
# Camera Height,width
############################
wcam, hcam = 480, 480
handNo = 0
draw = True
tipIds = [4, 8, 12, 16, 20]
t = True

xList = []
yList = []
bbox = []
############################

###########################
# Camera capture and hand recognition
############################
cam = cv2.VideoCapture(0)
cam.set(3, wcam)
cam.set(4, hcam)
ptime = 0
length2 =0
#
mpHands = mp.solutions.hands

hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=1,
                      min_detection_confidence=0.7,
                      min_tracking_confidence=0.7)
mpDraw = mp.solutions.drawing_utils
############################


#########################
# adding circles on landmarks and processing rgb
#########################
while True:
    success, img = cam.read()
    img = cv2.flip(img, 1)

    #img = detector.findHands(img)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # re = hands.process(imgRGB)
    # Drawing the circels and connecting the dots on the landmarks
    # imgRGB=detector.findHands(imgRGB)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                # print(id,lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # if id ==0:
                cv2.circle(img, (cx, cy), 3, (255, 0, 255), cv2.FILLED)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)


    lmlist = []
    if results.multi_hand_landmarks:
        myHand = results.multi_hand_landmarks[handNo]
        for id, lm in enumerate(myHand.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            xList.append(cx)
            yList.append(cy)

            lmlist.append([id, cx, cy])
            if draw:
                cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
        xmin, xmax = min(xList), max(xList)
        ymin, ymax = min(yList), max(yList)
        bbox = xmin, ymin, xmax, ymax
        ''' 
        if draw:
            cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20),
                          (0, 255, 0), 2)
    # print(lmlist,bbox)
        '''
    if len(lmlist) != 0:
        x1, y1 = lmlist[8][1:]
        x2, y2 = lmlist[12][1:]
        x3, y3 = lmlist[16][1:]
        x4, y4 = lmlist[20][1:]
        x5, y5 = lmlist[4][1:]
        # print(x1,y1,x2,y2)

    if len(lmlist) != 0:
        fingers = []
        for id in range(0, 5):
            if lmlist[tipIds[id]][2] < lmlist[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        #print(fingers)
        if len(lmlist) != 0:
            x1, y1 = lmlist[4][1], lmlist[4][2]
            x2, y2 = lmlist[8][1], lmlist[8][2]
            x3, y3 = lmlist[12][1], lmlist[12][2]
            x4, y4 = lmlist[16][1], lmlist[16][2]
            x5, y5 = lmlist[20][1], lmlist[20][2]

            length = math.hypot(x2 - x1, y2 - y1)
            length3 = math.hypot(x5 - x1, y5 - y1)
            length4 = math.hypot(x3 - x1, y3 - y1)
            length5 = math.hypot(x4 - x1, y4 - y1)
            #print(length)
            #print(length2)
            #print(length3)
            #print(length4)
        # next two lines pyautogui is not working, the camera is freezing

#############################
# Gestures
#############################
            # 1
            if fingers[1] == 1 and fingers[0] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[
                4] == 0:

                while t:

                    os.startfile("C:\Program Files\Microsoft Office\\root\Office16\WINWORD.EXE")
                    os.system("C:\Program Files\Microsoft Office\\root\Office16\WINWORD.EXE")
                    t = False
                # for ctrlz(cut)
            # 2
            elif fingers[1] == 1 and fingers[0] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[
                4] == 0 :

                while t:
                    pyautogui.hotkey('ctrlleft', 'x')
                    t = False

            # 4
            elif fingers[1] == 1 and fingers[0] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:

                while t:
                    pyautogui.hotkey('ctrlleft', 'a')
                    t = False
            # 5
            elif fingers[1] == 1 and fingers[0] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:

                while t:
                    pyautogui.hotkey('ctrlleft', 'v')
                    t = False
                # for altf4(closing)
            # 6
            15
            if fingers[1] == 0 and fingers[0] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                t = True

#####################

######################
# To show Fps and image tab
######################
    cTime = time.time()
    fps = 1 / (cTime - ptime)
    ptime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("image", img)
    cv2.waitKey(1)
######################