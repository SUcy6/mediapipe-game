import pygame
import pymunk
import random


class Fruit:
    def __init__(self, space, path, scale=1, grid=(2, 4),
                 animationFrames=None, speedAnimation=1, speed=3, pathSoundSlice=None):
        # Loading Main Image
        self.scale = scale
        img = pygame.image.load(path).convert_alpha()
        width, height = img.get_size()
        img = pygame.transform.smoothscale(img, (int(width * self.scale), int(height * self.scale)))
        width, height = img.get_size()

        # Split image to get all frames
        if animationFrames is None:  # When animation frames is not defined then use all frames
            animationFrames = grid[0] * grid[1]
        widthSingleFrame = width / grid[1]
        heightSingleFrame = height / grid[0]
        self.imgList = []
        counter = 0
        for row in range(grid[0]):
            for col in range(grid[1]):
                counter += 1
                if counter <= animationFrames:
                    imgCrop = img.subsurface((col * widthSingleFrame, row * heightSingleFrame,
                                              widthSingleFrame, heightSingleFrame))
                    self.imgList.append(imgCrop)

        self.img = self.imgList[0]
        self.rectImg = self.img.get_rect()
        # self.rectImg.x, self.rectImg.y = pos[0], pos[1]
        # self.pos = pos
        self.path = path
        self.animationCount = 0
        self.speedAnimation = speedAnimation
        self.isAnimating = False
        self.speed = speed
        self.pathSoundSlice = pathSoundSlice
        if self.pathSoundSlice:
            self.soundSlice = pygame.mixer.Sound(self.pathSoundSlice)
        self.slice = False

        self.widthWindow, self.heightWindow = pygame.display.get_surface().get_size()
        self.pos = random.randint(0, self.widthWindow), 100

        # Physics
        # Body
        self.mass = 1
        self.moment = pymunk.moment_for_circle(self.mass, 0, 30)
        self.body = pymunk.Body(self.mass, self.moment)
        # Shape
        self.shape = pymunk.Circle(self.body, 30)
        self.shape.body.position = self.pos

        # Add to Space
        self.space = space
        self.space.add(self.body, self.shape)

        self.isStartingFrame = True
        self.width, self.height = self.img.get_size()

        if "bomb" in path:
            self.isBomb = True
        else:
            self.isBomb = False

    def draw(self, window):

        if self.isStartingFrame:

            if self.pos[0] < self.widthWindow // 2:
                randX = random.randint(100, 300)
            else:
                randX = random.randint(-300, -100)
            randY = random.randint(900, 1100)
            self.shape.body.apply_impulse_at_local_point((randX, randY), (0, 0))
            self.isStartingFrame = False

        # Draw
        x, y = int(self.body.position[0]), self.heightWindow - int(self.body.position[1])

        self.rectImg.x, self.rectImg.y = x - self.width // 2, y - self.height // 2
        window.blit(self.img, self.rectImg)
        # pygame.draw.circle(window, (255, 0, 0), (x, y), 25)

    def checkSlice(self, x, y):

        # Check for the hit
        fx, fy = self.rectImg.x + int(186 * self.scale), self.rectImg.y + int(186 * self.scale)
        fw, fh = int(140 * self.scale), (140 * self.scale)

        if fx < x < fx + fw and fy < y < fy + fh and self.isAnimating is False:
            self.isAnimating = True
            if self.pathSoundSlice:
                self.soundSlice.play()

        if self.isAnimating:
            # Loop through all the frames
            if self.animationCount != len(self.imgList) - 1:
                self.animationCount += 1
                self.img = self.imgList[self.animationCount]
            else:
                self.slice = True
                self.space.remove(self.shape, self.body)

        if self.slice:
            if self.isBomb:
                return 2
            else:
                return 1
        else:
            return None
