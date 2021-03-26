from lab2.model import Map, Drone
from random import randint
import time
import pygame
from pygame.locals import *


class ControllerClass:

    def __init__(self, repository, colors, directions, mapSize):
        self.repository = repository
        self.colors = colors
        self.directions = directions
        self.map = Map.MapClass(colors, directions, mapSize[0], mapSize[1])
        self.initializeMap()
        self.drone = self.positionDrone(mapSize[0], mapSize[1], colors, directions)
        self.pygameSetup()
        self.screen = self.screenSetup(colors.getWhiteColor())

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                pressedKeys = pygame.key.get_pressed()
                if event.type == pygame.QUIT:
                    print(self.repository.startPoint)
                    print(self.repository.endPoint)
                    running = False
                if event.type == KEYDOWN:
                    self.drone.move(self.map)
                if pressedKeys[K_s]:
                    self.repository.setStartPoint(self.drone.x, self.drone.y)
                    print("START POINT SET!")
                if pressedKeys[K_e]:
                    self.repository.setEndPoint(self.drone.x, self.drone.y)
                    print("END POINT SET!")
                if pressedKeys[K_SPACE]:
                    start = time.perf_counter()
                    pathA = self.repository.getAStarPath(self.map)
                    end = time.perf_counter()
                    print("Time A Star : " + str(end-start))
                    if len(pathA) == 1:
                        if pathA == ["NO PATH"]:
                            print("No path found")
                    else:
                        self.drawPath(pathA)
                        time.sleep(5)
                    start = time.perf_counter()
                    pathB = self.repository.getGreedyPath(self.map)
                    end = time.perf_counter()
                    print("Time Greedy : " + str(end - start))
                    if len(pathB) == 1:
                        if pathB == ["NO PATH"]:
                            print("No path found")
                    else:
                        self.drawPath(pathB)
                        time.sleep(5)


            self.screen.blit(self.drone.mapWithDrone(self.map.image()), (0, 0))
            pygame.display.flip()

        #path = self.repository.getDummyPath()
        #self.screen.blit(self.displayWithPath(self.map.image(), path), (0, 0))

        #pygame.display.flip()
        pygame.quit()

    def drawPath(self, path):
        self.screen.blit(self.displayWithPath(self.map.image(), path), (0, 0))
        pygame.display.flip()

    def initializeMap(self):
        self.map.randomMap()
        self.map.saveMap("test2.map")
        # self.map.loadMap("test1.map")

    def displayWithPath(self, image, path):
        mark = pygame.Surface((20, 20))
        mark.fill(self.colors.getGreenColor())
        for move in path:
            image.blit(mark, (move[1] * 20, move[0] * 20))

        return image

    def positionDrone(self, n, m, colors, directions):
        x = randint(0, n-1)
        y = randint(0, m-1)
        self.repository.setStartPoint(x,y)
        d = Drone.DroneClass(x, y, colors, directions)
        return d

    @staticmethod
    def screenSetup(colorFilling):
        screen = pygame.display.set_mode((400, 400))
        screen.fill(colorFilling)
        return screen

    @staticmethod
    def pygameSetup():
        pygame.init()
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Path in simple environment")

