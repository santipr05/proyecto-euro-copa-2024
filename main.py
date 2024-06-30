import requests
from data_objects import Team, Stadium, Match, Restaurant, RestaurantItem, Ticket

def printDebugInfo(message):
    print(f"[Debug]: {message}")

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
        print("-" * (len(self.title) + 4))
        print(f"| {self.title} |")
        print("-" * (len(self.title) + 4))


    def display(self):

        selection = 0

        while selection != len(self.actions) + 1:
            self.printTitle()
            i = 1
            for k, _ in self.actions.items():
                print(f"{i}. {k}")

                i += 1

            print(f"{i} Salir")

            selection = int(input("Seleccione una opcion: "))

            if selection <= 0 or selection > len(self.actions) + 1:
                print("Opcion invalida.")
                continue

            if selection != len(self.actions) + 1:
                key = list(self.actions)[selection - 1]
                self.actions[key]()


# TODO: Hacer Menu
class MatchStadiumManager:
    def __init__(self, stadiums, matches) -> None:
        self.stadiums = stadiums
        self.matches = matches

    def searchByCountry(self, country_name):
        results = []
        for match in self.matches:
            if country_name in match.home.name :
                results.append(match)
            elif country_name in match.away.name:
                results.append(match)
        return results

    def searchByStadium(self, stadium_name):
        results = []
        for match in self.matches:
            if stadium_name in match.stadium.name:
                results.append(match)
        return results

    def searchByDate(self, date):
        results = []
        for match in self.matches:
            if date in match.date:
                results.append(match)
        return results

    def menu(self):
        printDebugInfo("Match Stadium Manager")

        menu = Menu("Buscar Partidos", {})
        menu.display()

class TicketManager:
    def __init__(self, matches) -> None:
        self.tickets = []
        self.assists = []
        self.matches = matches
        self.seating = {}

    def sellTicket(self):
        # TODO: Crear menu
        pass

    def checkTicket(self, ticket_id):
        found = False
        for t in self.tickets:
            if t.id == ticket_id:
                found = True
                break

        if not found:
            return False
            
        if ticket_id in self.assists:
            return False

        return True

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
        self.ticket_manager = TicketManager(self.matches)
        self.restaurant_manager = RestaurantManager(self.stadiums)

    def main_menu(self):
        menu = Menu("Menu principal", {
            "Buscar Partidos": self.match_stadium_manager.menu,
            # "Comprar Entrada": 0,
            # "Chequear Entrada": 0,
            # "Asistir al partido": 0,
            # "Estadisticas": 0,
        })

        menu.display()


program = Program()
program.main_menu()
