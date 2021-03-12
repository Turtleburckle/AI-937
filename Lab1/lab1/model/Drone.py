import time

import pygame


class DroneClass:

    def __init__(self, x, y, directions):
        self.x = x
        self.y = y
        self.directions = directions
        self.moves = []

    def move(self, detectedMap, direction):
        if self.x > 0 and self.directions.getUp() == direction: self.moveUp(detectedMap)
        if self.x < 19 and self.directions.getDown() == direction: self.moveDown(detectedMap)
        if self.y > 0 and self.directions.getLeft() == direction: self.moveLeft(detectedMap)
        if self.y < 19 and self.directions.getRight() == direction: self.moveRight(detectedMap)

    def moveUp(self, detectedMap):
        if detectedMap.surface[self.x - 1][self.y] == 0:
            self.x = self.x - 1

    def moveDown(self, detectedMap):
        if detectedMap.surface[self.x + 1][self.y] == 0:
            self.x = self.x + 1

    def moveLeft(self, detectedMap):
        if detectedMap.surface[self.x][self.y - 1] == 0:
            self.y = self.y - 1

    def moveRight(self, detectedMap):
        if detectedMap.surface[self.x][self.y + 1] == 0:
            self.y = self.y + 1

# This method receives:
# -> move - the direction in which the move needs to be made
# adds to the moves stack the move that needs to be made.
    def addMove(self, move):
        self.moves.append(move)

