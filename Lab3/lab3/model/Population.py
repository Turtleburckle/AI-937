from lab3.model import Individual


class PopulationClass:
    def __init__(self, individualSize, mutationProbability, crossoverProbability, myMap, battery):
        self.__individualSize = individualSize
        self.__mutationProbability = mutationProbability
        self.__crossoverProbability = crossoverProbability
        self.__myMap = myMap
        self.battery = battery
        self.individuals = []
        self.createIndividuals()
        self.parent1 = None
        self.parent2 = None

    # Generates the initial population of individuals.
    def createIndividuals(self):
        for index in range(self.__individualSize):
            newIndividual = Individual.IndividualClass(self.__mutationProbability,
                                                       self.__crossoverProbability,
                                                       self.__myMap,
                                                       self.battery)
            self.individuals.append(newIndividual)

    # Evaluates the fitness for each individual
    def evaluate(self):
        for individual in self.individuals:
            individual.fitness()


    def putOldPopulation(self, previousPopulation):
        self.sortIndividuals()
        previousPopulation.sort(reverse=True, key=self.myFunc)
        newIndividuals = []
        indexIndividual = 0
        indexPrevious = 0
        while len(newIndividuals) < self.__individualSize:
            if indexPrevious < len(previousPopulation):
                if self.individuals[indexIndividual].fitnessValue > previousPopulation[indexPrevious].fitnessValue:
                    newIndividuals.append(self.individuals[indexIndividual])
                    indexIndividual += 1
                elif self.individuals[indexIndividual].fitnessValue < previousPopulation[indexPrevious].fitnessValue:
                    newIndividuals.append(previousPopulation[indexPrevious])
                    indexPrevious += 1
                elif self.individuals[indexIndividual].fitnessValue == previousPopulation[indexPrevious].fitnessValue:
                    newIndividuals.append(self.individuals[indexIndividual])
                    newIndividuals.append(previousPopulation[previousPopulation])
                    indexIndividual += 1
                    indexPrevious += 1
            else:
                newIndividuals.append(self.individuals[indexIndividual])
                indexIndividual += 1
        self.individuals = newIndividuals


    def sortIndividuals(self):
        self.individuals.sort(reverse=True, key=self.myFunc)

    def myFunc(self, e):
        return e.fitnessValue


    # Selects the fittest two individuals from this population that area ready for reproduction
    def selection(self):
        self.sortIndividuals()
        self.parent1 = self.individuals[0]
        self.parent2 = self.individuals[1]

    # Realizes the crossover between the parents (two, most fittest, individuals)
    def crossoverParents(self):
        return self.parent1.crossover(self.parent2)

    # Getter for the first fittest parent (an individual from the population)
    def getParent1(self):
        return self.parent1

    # Getter for the second fittest parent (also an individual from the population)
    def getParent2(self):
        return self.parent2


