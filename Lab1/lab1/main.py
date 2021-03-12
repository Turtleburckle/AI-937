import pygame
import pickle
import numpy as np
from random import randint, random

from lab1.model import Colors
from lab1.model import Directions
from lab1.model import Drone
from lab1.model import DMap
from lab1.controller import MyController


class Environment:

    def __init__(self, colors, directions):
        self.__n = 20
        self.__m = 20
        self.__surface = np.zeros((self.__n, self.__m))
        self.colors = colors
        self.directions = directions

    def randomMap(self, fill=0.2):
        for i in range(self.__n):
            for j in range(self.__m):
                if random() <= fill:
                    self.__surface[i][j] = 1

    def existsWallThere(self, x, y):
        if self.__surface[x][y] == 1:
            return True
        else:
            return False

    def readUDMSensors(self, x, y):
        readings = [0, 0, 0, 0]
        # UP
        xf = x - 1
        while (xf >= 0) and (self.__surface[xf][y] == 0):
            xf -= 1
            readings[self.directions.getUp()] += 1
        # DOWN
        xf = x + 1
        while (xf < self.__n) and (self.__surface[xf][y] == 0):
            xf += 1
            readings[self.directions.getDown()] += 1
        # LEFT
        yf = y - 1
        while (yf >= 0) and (self.__surface[x][yf] == 0):
            yf -= 1
            readings[self.directions.getLeft()] += 1
        # RIGHT
        yf = y + 1
        while (yf < self.__m) and (self.__surface[x][yf] == 0):
            yf += 1
            readings[self.directions.getRight()] += 1
        return readings

    def saveEnvironment(self, numFile):
        with open(numFile, 'wb') as f:
            pickle.dump(self, f)
            f.close()

    def loadEnvironment(self, numFile):
        with open(numFile, "rb") as f:
            dummy = pickle.load(f)
            self.__n = dummy.__n
            self.__m = dummy.__m
            self.__surface = dummy.__surface
            f.close()

    def image(self):
        imagine = pygame.Surface((420, 420))
        brick = pygame.Surface((20, 20))
        brick.fill(self.colors.getBlueColor())
        imagine.fill(self.colors.getWhiteColor())
        for i in range(self.__n):
            for j in range(self.__m):
                if self.__surface[i][j] == 1:
                    imagine.blit(brick, (j * 20, i * 20))
        return imagine

    def __str__(self):
        string = ""
        for i in range(self.__n):
            for j in range(self.__m):
                string = string + str(int(self.__surface[i][j]))
            string = string + "\n"
        return string


def generateCoordinatesForDrone(environment):
    x = randint(0, 19)
    y = randint(0, 19)
    if environment.existsWallThere(x, y):
        generateCoordinatesForDrone(environment)
    else:
        return [x, y]


def main():
    colors = Colors.ColorsClass()
    directions = Directions.DirectionsClass()
    environment = Environment(colors, directions)
    environment.loadEnvironment("lab1/test2.map")
    dmap = DMap.DMapClass(colors, directions)
    xy = generateCoordinatesForDrone(environment)
    drone = Drone.DroneClass(xy[0], xy[1], directions)
    n = 5
    # n = int(input("n="))
    controller = MyController.MyControllerClass(environment, dmap, drone, colors, directions, n)
    controller.run()


if __name__ == "__main__":
    main()
