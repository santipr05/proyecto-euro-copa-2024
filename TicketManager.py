from utils import inputInt, isVapireNumber
from Menu import Menu
from data_objects import Ticket

class TicketManager:
    def __init__(self, matchManager) -> None:
        self.tickets = []
        self.assists = []
        self.matchManager = matchManager
        self.seating = {}
        self.pageSize = 8
        self.code = 0

    def occupied_seat(self, row, col):
        for t in self.tickets:
            if t.row == row and t.col == col:
                return True
        return False

    def sellTicket(self):
        name = input("Ingrese su nombre: ")
        ci = inputInt("Ingrese su cedula: ")
        age = inputInt("Ingrese su edad: ")

        menuPartido = Menu("Elejir partido", {
            "Buscar por pais": None,            
            "Buscar por estadio": None,            
            "Buscar por fecha": None,            
        })

        print("\nElejir partido")

        selection = -1

        matches = []
        selectedMatch = None
        while True:
            while selection == -1:
                selection = menuPartido.promt(exitOption=False)

            if(selection == 1):
                stadium = input("Escriba el pais: ")
                matches = self.matchManager.searchByCountry(stadium)
                if(len(matches) == 0):
                    print("La busqueda no tubo resultados.")
                    continue

            if(selection == 2):
                stadium = input("Escriba el estadio: ")
                matches = self.matchManager.searchByStadium(stadium)
                if(len(matches) == 0):
                    print("La busqueda no tubo resultados.")
                    continue

            if(selection == 3):
                date = input("Introduzca la fecha (año-mes-dia): ")
                matches = self.matchManager.searchByDate(date)
                if(len(matches) == 0):
                    print("La busqueda no tubo resultados.")
                    continue

            matchesMenu = Menu("", {x.__str__(): None for x in matches})

            selection = matchesMenu.promt()

            # La persona canceló
            if selection != 4 and selection != -1:
                selectedMatch = matches[selection - 1]
                break

            selection = -1

        row, col = 0, 0
        validRow = False
        validCol = False
        taken = True

        capacity = selectedMatch.stadium.capacity

        while taken:
            while not validRow:
                row = inputInt(f"Indique la fila, 0-{capacity[1]}: ")
                if row < 0 and row > capacity[1]:
                    print("Fila invalida.")
                else:
                    validRow = True

            while not validCol:
                col = inputInt(f"Indique la columna, 0-{capacity[0]}: ")
                if col < 0 and col > capacity[0]:
                    print("Columna invalida")
                else:
                    validCol = True

            if self.occupied_seat(row, col):
                print("El asiento ya esta ocupado.")
            else:
                taken = False


        isVip = input("Desea comprar una entrada Vip (si, no): ")
        vip = isVip.lower() == "si"

        self.code += 1
        ticket = Ticket(name, ci, age, selectedMatch, vip, row, col, self.code)

        cost = ticket.getCost()
        print(f"Subtotal: {cost}")
        if(isVapireNumber(ci)):
            print("Su numero de cedula es vampiro! Obtiene un 50% de descuento")
            cost = cost * 0.5

        print(f"IVA: {cost * 0.16}")
        print(f"TOTAL: {ticket.calculateCost()}")

        print("")

        confirmation = input("Desea comprar la entrada (si, no): ")
        bought = confirmation.lower() == 'si'

        if bought:
            self.tickets.append(ticket)
            print("Gracias por su compra")
            print("Su codigo de ticket es: ", ticket.code)

    def checkTicket(self, ticket_id):
        found = False
        for t in self.tickets:
            if t.code == ticket_id:
                found = True
                break

        if not found:
            return False
            
        if ticket_id in self.assists:
            return False

        return True

    def checkTicketMenu(self):
        ticket_id = input("Ingrese el codigo del ticket: ")
        if(self.checkTicket(ticket_id)):
            print("Su Ticket es valido")
        else:
            print("Su ticket es invalido.")
