# Import
import os
import random
import pygame
import mediapipe as mp
import cv2
import numpy as np
from Fruit import Fruit
import pymunk
import time


def Game():
    # Initialize
    pygame.init()
    pygame.event.clear()

    # Create Window/Display
    width, height = 1200, 686
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Fruit Slicer")

    # Initialize Clock for FPS
    fps = 23
    clock = pygame.time.Clock()

    # Images
    imgGameOver = pygame.image.load("./fru.jpg").convert()

    # # Hand Detector
    # detector = HandDetector(maxHands=1, detectionCon=0.8)
    # Initialize mediapipe pose class.
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    # Webcam
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)  # width
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)  # height

    # Meta.
    # fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Physics
    space = pymunk.Space()
    space.gravity = 0.0, -1000.0

    # Parameters
    timeTotal = 60

    # Variables
    fruitList = []
    timeGenerator = time.time()
    timeStart = time.time()
    gameOver = False
    score = 0

    # Colors.
    blue = (255, 127, 0)
    yellow = (0, 255, 255)
    white = (255,255,255)
    black = (0,0,0)

    # Fruit Path List
    pathFruitFolder = "./Fruits"
    pathListFruit = os.listdir(pathFruitFolder)

    # Fruit
    def generateFruit():
        randomScale = round(random.uniform(0.6, 0.8), 2)
        randomFruitPath = pathListFruit[random.randint(0, len(pathListFruit) - 1)]
        if "bomb" in randomFruitPath:
            pathSoundSlice = './explosion.wav'
        else:
            pathSoundSlice = './slice.wav'

        fruitList.append(Fruit(space, path=os.path.join(pathFruitFolder, randomFruitPath),
                               grid=(4, 4), animationFrames=14, scale=randomScale,
                               pathSoundSlice=pathSoundSlice))

    # Main loop
    while cap.isOpened():
        # Get Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

        if gameOver is False:
            success, img = cap.read()
            img = cv2.flip(img, 1)
            # Get height and width.
            h, w = img.shape[:2]

            # Convert the BGR image to RGB.
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Process the image.
            keypoints = pose.process(img)

            # Convert the image back to BGR.
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            # Process the image.
            lm = keypoints.pose_landmarks
            lmPose = mp_pose.PoseLandmark

            try:
                # Nose
                nose_x = int(lm.landmark[lmPose.NOSE].x * w)
                nose_y = int(lm.landmark[lmPose.NOSE].y * h)
            except AttributeError:
                continue

            # Draw circles
            cv2.circle(img, (nose_x, nose_y), 20, yellow, -1)

            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            imgRGB = np.rot90(imgRGB)
            frame = pygame.surfarray.make_surface(imgRGB).convert()
            frame = pygame.transform.flip(frame, True, False)
            window.blit(frame, (0, 0))


            if time.time() - timeGenerator > 1:
                generateFruit()
                timeGenerator = time.time()

            x, y = nose_x, nose_y
            for i, fruit in enumerate(fruitList):
                if fruit:
                    fruit.draw(window)
                    checkSlice = fruit.checkSlice(x, y)
                    if checkSlice == 2:
                        gameOver = True
                        pygame.mixer.music.stop()
                    if checkSlice == 1:
                        fruitList[i] = False
                        score += 1

            timeLeft = int(timeTotal - (time.time() - timeStart))
            if timeLeft <= 0:
                gameOver = True
                pygame.mixer.music.stop()

            font = pygame.font.Font(None, 60)
            textScore = font.render(str(score), True, blue)
            textTime = font.render(str(timeLeft), True, blue)
            window.blit(textScore, (225, 35))
            window.blit(textTime, (1100, 38))


        else:
            window.blit(imgGameOver, (0, 0))

            # Text Score
            font = pygame.font.Font(None, 150)
            textLose = font.render("You Lose!", True, (0, 0, 0))
            textYour = font.render("Your Score:", True, (0, 0, 0))
            textScore = font.render(str(score), True, (0, 0, 0))
            window.blit(textLose, (400, 143))
            window.blit(textYour, (350, 243))
            window.blit(textScore, (600, 343))

        # Update Display
        pygame.display.update()
        # Set FPS
        clock.tick(fps)
        space.step(1 / fps)


if __name__ == "__main__":
    Game()
