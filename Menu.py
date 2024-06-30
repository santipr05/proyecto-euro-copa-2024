from utils import inputInt

class Menu:
    def __init__(self, title, actions):
        self.actions = actions
        self.title = title

    def printTitle(self):
        print()
        print("-" * (len(self.title) + 4))
        print(f"| {self.title} |")
        print("-" * (len(self.title) + 4))


    def promt(self, exitOption = True, exitText = "Salir"):

        selection = -1

        maxOptionNumber = len(self.actions)
        if(exitOption):
            maxOptionNumber += 1

        if self.title != "":
            self.printTitle()

        i = 1
        for k, _ in self.actions.items():
            print(f"{i}. {k}")

            i += 1

        if(exitOption):
            print(f"{i}. {exitText}")

        selection = inputInt("Seleccione una opcion: ", "Opcion invalida.")

        if selection <= 0 or selection > maxOptionNumber:
            print("Opcion invalida.")
            return -1
        
        return selection

    def show(self):
        selection = 0

        while selection != len(self.actions) + 1:
            selection = self.promt()
            if selection == -1:
                continue

            if selection != len(self.actions) + 1:
                key = list(self.actions)[selection - 1]
                self.actions[key]()
