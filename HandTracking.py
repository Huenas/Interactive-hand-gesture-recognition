import cv2
import time


# Camera settings
DEFAULT_CAM = 0 # Built-in camera
USB_CAM = 1 # External camera connected via USB port

CAM_SELECTED = DEFAULT_CAM
CAM_WIDTH = 1280
CAM_HEIGHT = 720
CAM_FPS = 30
FLIP_CAMERA_FRAME_HORIZONTALLY = True

# mediapipe parameters
MAX_HANDS = 2
DETECTION_CONF = 0.8
TRACKING_CONF = 0.8
MODEL_COMPLEX = 1
HAND_1 = 0
HAND_2 = 1
INDEX_FINGER_TIP = 8
X_COORD = 0
Y_COORD = 1

FIGURES_LIST = ["Circles", "MergedCircle", "Rectangle"]

# Drawing parameters - for opencv
CIR_RADIUS = 200
CIR_COLOR = (255, 0, 0)
CIR_THICKNESS = 3

MERG_CIR_COLOR = (0, 255, 0)
MERG_CIR_THICKNESS = 3

RECT_POINT = 300
RECT_COLOR = (0, 0, 255)
RECT_THICKNESS = 3


# class creation from hand in mediapipe
class handDetector():
    import mediapipe as mp
    HAND_1 = 0
    HAND_2 = 1
    def __init__(self, max_hands=MAX_HANDS, det_conf=DETECTION_CONF, complexity=MODEL_COMPLEX, track_conf=TRACKING_CONF):
        """
        Inputs:-
        static_image_mode: Mode of input. If set to False, the solution treats the input images as a video stream.
        max_num_hands: Maximum number of hands to detect. Default to 2
        model_complexity: Complexity of the hand landmark model. 0 or 1.
                          Landmark accuracy as well as inference latency generally go up with the model complexity.
                          Default to 1.
        min_detection_confidence: Minimum confidence value ([0.0, 1.0]) from the hand detection model for the
                                  detection to be considered successful. Default to 0.5.
        min_tracking_confidence: Minimum confidence value ([0.0, 1.0]) from the landmark-tracking model for the
                                 hand landmarks to be considered tracked successfully.
                                 Ignored if static_image_mode is True. Default to 0.5.
        Output:-
        multi_hand_landmarks: Collection of detected/tracked hands, where each hand is represented as a
                              list of 21 hand landmarks and each landmark is composed of x, y and z.
                              x and y are normalized to [0.0, 1.0] by the image width and height respectively.
        """
        self.hands = self.mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=max_hands,
                                                   model_complexity=complexity, min_detection_confidence=det_conf,
                                                   min_tracking_confidence=track_conf)
        self.mpHands = self.mp.solutions.hands
        self.mpDraw = self.mp.solutions.drawing_utils # it gives small dots onhands total 20 landmark points

    def fingersup(self,myHand):
        #imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #self.results = self.hands.process(imgRGB)
        myHandType = myHand["type"]
        myLmList = myHand["lmList"]
        tipIds = [4, 8, 12, 16, 20]
        #myLmList = myHandType[0]
        fingers = []
        pointFingers = []

        # Thumb
        if myLmList[tipIds[0]][0] > myLmList[tipIds[0] - 1][0]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 Fingers
        for id in range(1, 5):
            if myLmList[tipIds[id]][1] < myLmList[tipIds[id] - 1][1]:
                # xtest, ytest = myLmList[tipIds[id]][0], myLmList[tipIds[id]][1]
                # pointFingers.append((xtest,ytest))
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers#, pointFingers


    def findHands(self,img,draw=True):
        # Send rgb image to hands

        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB) # process the frame
    #   print(results.multi_hand_landmarks)
        return img

    def findPosition(self,img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)  # process the frame
        #   print(results.multi_hand_landmarks)
        allHands = []
        #lmlist = []
        multi_hand_landmarks = self.hands.process(img).multi_hand_landmarks

        if multi_hand_landmarks:
            #for handType, handLms in zip(self.results.multi_handedness, self.results.multi_hand_landmarks):
            for handType, hand_landmarks in zip(self.results.multi_handedness, self.results.multi_hand_landmarks):  # Stepping through each hand
            #for hand_landmarks in multi_hand_landmarks:  # Stepping through each hand
                mylmList = []
                myHand = {}
                for land_mark in hand_landmarks.landmark:  # Stepping through the 21 landmarks of each hand
                    # landmark is a dict with x,y & z coordinates. We are interested in x & y only.
                    # Since x & y are normalized, multiply them with camera width and height to get the actual values.
                    # Finally, convert the coordinates into integers for opencv
                    for handLms in self.results.multi_hand_landmarks:
                        # Draw dots and connect them
                        self.mpDraw.draw_landmarks(img, handLms,
                                                   self.mpHands.HAND_CONNECTIONS)

                    h, w, c = img.shape
                    mylmList.append((int(land_mark.x * w), int(land_mark.y * h)))

                myHand["lmList"] = mylmList

                #lmlist.append(mylmList)
                #allHands.append(mylmList)

                if handType.classification[0].label == "Right":


                    myHand["type"] = "Left"
                else:
                    myHand["type"] = "Right"
                allHands.append(myHand)
        #print("my hands: ", lmlist)
        return allHands

    def marks(self, img):
        my_hands = []
        frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # opencv works in BGR, while rest of the world in RGB
        multi_hand_landmarks = self.hands.process(frame_rgb).multi_hand_landmarks
        if multi_hand_landmarks:  # Do the following if we have detected/tracked hands
            # multi_hand_landmarks is an array of arrays. Each array contains the 21 landmarks (in dict) of each hand
            for hand_landmarks in multi_hand_landmarks:  # Stepping through each hand
                my_hand = []
                for land_mark in hand_landmarks.landmark:  # Stepping through the 21 landmarks of each hand
                    # landmark is a dict with x,y & z coordinates. We are interested in x & y only.
                    # Since x & y are normalized, multiply them with camera width and height to get the actual values.
                    # Finally, convert the coordinates into integers for opencv
                    h, w, c = img.shape
                    my_hand.append((int(land_mark.x * w), int(land_mark.y * h)))
                my_hands.append(my_hand)
        #print("my hands: ", my_hands)
        return my_hands


findHands = handDetector()

def main():
    #Frame rates
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()

    while True:
        success,img = cap.read()
        img = detector.findHands(img)
        lmList= detector.findPosition(img)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        handData = detector.findPosition(img)  # Get the locations of both hands & fingers

        handDataLength = len(handData)  # Get the number of hands in the frame
        #print("ddddd",handData)
        # print(handDataLength)
        cv2.putText(img,str(int(fps)),(10,70), cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)

        cv2.imshow("Video",img)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()