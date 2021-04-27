import statistics
from copy import deepcopy

from lab3.model import Population, Individual


class ControllerClass:
    def __init__(self, repository):
        self.repository = repository
        self.numberOfRuns = 100
        self.averageFitness = []
        self.maximumFitness = []
        self.bestSolution = None

    # Getter for the Average Fitness (a list of the average fitness for each population's individuals)
    def getAverage(self):
        return self.averageFitness

    # Getter for the Maximum Fitness (a list of the maximum fitness from each population)
    def getMaximum(self):
        maximumList = []
        for individual in self.maximumFitness:
            maximumList.append(individual.fitnessValue)
        return maximumList

    # Getter for the best individual (the fittest individual from all populations)
    def getBest(self):
        print(self.bestSolution.getGenePath())
        return self.bestSolution.fitnessValue

    # Getter for the path of the best individual
    def getPath(self):
        return self.bestSolution.getGoodPath()

    # Iteration does a set of iterations for each population:
    # -> creates the population firstly
    # -> evaluates the individuals of this population
    # -> selects the fittest two members (individuals) of the population
    # -> crossovers the genes of these two members (parents) creating the offsprings
    # -> mutates the offsprings (the crossover results of the two parents)
    # -> adds the mutated offsprings to the set of new population.
    def iteration(self):
        newPopulation = []
        for population in range(self.repository.populationSize):
            self.repository.createPopulation()
            self.repository.evaluatePopulation()
            self.repository.selectFittestPopulation()
            offspring1, offspring2 = self.repository.getCrossover()
            offspring1.mutation()
            offspring2.mutation()
            newPopulation.append(offspring1)
            newPopulation.append(offspring2)
        self.repository.setNewPopulation(newPopulation)

    # For each run the program does an iteration and after that generates the statistics for each run.
    # The statistics contains:
    # -> the average fitness for each population
    # -> the maximum fitness for each population
    # -> the best solution between all populations
    def run(self):
        for run in range(self.numberOfRuns):
            self.iteration()
            averageFitnessCurrent = 0
            sizePopulation = 0
            maxIndividual = None
            for population in self.repository.getPopulations():
                averageFitnessCurrent += population.fitnessValue
                sizePopulation += 1
                if self.bestSolution is None:
                    self.bestSolution = population
                if maxIndividual is None:
                    maxIndividual = population
                elif population.fitnessValue > maxIndividual.fitnessValue:
                    maxIndividual = population
            self.maximumFitness.append(maxIndividual)
            self.averageFitness.append(averageFitnessCurrent / sizePopulation)
        for individual in self.maximumFitness:
            if self.bestSolution is None:
                self.bestSolution = individual
            elif self.bestSolution.fitnessValue < individual.fitnessValue:
                self.bestSolution = individual

    # The solver triggers the run
    def solver(self):
        self.run()

    # Calls the Repository's create random map method.
    def createRandomMap(self):
        self.repository.createRandomMap()

    # Calls the Repository's load map method
    # Receives : -> nameFile : string - the name of the file we want to load (default : "test.map")
    def loadMap(self, nameFile="test.map"):
        self.repository.loadMap(nameFile)

    # Calls the Repository's save map method
    # Receives : -> nameFile : string - the name of the file we want to save the map to (default : "randomMap.map")
    def saveMap(self, nameFile="randomMap.map"):
        self.repository.saveMap(nameFile)

    # Getter for the map from the Repository
    def getMap(self):
        return self.repository.getMap()

    #  Triggers the setter for the battery from the Repository
    def setBattery(self, battery):
        self.repository.setBattery(battery)

    # Setter for the number of runs
    def setNumberOfRuns(self, numberOfRuns):
        self.numberOfRuns = numberOfRuns

    # Triggers the setter for the population size from the Repository
    def setPopulationSize(self, populationSize):
        self.repository.setPopulationSize(populationSize)

    # Triggers the setter for the individual size from the Repository
    def setIndividualSize(self, individualSize):
        self.repository.setIndividualSize(individualSize)

    # Triggers the setter for the mutation probability from the Repository
    def setMutationProbability(self, mutationProbability):
        self.repository.setMutationProbability(mutationProbability)

    # Triggers the setter for the crossover probability from the Repository
    def setCrossoverProbability(self, crossoverProbability):
        self.repository.setCrossoverProbability(crossoverProbability)
