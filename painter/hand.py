import cv2
import time
import math as m
import numpy as np
import mediapipe as mp

############################################################################
############################################################################
# useful functions



############################################################################
############################################################################

font = cv2.FONT_HERSHEY_SIMPLEX

# Colors.
blue = (255, 127, 0)
red = (50, 50, 255)
green = (127, 255, 0)
dark_blue = (127, 20, 0)
light_green = (127, 233, 100)
yellow = (0, 255, 255)
pink = (255, 0, 255)

# Initialize mediapipe class.
# pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
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
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_size = (width, height)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Video writer.
    video_output = cv2.VideoWriter('output.mp4', fourcc, fps, frame_size)

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
        keypoints = pose.process(image)
        results = hands.process(image)

        # Convert the image back to BGR.
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Use wlm and lmPose as representative of the following methods.
        wlm = keypoints.pose_world_landmarks
        lm = keypoints.pose_landmarks
        lmPose = mp_pose.PoseLandmark

        xList = []
        yList = []
        bbox = []
        lmList = []
        if results.multi_hand_landmarks:
                myHand = results.multi_hand_landmarks[0]
                print(myHand)
                for id, lm in enumerate(myHand.landmark):
                    # print(id, lm)
                #     # get x and y for each node on hand
                    cx, cy = int(lm.x * w), int(lm.y * h)
                #     xList.append(cx)
                #     yList.append(cy)
                #     # print(id, cx, cy)
                #     # append coordinate into list
                #     lmList.append([id, cx, cy])

                # # get bounding box
                # xmin, xmax = min(xList), max(xList)
                # ymin, ymax = min(yList), max(yList)
                # bbox = xmin, ymin, xmax, ymax
 
 


        try: 
            # Acquire the world landmark coordinates.
            mpt_shoulder_wx = (wlm.landmark[lmPose.LEFT_SHOULDER].x * 1000  + wlm.landmark[lmPose.RIGHT_SHOULDER].x * 1000 )/2
            mpt_shoulder_wy = (wlm.landmark[lmPose.LEFT_SHOULDER].y * 1000  + wlm.landmark[lmPose.RIGHT_SHOULDER].y * 1000 )/2
            mpt_shoulder_wz = (wlm.landmark[lmPose.LEFT_SHOULDER].z * 1000  + wlm.landmark[lmPose.RIGHT_SHOULDER].z * 1000 )/2
            #mpt_shoulder_z = (lm.landmark[lmPose.LEFT_SHOULDER].z * c + lm.landmark[lmPose.RIGHT_SHOULDER].z * c)/2

            mpt_hip_wx = (wlm.landmark[lmPose.LEFT_HIP].x * 1000  + wlm.landmark[lmPose.RIGHT_HIP].x * 1000 )/2
            mpt_hip_wy = (wlm.landmark[lmPose.LEFT_HIP].y * 1000  + wlm.landmark[lmPose.RIGHT_HIP].y * 1000 )/2
            mpt_hip_wz = (wlm.landmark[lmPose.LEFT_HIP].z * 1000  + wlm.landmark[lmPose.RIGHT_HIP].z * 1000 )/2
            mpt_hip_extend_wx = mpt_hip_wx 
            mpt_hip_extend_wy = 0
            mpt_hip_extend_wz = mpt_hip_wz
            
            left_shoulder_wx = int(wlm.landmark[lmPose.LEFT_SHOULDER].x * 1000)
            left_shoulder_wy = int(wlm.landmark[lmPose.LEFT_SHOULDER].y * 1000)
            left_shoulder_wz = int(wlm.landmark[lmPose.LEFT_SHOULDER].z * 1000)
            
            right_shoulder_wx = int(wlm.landmark[lmPose.RIGHT_SHOULDER].x * 1000)
            right_shoulder_wy = int(wlm.landmark[lmPose.RIGHT_SHOULDER].y * 1000)
            right_shoulder_wz = int(wlm.landmark[lmPose.RIGHT_SHOULDER].z * 1000)
            
            left_hip_wx = int(wlm.landmark[lmPose.LEFT_HIP].x * 1000)
            left_hip_wy = int(wlm.landmark[lmPose.LEFT_HIP].y * 1000)
            left_hip_wz = int(wlm.landmark[lmPose.LEFT_HIP].z * 1000)
            
            right_hip_wx = int(wlm.landmark[lmPose.RIGHT_HIP].x * 1000)
            right_hip_wy = int(wlm.landmark[lmPose.RIGHT_HIP].y * 1000)
            right_hip_wz = int(wlm.landmark[lmPose.RIGHT_HIP].z * 1000)
            
            
            # Acquire the landmark coordinates.
            mpt_shoulder_x = int((lm.landmark[lmPose.LEFT_SHOULDER].x * w  + lm.landmark[lmPose.RIGHT_SHOULDER].x * w )/2)
            mpt_shoulder_y = int((lm.landmark[lmPose.LEFT_SHOULDER].y * h  + lm.landmark[lmPose.RIGHT_SHOULDER].y * h )/2)
            mpt_shoulder_z = int((lm.landmark[lmPose.LEFT_SHOULDER].z * w  + lm.landmark[lmPose.RIGHT_SHOULDER].z * w )/2)
            #mpt_shoulder_z = (lm.landmark[lmPose.LEFT_SHOULDER].z * c + lm.landmark[lmPose.RIGHT_SHOULDER].z * c)/2

            mpt_hip_x = int((lm.landmark[lmPose.LEFT_HIP].x * w  + lm.landmark[lmPose.RIGHT_HIP].x * w )/2)
            mpt_hip_y = int((lm.landmark[lmPose.LEFT_HIP].y * h  + lm.landmark[lmPose.RIGHT_HIP].y * h )/2)
            mpt_hip_z = int((lm.landmark[lmPose.LEFT_HIP].z * w  + lm.landmark[lmPose.RIGHT_HIP].z * w )/2)
            mpt_hip_extend_x = mpt_hip_x 
            mpt_hip_extend_y = 0
            mpt_hip_extend_z = mpt_hip_z


        except AttributeError:
            continue 
        # Draw
        # imageX1 = int(mpt_shoulder_x)
        # imageX2 = int(mpt_hip_x)
        # imageX3 = int(mpt_hip_extend_x)
        # imageY1 = int(mpt_shoulder_y)
        # imageY2 = int(mpt_hip_y)
        # imageY3 = int(mpt_hip_extend_y)

        #draw circle
        # cv2.circle(image, (imageX1, imageY1), 7, yellow, -1)
        # cv2.circle(image, (imageX2, imageY2), 7, yellow, -1)
        # cv2.circle(image, (imageX3, imageY3), 7, yellow, -1)

        # #draw line
        # cv2.line(image, (imageX1, imageY1), (imageX2, imageY2), (255, 255, 255), 3)
        # cv2.line(image, (imageX2, imageY2), (imageX3, imageY3), (255, 255, 255), 3)


        # draw hands
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS)
      
        # Display.
        image = cv2.flip(image, 1)
        cv2.imshow('MediaPipe Pose', image)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
