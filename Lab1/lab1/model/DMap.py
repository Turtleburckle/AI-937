import numpy as np
import pygame


class DMapClass:

    def __init__(self, colors, directions):
        self.__n = 20
        self.__m = 20
        self.surface = np.zeros((self.__n, self.__m))
        self.colors = colors
        self.directions = directions
        for i in range(self.__n):
            for j in range(self.__m):
                self.surface[i][j] = -1

    def markDetectedWalls(self, e, x, y):
        # walls - [up,left,down,right]
        walls = e.readUDMSensors(x, y)

        # UP
        index = 1
        if walls[self.directions.getUp()] > 0:
            while index <= walls[self.directions.getUp()] and (x-index) > 0:
                self.surface[x-index][y] = 0
                index += 1
        if (x - index) >= 0 :
            self.surface[x-index][y] = 1

        # DOWN
        index = 1
        if walls[self.directions.getDown()] > 0:
            while index <= walls[self.directions.getDown()] and (x + index) < self.__n:
                self.surface[x+index][y] = 0
                index += 1
        if (x + index) < self.__n :
            self.surface[x+index][y] = 1

        # LEFT
        index = 1
        if walls[self.directions.getLeft()] > 0:
            while index <= walls[self.directions.getLeft()] and (y-index) > 0:
                self.surface[x][y-index] = 0
                index += 1
        if (y-index) >= 0:
            self.surface[x][y-index] = 1

        # RIGHT
        index = 1
        if walls[self.directions.getRight()] > 0:
            while index <= walls[self.directions.getRight()] and (y+index) < self.__m:
                self.surface[x][y+index] = 0
                index += 1
        if (y + index) < self.__m:
            self.surface[x][y+index] = 1

        return None

    def image(self, x, y):
        imagine = pygame.Surface((420, 420))
        brick = pygame.Surface((20, 20))
        empty = pygame.Surface((20, 20))
        coloredBrick = pygame.Surface((20, 20))
        empty.fill(self.colors.getWhiteColor())
        brick.fill(self.colors.getBlackColor())
        coloredBrick.fill(self.colors.getPurpleColor())
        imagine.fill(self.colors.getGrayBlueColor())

        for i in range(self.__n):
            for j in range(self.__m):
                if self.surface[i][j] == 1:
                    imagine.blit(brick, (j * 20, i * 20))
                elif self.surface[i][j] == 0:
                    imagine.blit(empty, (j * 20, i * 20))

        drona = pygame.image.load("lab1/drona.png")
        imagine.blit(coloredBrick,(y*20, x*20))
        imagine.blit(drona, (y * 20, x * 20))
        return imagine
