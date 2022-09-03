import math
import os
import sys
import time

import cv2
import face_recognition
import mediapipe as mp
import numpy as np
import pyautogui

###########################
# Camera Height,width
############################
wcam, hcam = 420, 420
handNo = 0
draw = True
tipIds = [4, 8, 12, 16, 20]
t = True
path = "C:\images"
images = []
classNames = []
mylist = os.listdir(path)
decide = bool

xList = []
yList = []
bbox = []
############################
print(mylist)
for cl in mylist:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)


###########################

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # for i in range(0, len(encodeList)):
        #     print(encodeList[i])
        try:
            encoded_face = face_recognition.face_encodings(img)[0]
        except IndexError as e:
            print(e)
            sys.exit(1)
        encodeList.append(encoded_face)
    return encodeList


encoded_face_train = findEncodings(images)
# Camera capture and hand recognition
############################
cam = cv2.VideoCapture(0)
cam.set(3, wcam)
cam.set(4, hcam)
ptime = 0

# detector=HandDetector(detectionCon=0.8)
mpHands = mp.solutions.hands

hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=1,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils
############################


#########################
# adding circles on landmarks and processing rgb
#########################
while True:
    success, img = cam.read()
    img = cv2.flip(img, 1)

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    faces_in_frame = face_recognition.face_locations(imgS)
    encoded_faces = face_recognition.face_encodings(imgS, faces_in_frame)
    cv2.imshow("image", img)
    for encode_face, faceloc in zip(encoded_faces, faces_in_frame):
        matches = face_recognition.compare_faces(encoded_face_train, encode_face)
        name = "Not Recognized"
        faceDist = face_recognition.face_distance(encoded_face_train,
                                                  encode_face)  # we are makeing the image with the shortest distance our image for face check
        matchIndex = np.argmin(faceDist)
        print(matchIndex)
        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            key = cv2.waitKey(1)
            if key ==81 or key == 113:
               break
            #####################

            ######################
            # To show Fps and image tab
            ######################
            cTime = time.time()
            fps = 1 / (cTime - ptime)
            ptime = cTime
            cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        # re = hands.process(imgRGB)
        # Drawing the circels and connecting the dots on the landmarks
        # imgRGB=detector.findHands(imgRGB)
        if name == "Not Recognized":
            print("The person does not have access")
            # cv2.putText("not recognized")
            # time.sleep(2)
            # sys.exit(0)
        y1, x2, y2, x1 = faceloc
        # since we scaled down by 4 times
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, name, (x1 + 6, y2 - 5), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)


    #cv2.waitKey(1)
######################