import HandTracking as htm
import cv2
import numpy as np
import time
import math
import pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pyautogui, sys
import SlideInteraction as sli

#############
wCam, hCam = 640,480

#############
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
volBar =400
vol = 0
pTime = 0
volPer =0
detector = htm.handDetector()
MouseControl = sli.SlideInteraction()

spaceState = False

#using pycaw library to control volume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

HAND_1 = detector.HAND_1
HAND_2 = detector.HAND_2
MouseControlState = False
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    #img = detector.findHands(img)
    lmList = detector.findPosition(img)

    #get landmark only if hand is detected (see landmark information point on mediapipe website)

    # lmList = [[(393, 483), (353, 486), (318, 476), (289, 468), (261, 464), (321, 412), (294, 379), (281, 356), (270, 336),
    #          (342, 399), (321, 354), (307, 324), (296, 299), (367, 397), (352, 352), (340, 325), (328, 302), (393, 402),
    #          (390, 368), (385, 346), (378, 326)], {'type': 'Left'}][(393, 483), (353, 486), (318, 476), (289, 468), (261, 464), (321, 412), (294, 379), (281, 356), (270, 336),
    #     #          (342, 399), (321, 354), (307, 324), (296, 299), (367, 397), (352, 352), (340, 325), (328, 302), (393, 402),
    #     #          (390, 368), (385, 346), (378, 326)], {'type': 'Left'}

    if len(lmList) !=0:
        hand1 = lmList[0]

        #print(lmList[4], lmList[8], lmList[12])
        #get the x and y value from thumb and index
        lmList1 = hand1["lmList"]
        handType1 = hand1["type"]  # Handtype Left or Right
        fingers1 = detector.fingersup(hand1)
        #print(fingers1)
        if len(lmList) ==1:
    # region volume
            #coordinate for index and thumb
            x1, y1 = lmList1[4][0], lmList1[4][1]
            x2, y2 = lmList1[8][0], lmList1[8][1]
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
            #coordinate for middle finger and Palm point
            x3, y3 = lmList1[12][0], lmList1[12][1]
            x4, y4 = lmList1[9][0], lmList1[9][1]
            cv2.line(img, (x3, y3), (x4, y4), (255, 0, 255), 2)

            cx,cy = (x1+x2)//2, (y1+y2)//2
            cxStop, cyStop = (x3 + x4) // 2, (y3 + y4) // 2

            cv2.circle(img, (x1, y1), 6, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 6, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 6, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), 6, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cxStop, cyStop), 6, (255, 0, 255), cv2.FILLED)

            # value from length between thumb and index : max:120 and min:15
            # volume range : -65 -> 0
            length = math.hypot(x2 - x1, y2 - y1)
            vol = np.interp(length, [50, 150], [minVol, maxVol])

            volBar = np.interp(length, [50, 150], [400, 150])
            volPer = np.interp(length, [50, 150], [0, 100])

            volume.SetMasterVolumeLevel(vol, None)
            if length < 30:
                cv2.circle(img, (cx, cy), 9, (0, 255, 0), cv2.FILLED)
            cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
            cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
            cv2.putText(img, f'{int(volPer)}%', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                        1, (255, 0, 0), 3)
    #endregion volume

    #region spacebaroperation
            lengthStop = math.hypot(x4 - x3, y4 - y3)
            if lengthStop < 40:
                cv2.circle(img, (cxStop, cyStop), 15, (0, 255, 0), cv2.FILLED)

                if not spaceState:
                    spaceState = True
                    pyautogui.press("space")

            if lengthStop > 40:
                spaceState = False
    #endregion spacebar operation

        handDataLength = len(lmList)

        if handDataLength ==2:
            hand1 = lmList[0]
            hand2 = lmList[1]


            # Here hand1 will be the left hand, hand2 the right one
            if hand1["type"] == "Left":
                lmListLeft = hand1["lmList"]
                lmListRight = hand2["lmList"]
                handTypeLeft = hand1["type"]
                handTypeRight = hand2["type"]
                fingersLeft = detector.fingersup(hand1)
                fingersRight = detector.fingersup(hand2)


            if hand1["type"] == "Right":
                lmListLeft = hand2["lmList"]
                lmListRight = hand1["lmList"]
                handTypeLeft = hand2["type"]
                handTypeRight = hand1["type"]
                fingersLeft = detector.fingersup(hand2)
                fingersRight = detector.fingersup(hand1)


            point1x, point1y = lmListLeft[8][0], lmListLeft[8][1]
            point2x, point2y = lmListRight[8][0], lmListRight[8][1]
            cxindex, cyindex = (point1x + point2x) // 2, (point1y + point2y) // 2
            cv2.line(img, (point1x,point1y), (point2x,point2y), (255, 0, 255), 2)
            cv2.circle(img, (cxindex, cyindex), 9, (255, 0, 255), cv2.FILLED)
            lengthIndex = math.hypot(point1x-point2x, point1y-point2y)
            if lengthIndex < 30:
                cv2.circle(img, (cxindex, cyindex), 9, (0, 255, 0), cv2.FILLED)
            # myLmList[self.tipIds[0]][0] < myLmList[self.tipIds[0] - 1][0]:
            # myLmList[self.tipIds[id]][1] < myLmList[self.tipIds[id] - 2][1]:

            # coordinate for index and wrist
            x5, y5 = lmListLeft[0][0], lmListLeft[0][1]
            x6, y6 = lmListRight[8][0], lmListRight[8][1]
            iwx, iwy = (x5 + x6) // 2, (y5 + y6) // 2
            cv2.line(img, (x5, y5), (x6, y6), (0, 100, 255), 3)
            lengthControlMouse = math.hypot(x5-x6, y5-y6)
            cv2.circle(img, (iwx, iwy), 9, (255, 0, 255), cv2.FILLED)
            if lengthControlMouse < 45:
                cv2.circle(img, (iwx, iwy), 9, (0, 255, 0), cv2.FILLED)
                MouseControlState = 'True'

            if MouseControlState:
                ControlMousess = MouseControl.MouseInteraction(hand1, hand2)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS:{int(fps)}', (40,50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255,0 ,0), 3)
    cv2.imshow("img", img)
    cv2.waitKey(1)