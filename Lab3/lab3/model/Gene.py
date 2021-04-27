from random import *


class GeneClass:
    # The gene is a random generated set of moves for the drone.
    def __init__(self):
        self.__gene = []

    # The random generator.
    # -> size : integer - the battery level which represents how many moves a drone can make
    def generateRandomGene(self, size):
        for index in range(size):
            self.__gene.append(randint(0, 3))

    # The getter for the gene set.
    # -> gene : Set of integers - containing directions from DirectionsClass
    def getGene(self):
        return self.__gene
