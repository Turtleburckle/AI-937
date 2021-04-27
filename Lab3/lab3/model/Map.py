from random import *
import numpy as np
import pickle


class MapClass:
    def __init__(self, n=20, m=20):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))
        self.fileName = "test2.map"
        self.dronePosition = (0, 0)

    def areNeighbors(self, point1, point2):
        xPoint1 = point1[0]
        yPoint1 = point1[1]
        xPoint2 = point2[0]
        yPoint2 = point2[1]
        if xPoint1 == xPoint2:
            if yPoint1 - 1 == yPoint2:
                return True
            elif yPoint1 + 1 == yPoint2:
                return True
        elif yPoint1 == yPoint2:
            if xPoint1 - 1 == xPoint2:
                return True
            elif xPoint1 + 1 == xPoint2:
                return True
        else: return False

    def existsWall(self, x, y):
        return self.surface[x][y] == 1

    def randomMap(self, fill=0.2):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill:
                    self.surface[i][j] = 1

    def saveMap(self, nameFile):
        self.fileName = nameFile
        with open(nameFile, 'wb') as f:
            pickle.dump(self, f)
            f.close()
        self.dronePosition = self.generateRandomPosition()

    def generateRandomPosition(self):
        xPosition = randint(0, self.n-1)
        yPosition = randint(0, self.m-1)
        while self.surface[xPosition][yPosition] == 1:
            xPosition = randint(0, self.n-1)
            yPosition = randint(0, self.m-1)
        position = (xPosition, yPosition)
        return position

    def loadMap(self, nameFile):
        self.fileName = nameFile
        with open(nameFile, "rb") as f:
            dummy = pickle.load(f)
            self.n = dummy.n
            self.m = dummy.m
            self.surface = dummy.surface
            f.close()
        self.dronePosition = self.generateRandomPosition()

    def getSurface(self):
        return self.surface

    def getDronePosition(self):
        return self.dronePosition

    def __str__(self):
        string = ""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string
