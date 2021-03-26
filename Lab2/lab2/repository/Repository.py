from queue import PriorityQueue

import numpy as np


class RepositoryClass:

    def __init__(self, x=0, y=0):
        self.startPoint = (x, y)
        self.endPoint = self.startPoint

    def setStartPoint(self, x, y):
        self.startPoint = (x, y)

    def setEndPoint(self, x, y):
        self.endPoint = (x, y)

    def searchAStar(self, myMap):
        openList = []
        closedList = []
        cellsDistance = self.getCellsDistance(myMap)
        cellsPrevious = self.getCellsPrevious(myMap)
        distanceFromStartPoint = 0

        currentCell = self.startPoint
        openList.append(self.startPoint)
        closedList.append(self.startPoint)
        while len(openList) != 0:
            if currentCell != self.startPoint:
                distanceFromStartPoint = cellsDistance[currentCell[0], currentCell[1]]
            if currentCell == self.endPoint:
                path = self.generatePath(cellsPrevious)
                path.append(currentCell)
                return path
            neighbors = self.getNeighbors(currentCell, myMap)
            bestF = 999999
            bestCell = (-1, -1)
            for neighbor in neighbors:
                if not (neighbor in closedList):
                    currentF = distanceFromStartPoint + self.getHeuristicValue(neighbor)
                    if bestF > currentF:
                        bestF = currentF
                        bestCell = neighbor
                    if not (neighbor in openList):
                        openList.append(neighbor)
                        if cellsPrevious[neighbor[0]][neighbor[1]] == (-1, -1):
                            cellsPrevious[neighbor[0]][neighbor[1]] = currentCell
                            cellsDistance[neighbor[0]][neighbor[1]] = distanceFromStartPoint + 1
                    elif neighbor in openList:
                        if cellsDistance[neighbor[0]][neighbor[1]] < distanceFromStartPoint:
                            closedList.append(currentCell)
                        elif cellsDistance[neighbor[0]][neighbor[1]] > distanceFromStartPoint:
                            cellsDistance[neighbor[0]][neighbor[1]] = distanceFromStartPoint + 1
                            cellsPrevious[neighbor[0]][neighbor[1]] = currentCell
            if bestCell[0] != -1:
                currentCell = bestCell
                closedList.append(currentCell)
            else:
                currentCell = openList.pop()
        return ["NO PATH"]

    def getCellsPrevious(self, myMap):
        cells = []
        for index1 in range(myMap.n):
            cells.append([])
            for index2 in range(myMap.m):
                cells[index1].append((-1, -1))
        return cells

    def getCellsDistance(self, myMap):
        cells = np.zeros((myMap.n, myMap.m))
        return cells

    def getNeighbors(self, cell, myMap):
        result = []
        # UP
        up = (cell[0] - 1, cell[1])
        if up[0] >= 0:
            if myMap.surface[up[0], up[1]] != 1:
                result.append(up)
        # DOWN
        down = (cell[0] + 1, cell[1])
        if down[0] < myMap.n:
            if myMap.surface[down[0], down[1]] != 1:
                result.append(down)
        # LEFT
        left = (cell[0], cell[1] - 1)
        if left[1] >= 0:
            if myMap.surface[left[0], left[1]] != 1:
                result.append(left)
        # RIGHT
        right = (cell[0], cell[1] + 1)
        if right[1] < myMap.m:
            if myMap.surface[right[0], right[1]] != 1:
                result.append(right)
        return result

    def getHeuristicValue(self, currentPoint):
        xResult = 0
        yResult = 0
        if currentPoint[0] > self.endPoint[0]:
            xResult = currentPoint[0] - self.endPoint[0]
        elif currentPoint[0] < self.endPoint[0]:
            xResult = self.endPoint[0] - currentPoint[0]
        if currentPoint[1] > self.endPoint[1]:
            yResult = currentPoint[1] - self.endPoint[1]
        elif currentPoint[1] < self.endPoint[1]:
            yResult = self.endPoint[1] - currentPoint[1]
        result = np.sqrt(xResult * xResult + yResult * yResult)
        return result

    def getAStarPath(self, myMap):
        path = self.searchAStar(myMap)
        print(path)
        return path

    def searchGreedy(self, myMap):
        path = []
        visited = self.getCellsDistance(myMap)
        pq = PriorityQueue()
        pq.put((0,self.startPoint))
        while not pq.empty():
            u = pq.get()[1]
            path.append(u)
            if u == self.endPoint:
                return path
            neighbors = self.getNeighbors(u,myMap)
            for neighbor in neighbors:
                index1 = neighbor[0]
                index2 = neighbor[1]
                if visited[index1][index2] == 0:
                    visited[index1][index2] = 1
                    cell = (index1, index2)
                    priority = self.getHeuristicValue(cell)
                    pq.put((priority, cell))
        return ["NO PATH"]

    def getGreedyPath(self, myMap):
        path = self.searchGreedy(myMap)
        print(path)
        return path

    def generatePath(self, cells):
        path = []
        currentCell = self.endPoint
        while currentCell != self.startPoint:
            path.append(currentCell)
            currentCell = cells[currentCell[0]][currentCell[1]]
        return path
