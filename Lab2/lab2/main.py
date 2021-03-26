import pickle
from random import randint
import pygame
import time
from pygame.locals import *

from lab2.controller import Controller
from lab2.model import Colors, Directions, Map
from lab2.repository import Repository


def main():
    colors = Colors.ColorsClass()
    directions = Directions.DirectionsClass()
    n = 20
    m = 20
    mapSize = (n, m)
    repository = Repository.RepositoryClass()
    controller = Controller.ControllerClass(repository, colors, directions, mapSize)
    controller.run()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
