import cv2
import time
import pyautogui, sys

class SlideInteraction:
    def MouseInteraction(self, handLeft, handRight):

            lmListLeft = handLeft["lmList"]
            lmListRight = handRight["lmList"]
            #wCam, hCam = 640,480
            #maxwidth/height = 1919, 1079
            xMultiplier = 4
            yMultiplier = 4

            cxMouse, cyMouse = lmListLeft[9][0], lmListLeft[9][1]

            cxMouse *=xMultiplier
            cyMouse *=yMultiplier

            pyautogui.moveTo(cxMouse, cyMouse)

            if lmListRight[8][1] > lmListRight[7][1]:
                pyautogui.click(cxMouse, cyMouse)

            if lmListRight[12][1] > lmListRight[11][1]:
                pyautogui.click(cxMouse, cyMouse,button='right')
                #pyautogui.click(cxMouse, cyMouse)
            #cxMouse, cyMouse = pyautogui.position()
            # pyautogui.moveTo(cxMouse, cyMouse)
            # positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
            # print(positionStr), print('\b' * (len(positionStr) + 2), sys.stdout.flush())