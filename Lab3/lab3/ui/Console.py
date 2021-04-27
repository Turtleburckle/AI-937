import time
from matplotlib import pyplot

class ConsoleClass:
    def __init__(self, controller, gui):
        self.controller = controller
        self.gui = gui
        self.runTime = 0
        self.mapLoaded = False
        self.runMade = False

    # Runs the main console
    def runConsole(self):
        while True:
            self.printableMenu()
            command = input(">>> ")
            if command == "1":
                self.runMapMenu()
            elif command == "2":
                self.runEaMenu()
            else:
                quit()

    # Runs the map menu console
    def runMapMenu(self):
        while True:
            self.printableMapMenu()
            command = input(">>> ")
            if command == "a":
                self.controller.createRandomMap()
                self.mapLoaded = True
            elif command == "b":
                self.loadMap()
            elif command == "c":
                self.saveMap()
            elif command == "d":
                self.visualiseMap()
            elif command == "0":
                self.runConsole()
            else:
                quit()

    # Takes the name of the file we want to load and triggers the event from the Controller
    def loadMap(self):
        nameFile = input(">>> Map Name : ")
        self.controller.loadMap(nameFile)
        self.mapLoaded = True

    # Takes the name of the file we want to load and triggers the event from the Controller
    def saveMap(self):
        nameFile = input(">>> Map Name : ")
        self.controller.saveMap(nameFile)
        self.mapLoaded = True

    # Triggers the method that shows the map from the GUI
    def visualiseMap(self):
        if self.mapLoaded:
            self.gui.showMap(self.controller.getMap())
        else:
            print("No Map is loaded or generated!\n")

    # Runs the evolutionary algorithm menu console
    def runEaMenu(self):
        while True:
            self.printableEaMenu()
            command = input(">>> ")
            if command == "a":
                self.setUpParameters()
            elif command == "b":
                self.runSolver()
            elif command == "c":
                self.visualiseStatistics()
            elif command == "d":
                self.viewDroneMovingPath()
            elif command == "0":
                self.runConsole()
            else:
                quit()

    # Runs the set up parameters menu from the EA's menu console
    def setUpParameters(self):
        while True:
            self.printableParametersSetupMenu()
            command = input(">>> ")
            if command == "a":
                self.setBattery()
            elif command == "b":
                self.setNumberOfRuns()
            elif command == "c":
                self.setPopulationSize()
            elif command == "d":
                self.setIndividualSize()
            elif command == "e":
                self.setMutationProbability()
            elif command == "f":
                self.setCrossoverProbability()
            elif command == "g":
                self.setSpeedOfDrone()
            elif command == "0":
                self.runEaMenu()
            else:
                quit()

    # Reads the battery input and calls the Controller method that sets the battery level
    def setBattery(self):
        battery = int(input(">>> Battery : "))
        if battery != 0:
            self.controller.setBattery(battery)

    # Reads the number of runs and calls the method that sets it from the Controller
    def setNumberOfRuns(self):
        numberOfRuns = int(input(">>> Number of Runs : "))
        if numberOfRuns != 0:
            self.controller.setNumberOfRuns(numberOfRuns)

    # Reads the population size and calls the method that sets it from the Controller
    def setPopulationSize(self):
        populationSize = int(input(">>> Population Size : "))
        if populationSize != 0:
            self.controller.setPopulationSize(populationSize)

    # Reads the individual size and calls the method that sets it from the Controller
    def setIndividualSize(self):
        individualSize = int(input(">>> Individual Size : "))
        if individualSize != 0:
            self.controller.setIndividualSize(individualSize)

    # Reads the mutation probability and calls the method that sets it from the Controller
    def setMutationProbability(self):
        mutationProbability = float(input(">>> Mutation Probability : "))
        if mutationProbability != 0:
            self.controller.setMutationProbability(mutationProbability)

    # Reads the crossover probability and calls the method that sets it from the Controller
    def setCrossoverProbability(self):
        crossoverProbability = float(input(">>> Crossover Probability : "))
        if crossoverProbability != 0:
            self.controller.setCrossoverProbability(crossoverProbability)

    # Reads the speed of the drone and calls the method that sets it from the GUI
    def setSpeedOfDrone(self):
        speedOfDrone = float(input(">>> Speed of Drone : "))
        if speedOfDrone != 0:
            self.gui.setSpeedOfDrone(speedOfDrone)

    # Triggers the method run from the Controller
    def runSolver(self):
        start = time.perf_counter()
        self.controller.run()
        end = time.perf_counter()
        self.runTime = end-start
        self.runMade = True

    # Takes the statistics from the Controller after the run is made and prints them
    def visualiseStatistics(self):
        if self.runMade:
            average = self.controller.getAverage()
            maximum = self.controller.getMaximum()
            best = self.controller.getBest()
            x = []
            print("-------------------------------")
            print("|  It.  |   Avg.   |   Max.   |")
            print("-------------------------------")
            for index in range(len(average)):
                x.append(index+1)
                print("|  " + str(index+1) + "  |   " + str(average[index]) + "   |   " + str(maximum[index]) + "   |")
                print("-------------------------------")
            averageFitness = sum(average)/len(average)
            print("Average fitness: " + str(averageFitness))
            print("~~~~~~ Best fitness : " + str(best))
            print("Run Time : " + str(self.runTime))
            pyplot.plot(x,average)
            pyplot.xlabel('Iteration')
            pyplot.ylabel('Average fitness')
            pyplot.title('EA fitness')
            pyplot.show()
        else:
            print("No run was made, Statistics are empty!\n")

    # Takes the path from the Controller and calls the method that shows the move of the drone from the GUI
    def viewDroneMovingPath(self):
        if self.runMade:
            map = self.controller.getMap()
            path = self.controller.getPath()
            self.gui.movingDrone(path, map)
        else:
            print("No run was made!")

    # Prints the menu for the parameters setup
    @staticmethod
    def printableParametersSetupMenu():
        print("a. Battery -> Default : 20")
        print("b. Number of Runs -> Default : 100")
        print("c. Population Size -> Default : 100")
        print("d. Individual Size -> Default : 20")
        print("e. Mutation Probability -> Default : 0.04")
        print("f. Crossover Probability -> Default : 0.8")
        print("g. Speed of Drone -> Default : 1.0")
        print("0. BACK")

    # Prints the menu for the EA
    @staticmethod
    def printableEaMenu():
        print("a. parameters setup")
        print("b. run the solver")
        print("c. visualise the statistics")
        print("d. view the drone moving path")
        print("0. BACK")

    # Prints the menu for the map
    @staticmethod
    def printableMapMenu():
        print("a. create a Random Map")
        print("b. load a Map")
        print("c. save a Map")
        print("d. visualise Map")
        print("0. BACK")

    # Prints the main menu
    @staticmethod
    def printableMenu():
        print("_____Main Menu_____")
        print("1. Map Menu")
        print("2. EA Menu")
        print("0. EXIT")
        print("~Any other input will exit the App~")
