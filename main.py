import requests

class Team :
    def __init__(self, id, code, name, group) -> None:
        self.id = id
        self.code = code
        self.name = name
        self.group = group

    def __str__(self) -> str:
        return f"(Team) id: {self.id}, name: {self.name}, code: {self.code}, group: {self.group}"


class RestaurantItem:
    def __init__(self, name, price, stock, aditional) -> None:
        self.name = name
        self.price = price
        self.stock = stock

        self.isFood = aditional == "plate"
        self.isAlcoholic = aditional == "alcoholic"


class Restaurant:
    def __init__(self, name) -> None:
        self.name = name
        self.products = []


class Stadium:
    def __init__(self, id, name, city, capacity) -> None:
        self.id = id
        self.name = name
        self.city = city
        self.capacity = capacity
        self.restaurants = []


class Match: 
    def __init__(self, id, number, date, group, home_id, away_id) -> None:
        self.id = id
        self.number = number
        self.date = date
        self.group = group
        self.home_id = home_id
        self.away_id = away_id

def getTeams():
    res = requests.get('https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/teams.json')
    if(res.status_code != 200):
        print("No se pudo obtener los datos de los equipos")
        return
    
    data = res.json()

    teams = []

    for i in data:
        teams.append(Team(i['id'], i['code'], i['name'], i['group']))

    print(teams[0])

    return teams

getTeams()
