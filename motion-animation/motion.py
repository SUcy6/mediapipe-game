import cv2
import time
import math as m
import numpy as np
import mediapipe as mp

# Initialize mediapipe pose class.
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

if __name__ == "__main__":
    # For webcam input replace file name with 0.
    cap = cv2.VideoCapture("MTVideo.mp4")
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    # Meta.
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_size = (width, height)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    posList = []

    while cap.isOpened():
        # Capture frames.
        success, image = cap.read()
        if not success:
            print("Null.Frames")
        #     break
        # Get fps.
        fps = cap.get(cv2.CAP_PROP_FPS)
        # Get height and width.
        h, w = image.shape[:2]

        # Convert the BGR image to RGB.
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process the image.
        keypoints = pose.process(image)

        # Convert the image back to BGR.
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Use lm and lmPose as representative of the following methods.
        lm = keypoints.pose_landmarks
        lmw = keypoints.pose_world_landmarks
        lmPose = mp_pose.PoseLandmark

        lmstr = ""
        for id, lm in enumerate(lm.landmark):
            # print(id, lm.x)
            lmstr += f'{lm.x*w},{h - lm.y*h},{lm.z*w},'
        
        posList.append(lmstr)
        print(len(posList))
        

        # Display.
        cv2.imshow("Image", image)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
        with open("AnimationFile.txt", 'w') as f:
            f.writelines(["%s\n" % item for item in posList])

cap.release()
cv2.destroyAllWindows()
