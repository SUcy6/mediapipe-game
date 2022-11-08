import cv2
import time
import math as m
import numpy as np
import mediapipe as mp

############################################################################
############################################################################
# useful functions
def fingersUp(lmList):
    fingers = []
    # Thumb
    if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
        fingers.append(1)
    else:
        fingers.append(0)
 
    # Fingers
    for id in range(1, 5):
        if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
            fingers.append(1)
        else:
            fingers.append(0)
 
        # totalFingers = fingers.count(1)
 
    return fingers




############################################################################
############################################################################

font = cv2.FONT_HERSHEY_SIMPLEX

# Colors.
blue = (250, 206, 135)
red = (49, 49, 255)
green = (127, 255, 0)
dark_blue = (127, 20, 0)
light_green = (127, 233, 100)
yellow = (0, 234, 255)
pink = (255, 0, 255)
purple = (128, 0, 128)
orange = (80, 127, 250)

drawColor = (0, 0, 0)

# thickness
brushThickness = 25
eraserThickness = 100

# thumb, index, middle finger, ring finger, pinky
tipIds = [4, 8, 12, 16, 20]
xp, yp = 0, 0

# get header
header = cv2.imread("Header/header.png")

# Initialize mediapipe class.

# hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=True,max_num_hands=2,min_detection_confidence=0.5)
mpDraw = mp.solutions.drawing_utils
############################################################################
############################################################################
if __name__ == "__main__":

    # For webcam input replace file name with 0.
    # For video input replace 0 with file name
    file_name = 0
    cap = cv2.VideoCapture(0)
    
    # Meta data
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    # width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = 1280
    height = 720
    frame_size = (width, height)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Video writer.
    video_output = cv2.VideoWriter('output.mp4', fourcc, fps, frame_size)

    imgCanvas = np.zeros((720, 1280, 3), np.uint8)

    while cap.isOpened():
        # Capture frames.
        success, image = cap.read()
        #ret, frame = cap.read()

        if not success:
            print("Null.Frames")

        # Get height and width.
        h, w, c = image.shape

        # Try mark the image as not writeable
        image.flags.writeable = False
        
        # Convert the BGR image to RGB.
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process the image.
        results = hands.process(image)

        # Convert the image back to BGR.
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # hands
        # hl = results.multi_hand_landmarks[0]
        # hr = results.multi_hand_landmarks[1]

        xList = []
        yList = []
        bbox = []
        lmList = []
        if results.multi_hand_landmarks:
                myHand = results.multi_hand_landmarks[0]

                # draw hand landmarks
                for handLms in results.multi_hand_landmarks:
                    mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS)

                for id, lm in enumerate(myHand.landmark):
                    # print(id, lm)
                    # get x and y for each node on hand
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    xList.append(cx)
                    yList.append(cy)
                    # print(id, cx, cy)
                    # append coordinate into list
                    lmList.append([id, cx, cy])

                # get bounding box
                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                bbox = xmin, ymin, xmax, ymax

        if len(lmList) != 0:
            # print(lmList[4])

            # tip of index and middle fingers
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]

            # Check which fingers are up
            fingers = fingersUp(lmList)

            # Selection Mode - Two finger are up
            if fingers[1] and fingers[2]:
                xp, yp = 0, 0
                # print("Selection Mode")
                # Checking for the click
                if y1 < 125:
                    if 160 < x1 < 300: 
                        drawColor = purple
                    elif 325 < x1 < 470:
                        drawColor = orange
                    elif 500 < x1 < 640:
                        drawColor = yellow
                    elif 675 < x1 < 800:
                        drawColor = blue
                    elif 840 < x1 < 960:
                        drawColor = red
                    elif 990 < x1 < 1120:
                        drawColor = (0,0,0)
                cv2.rectangle(image, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

            # Drawing Mode - Index finger is up
            if fingers[1] and fingers[2] == False:
                cv2.circle(image, (x1, y1), 15, drawColor, cv2.FILLED)
                # print("Drawing Mode")
                if xp == 0 and yp == 0:
                    xp, yp = x1, y1
 
                cv2.line(image, (xp, yp), (x1, y1), drawColor, brushThickness)
                if drawColor == (0, 0, 0):
                    cv2.line(image, (xp, yp), (x1, y1), drawColor, eraserThickness)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            
                else:
                    cv2.line(image, (xp, yp), (x1, y1), drawColor, brushThickness)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

                xp, yp = x1, y1

            if fingers[1] == False:
                xp, yp = 0, 0


            # Clear Canvas when all fingers are up
            if all (x >= 1 for x in fingers):
                imgCanvas = np.zeros((720, 1280, 3), np.uint8)
            
        
        imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
        image = cv2.bitwise_and(image,imgInv)
        image = cv2.bitwise_or(image,imgCanvas)
      
        # Display.
        image = cv2.flip(image, 1)
        # imgCanvas = cv2.flip(imgCanvas, 1)
        # imgInv = cv2.flip(imgInv, 1)
        # image = cv2.addWeighted(image,0.5,imgCanvas,0.5,0)
        image[0:125, 0:1280] = header
        cv2.imshow('MediaPipe Pose', image)
        # cv2.imshow("Canvas", imgCanvas)
        # cv2.imshow("Inv", imgInv)
        cv2.waitKey(1)

        # press 'q' to quit the game
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
