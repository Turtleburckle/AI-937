import pygame
import time
from pygame.locals import *


class MyControllerClass:

    def __init__(self, environment, dmap, drone, colors, directions, n):
        self.environment = environment
        self.myMap = dmap
        self.drone = drone
        self.colors = colors
        self.directions = directions
        self.n = n
        self.screen = self.initializePygame()

    def initializePygame(self):
        pygame.init()

        logo = pygame.image.load("lab1/logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("drone exploration")
        screen = pygame.display.set_mode((800, 400))
        screen.fill(self.colors.getWhiteColor())
        screen.blit(self.environment.image(), (0, 0))
        return screen

    def run(self):
        done = False
        running = self.drone.moveDSF(self.n, self.environment)
        if not running: print("No solution can be found!")
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == KEYDOWN and not done:
                    done = self.drone.doOneStep(self.myMap)
            self.myMap.markDetectedWalls(self.environment, self.drone.x, self.drone.y)
            self.screen.blit(self.myMap.image(self.drone.x, self.drone.y), (400, 0))
            pygame.display.flip()
        pygame.quit()
