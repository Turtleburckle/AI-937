from lab3.model import Population


class RepositoryClass:
    def __init__(self, myMap):
        self.battery = 20
        self.populationSize = 100
        self.individualSize = 20
        self.mutationProbability = 0.04
        self.crossoverProbability = 0.8
        self.myMap = myMap
        self.population = None
        self.populations = []

    # Getter for the populations created
    def getPopulations(self):
        return self.populations

    # Sets the population with a new population list
    def setNewPopulation(self, populationList):
        self.populations.clear()
        self.populations = populationList

    # Triggers the crossover between the parents.
    def getCrossover(self):
        return self.population.crossoverParents()

    # Triggers the selection for the parents
    def selectFittestPopulation(self):
        self.population.selection()

    # Getter for the first, most fittest, parent from this population
    def getCurrentPopulationParent1(self):
        return self.population.getParent1()

    # Getter for the second, fittest, parent from this population
    def getCurrentPopulationParent2(self):
        return self.population.getParent2

    # Creates a population
    def createPopulation(self):
        self.population = Population.PopulationClass(self.individualSize,
                                                     self.mutationProbability,
                                                     self.crossoverProbability,
                                                     self.myMap,
                                                     self.battery)
        if len(self.populations) > 0:
            self.population.putOldPopulation(self.populations)

    # Triggers the evaluation of a population
    def evaluatePopulation(self):
        self.population.evaluate()

    # Triggers the method that randomise the map
    def createRandomMap(self, ):
        self.myMap.randomMap()

    # Triggers the load map method.
    def loadMap(self, nameFile):
        self.myMap.loadMap(nameFile)

    # Triggers the save method for the map
    def saveMap(self, nameFile):
        self.myMap.saveMap(nameFile)

    # Getter for the map
    def getMap(self):
        return self.myMap

    # Setter for the battery
    def setBattery(self, battery):
        self.battery = battery

    # Setter for the population size
    def setPopulationSize(self, newPopulationSize):
        self.populationSize = newPopulationSize

    # Setter for the individual size
    def setIndividualSize(self, newIndividualSize):
        self.individualSize = newIndividualSize

    # Setter for the mutation probability
    def setMutationProbability(self, newMutationProbability):
        self.mutationProbability = newMutationProbability

    # Setter for crossover probability
    def setCrossoverProbability(self, newCrossoverProbability):
        self.crossoverProbability = newCrossoverProbability