# This method receives:
# -> detectedMap - the map where the drone is
# and moves one step from the stack of moves. Returns :
# -> True - if there are no more moves that need to be made
# -> False - if there are still moves that need to be made
    def doOneStep(self, detectedMap):
        move = self.moves.pop()
        self.printMoves(self.moves)
        self.move(detectedMap, move)
        if len(self.moves) == 0:
            return True
        return False

    # This method receives:
    # -> n - the size that the square needs to be
    # -> environment - the environment that provides the UDM Sensors reading
    # parses every "neighbor" of every block that can be reached from the start point and after that
    # calls another method that tries to find a square of n by n between this neighbors.
    def moveDSF(self, n, environment):
        stack = [(self.x, self.y)]
        blocksPassed = []
        while len(stack) != 0:
            currentBlock = stack.pop()
            reading = environment.readUDMSensors(currentBlock[0], currentBlock[1])
            if reading[self.directions.getUp()] > 0:
                coordinates = (currentBlock[0] - 1, currentBlock[1])
                if not (coordinates in blocksPassed) and not (coordinates in stack): stack.insert(0, coordinates)
            if reading[self.directions.getDown()] > 0:
                coordinates = (currentBlock[0] + 1, currentBlock[1])
                if not (coordinates in blocksPassed) and not (coordinates in stack): stack.insert(0, coordinates)
            if reading[self.directions.getLeft()] > 0:
                coordinates = (currentBlock[0], currentBlock[1] - 1)
                if not (coordinates in blocksPassed) and not (coordinates in stack): stack.insert(0, coordinates)
            if reading[self.directions.getRight()] > 0:
                coordinates = (currentBlock[0], currentBlock[1] + 1)
                if not (coordinates in blocksPassed) and not (coordinates in stack): stack.insert(0, coordinates)
            blocksPassed.append(currentBlock)
        for currentBlock in blocksPassed:
            option = self.searchForSquare(blocksPassed, currentBlock, n)
            if option != -1:
                self.createPath(currentBlock, blocksPassed, n, option)
                return True
        return False

    # This method receives:
    # -> startPoint - the point from where the path needs to start
    # -> blockPassed - the list of neighbors that can be passed
    # -> n - the size of the square/path
    # -> option - the moves that need to be made in order to create the path
    # and adds the moves that need to be made in order to create the path/square.
    def createPath(self, startPoint, blockPassed, n, option):
        print(str(self.x) + ";" + str(self.y))
        print(startPoint)
        print(option)
        if startPoint[0] != self.x or startPoint[1] != self.y:
            self.moveToPoint((self.x, self.y), startPoint, blockPassed)
        for line in range(n):
            for block in range(n):
                if line == 0 and block < n-1:
                    if option == 0 or option == 1: self.addMove(self.directions.getUp())
                    elif option == 2 or option == 3: self.addMove(self.directions.getDown())
                elif line == 1 and block < n-1:
                    if option == 0 or option == 2: self.addMove(self.directions.getRight())
                    elif option == 1 or option == 3: self.addMove(self.directions.getLeft())
                elif line == 2 and block < n-1:
                    if option == 0 or option == 1: self.addMove(self.directions.getDown())
                    elif option == 2 or option == 3: self.addMove(self.directions.getUp())
                elif line == 3 and block < n-1:
                    if option == 0 or option == 2: self.addMove(self.directions.getLeft())
                    elif option == 1 or option == 3: self.addMove(self.directions.getRight())
        self.moves.reverse()

    # This method receives:
    # -> startPoint - from where we need to start
    # -> endPoint - where we need to arrive
    # -> neighbors - the list of the points parsed by the DFS method
    # and sets the moves that need to be done in order to reach the endPoint from the startPoint
    def moveToPoint(self, startPoint, endPoint, neighbors):
        while startPoint != endPoint:
            coordinates = (-1, -1)
            if startPoint[0] > endPoint[0]:
                coordinates = (startPoint[0] - 1, startPoint[1])
                if coordinates in neighbors:
                    startPoint = coordinates
                    self.addMove(self.directions.getUp())
            elif startPoint[0] < endPoint[0]:
                coordinates = (startPoint[0] + 1, startPoint[1])
                if coordinates in neighbors:
                    startPoint = coordinates
                    self.addMove(self.directions.getDown())
            if startPoint[1] > endPoint[1]:
                coordinates = (startPoint[0], startPoint[1] - 1)
                if coordinates in neighbors:
                    startPoint = coordinates
                    self.addMove(self.directions.getLeft())
            elif startPoint[1] < endPoint[1]:
                coordinates = (startPoint[0], startPoint[1] + 1)
                if coordinates in neighbors:
                    startPoint = coordinates
                    self.addMove(self.directions.getRight())
            if coordinates == (-1, -1):
                if startPoint[0] > endPoint[0]:
                    coordinates1 = (startPoint[0] + 1, startPoint[1] - 1)
                    coordinates2 = (startPoint[0] + 1, startPoint[1] + 1)
                    if coordinates1 in neighbors:
                        self.addMove(self.directions.getDown())
                        self.addMove(self.directions.getLeft())
                    elif coordinates2 in neighbors:
                        self.addMove(self.directions.getDown())
                        self.addMove(self.directions.getRight())
                elif startPoint[0] < endPoint[0]:
                    coordinates1 = (startPoint[0] - 1, startPoint[1] - 1)
                    coordinates2 = (startPoint[0] - 1, startPoint[1] + 1)
                    if coordinates1 in neighbors:
                        self.addMove(self.directions.getUp())
                        self.addMove(self.directions.getLeft())
                    elif coordinates2 in neighbors:
                        self.addMove(self.directions.getUp())
                        self.addMove(self.directions.getRight())

    # It's a method that receives
    # -> blockPassed - list of the blocks passed in the DFS
    # -> startPoint - the point from where the function tries to form a square
    # -> n - the size of the square
    # and checks if from the point transmitted exists a path that forms a square.
    # OPTIONS -> -1 if none of the options below can be applied
    # 0 = [UP, RIGHT, DOWN, LEFT];
    # 1 = [UP, LEFT, DOWN, RIGHT];
    # 2 = [DOWN, RIGHT, UP, LEFT];
    # 3 = [DOWN, LEFT, UP, RIGHT];
    @staticmethod
    def searchForSquare(blockPassed, startPoint, n):
        line = 1  # the number of lines that the square needs to have
        block = 1  # the number of blocks that a line has
        option = 0  # is the moves that need to be done in order to make the square from the startPoint
        copyPoint = startPoint  # a copy of the startPoint
        while line < n:
            while block < n:
                if option >= 4:
                    return -1
                coordinate = (-1, -1)
                if line == 1:
                    if option == 0 or option == 1:      # UP
                        coordinate = (copyPoint[0] - 1, copyPoint[1])
                    elif option == 2 or option == 3:    # DOWN
                        coordinate = (copyPoint[0] + 1, copyPoint[1])
                elif line == 2:
                    if option == 0 or option == 2:      # RIGHT
                        coordinate = (copyPoint[0], copyPoint[1] + 1)
                    elif option == 1 or option == 3:    # LEFT
                        coordinate = (copyPoint[0], copyPoint[1] - 1)
                elif line == 3:
                    if option == 0 or option == 1:      # DOWN
                        coordinate = (copyPoint[0] + 1, copyPoint[1])
                    elif option == 2 or option == 3:    # UP
                        coordinate = (copyPoint[0] - 1, copyPoint[1])
                elif line == 4:
                    if option == 0 or option == 2:      # LEFT
                        coordinate = (copyPoint[0], copyPoint[1] - 1)
                    elif option == 1 or option == 3:    # RIGHT
                        coordinate = (copyPoint[0], copyPoint[1] + 1)
                if coordinate == (-1, -1) or not (coordinate in blockPassed):
                    option += 1
                    line = 1
                    block = 1
                else:
                    copyPoint = coordinate
                    if block + 1 == n:
                        if line + 1 == n:
                            return option
                        else:
                            line += 1
                            block = 1
                    else:
                        block += 1
        return -1

    def printMoves(self, moves):
        result = ""
        for move in moves :
            if move == 0 : result += "UP"
            elif move == 1 : result += "LEFT"
            elif move == 2 : result += "DOWN"
            elif move == 3 : result += "RIGHT"
            result += " ; "
        print("[ " + result + " ] - " + str(self.x) + " ; " + str(self.y))