from lab3.controller import Controller
from lab3.model import Map, Colors, Directions
from lab3.repository import Repository
from lab3.ui import Console, GUI


def main():
    myMap = Map.MapClass()
    repository = Repository.RepositoryClass(myMap)
    controller = Controller.ControllerClass(repository)
    colors = Colors.ColorsClass()
    directions = Directions.DirectionsClass()
    gui = GUI.GuiClass(colors,directions)
    console = Console.ConsoleClass(controller, gui)
    console.runConsole()


if __name__ == "__main__":
    main()
