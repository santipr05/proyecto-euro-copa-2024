import requests
from data_objects import Team, Stadium, Match, Restaurant, RestaurantItem, Ticket
from utils import isVapireNumber

IS_DEV = True

def printDebugInfo(message):
    if IS_DEV:
        print(f"[Debug]: {message}")

def inputInt(propmt, errorMsg = "Ingrese un numero."):
    result = 0
    valid = False

    while not valid:
        try:
            result = int(input(propmt))
            valid = True
        except ValueError:
            print(errorMsg)

    return result

def getTeams():
    res = requests.get('https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/teams.json')
    if(res.status_code != 200):
        print("No se pudo obtener los datos de los equipos")
        return
    
    data = res.json()

    teams = []

    for i in data:
        teams.append(Team(i['id'], i['code'], i['name'], i['group']))

    return teams

def findTeam(teams, team_id):
    for t in teams:
        if(t.id == team_id):
            return t

def getStadiums():
    res = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json")
    if(res.status_code != 200):
        print("No se pudo obtener los datos de los equipos")
        return
    
    data = res.json()

    stadiums = []

    for s in data:
        stadium = Stadium(s['id'], s['name'], s['city'], s['capacity'])
        for r in s['restaurants']:
            restaurant = Restaurant(r['name'])
            for i in r['products']:
                product = RestaurantItem(i['name'], i['price'], i['stock'], i['adicional'])
                restaurant.products.append(product)

            stadium.restaurants.append(restaurant)

        stadiums.append(stadium)

    return stadiums

def findStadium(stadiums, stadium_id):
    for s in stadiums:
        if(s.id == stadium_id):
            return s

def getMatches(teams, stadiums):
    res = requests.get('https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/matches.json')
    if(res.status_code != 200):
        print("No se pudo obtener los datos de los partidos")
        return
    
    data = res.json()

    matches = []

    for m in data: 
        stadium = findStadium(stadiums, m['stadium_id'])
        home = findTeam(teams, m['home']['id'])
        away = findTeam(teams, m['away']['id'])
        match = Match(m['id'], m['number'], m['date'], m['group'], stadium, home, away)

        matches.append(match)

    return matches

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



class MatchStadiumManager:
    """Maneja la informacion de los partidos"""

    def __init__(self, stadiums, matches) -> None:
        self.stadiums = stadiums
        self.matches = matches

    def searchByCountry(self, country_name):
        """Busca los partidos de un pais específico"""

        results = []
        for match in self.matches:
            if country_name in match.home.name :
                results.append(match)
            elif country_name in match.away.name:
                results.append(match)
        return results

    def searchByStadium(self, stadium_name):
        """Busca los partidos por un estadio especifico"""

        results = []
        for match in self.matches:
            if stadium_name in match.stadium.name:
                results.append(match)
        return results

    def searchByDate(self, date):
        """Busca los partidos por una fecha especifica"""

        results = []
        for match in self.matches:
            if date in match.date:
                results.append(match)
        return results

    def searchByCountryMenu(self):
        """Muestra la entrada para buscar los partidos por pais"""

        country = input("Escriba el pais: ")
        matches = self.searchByCountry(country)
        print(f"Resultados para el pais {country}")
        for match in matches:
            print("\t", match)

    def searchByStadiumMenu(self):
        """Muestra la entrada para buscar los partidos por estadio"""

        stadium = input("Escriba el estadio: ")
        matches = self.searchByStadium(stadium)
        print(f"Resultados para el estadio {stadium}")
        for match in matches:
            print("\t", match)

    def searchByDateMenu(self):
        """Muestra la entrada para buscar los partidos por fecha"""

        date = input("Introduzca la fecha (año-mes-dia): ")
        matches = self.searchByDate(date)
        print(f"Resultados para la fecha: {date}")
        for match in matches:
            print("\t", match)

    def menu(self):
        """Muesta el menu para buscar partidos"""

        printDebugInfo("Match Stadium Manager")

        menu = Menu("Buscar Partidos", {
            "Buscar por pais": self.searchByCountryMenu,
            "Buscar por estadio": self.searchByStadiumMenu,
            "Buscar por fecha": self.searchByDateMenu,
        })
        menu.show()

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

class RestaurantManager:
    def __init__(self, stadiums) -> None:
        self.stadiums = stadiums
        pass

    def sellTicket(self):
        # TODO: Crear menú
        pass


    def search_product_by_name(self, restaurant, product_name):
        for p in restaurant.products:
            if product_name in p:
                return p

    def seach_product_by_type(self, restaurant, product_type):
        results = []
        for p in restaurant.products:
            if product_type == 'plate' and p.isFood:
                results.append(p)

            if product_type == 'alcoholic' and p.isAlcoholic:
                results.append(p)

            if product_type == 'non-alcoholic' and not p.isFood and not p.isAlcoholic:
                results.append(p)

        return results

    def seach_product_by_price_range(self, restaurant, top_price, bottom_price):
        results = []
        for p in restaurant.products:
            if p.price <= top_price and p.price >= bottom_price:
                results.append(p)

class Program:
    debug = True

    def __init__(self) -> None:
        printDebugInfo("Obteniendo datos de la api")
        try:
            self.teams = getTeams()
            self.stadiums = getStadiums()
            self.matches = getMatches(self.teams, self.stadiums)
        except requests.exceptions.ConnectionError:
            print("Error de coneccion: No se pudo obtener los datos de la api")

        # TODO: Guardar datos en archivos de texto

        self.match_stadium_manager = MatchStadiumManager(self.stadiums, self.matches)
        self.ticket_manager = TicketManager(self.match_stadium_manager)
        self.restaurant_manager = RestaurantManager(self.stadiums)

    def main_menu(self):
        menu = Menu("Menu principal", {
            "Buscar Partidos": self.match_stadium_manager.menu,
            "Comprar Entrada": self.ticket_manager.sellTicket,
            "Chequear Entrada": self.ticket_manager.checkTicketMenu,
            # "Asistir al partido": 0,
            # "Estadisticas": 0,
        })

        menu.show()

program = Program()
program.main_menu()
