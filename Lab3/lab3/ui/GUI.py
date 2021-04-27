import pygame
import time


class GuiClass:
    def __init__(self, colors, directions):
        self.colors = colors
        self.directions = directions
        self.speedOfDrone = 1
        self.screen = None

    # Setter for the speed of the Drone
    def setSpeedOfDrone(self, speedOfDrone):
        self.speedOfDrone = speedOfDrone

    # Shows the map that is currently loaded
    def showMap(self, map):
        self.initPyGame()
        screen = self.createSurface((400, 400))
        screen.blit(self.image(map.surface), (0, 0))
        screen.blit(self.mapWithDrone(self.image(map.surface), map.dronePosition), (0, 0))
        pygame.display.flip()
        self.closePyGame()

    # Initialises the PyGame
    @staticmethod
    def initPyGame():
        pygame.init()
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("drone exploration with AE")

    # Creates the surface on the screen that has the size of the dimension
    def createSurface(self, dimension):
        screen = pygame.display.set_mode(dimension)
        screen.fill(self.colors.getWhiteColor())
        return screen

    # Closes the PyGame when the user clicks the X button
    @staticmethod
    def closePyGame():
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()

    # Moves the drone based on the received path
    def movingDrone(self, path,  myMap):
        # Initialises the PyGame
        self.initPyGame()
        # Creates the screen
        self.screen = self.createSurface((myMap.n * 20, myMap.m * 20))

        for index in range(len(path)):
            newPath = []
            for index2 in range(index):
                newPath.append(path[index2])
            self.drawPath(newPath, myMap)
            time.sleep(0.5 * self.speedOfDrone)
            pygame.display.flip()
        self.closePyGame()

    # Puts the drone on the surface
    def mapWithDrone(self, mapImage, positionDrone):
        drona = pygame.image.load("drona.png")
        mapImage.blit(drona, (positionDrone[0] * 20, positionDrone[1] * 20))
        return mapImage


    def drawPath(self, path,map):
        mark = pygame.Surface((20, 20))
        mark.fill(self.colors.getGreenColor())
        image = self.image(map.surface)
        dronePosition = map.dronePosition
        for index in range(len(path)):
            if index < len(path) - 1:
                image.blit(mark, (path[index][0] * 20, path[index][1] * 20))
            else:
                drona = pygame.image.load("drona.png")
                image.blit(drona,(path[index][0] * 20, path[index][1]*20))
        self.screen.blit(image, (0, 0))
        pygame.display.flip()

    def displayWithPath(self, image, path):
        mark = pygame.Surface((20, 20))
        mark.fill(self.colors.getGreenColor())
        for move in path:
            image.blit(mark, (move[1] * 20, move[0] * 20))
        return image

    def image(self, currentMap):
        # creates the image of a map
        imagine = pygame.Surface((20 * 20, 20 * 20))
        brick = pygame.Surface((20, 20))
        brick.fill(self.colors.getBlueColor())
        imagine.fill(self.colors.getWhiteColor())
        for i in range(20):
            for j in range(20):
                if currentMap[i][j] == 1:
                    imagine.blit(brick, (j * 20, i * 20))
        return imagine
