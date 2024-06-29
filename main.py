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
    def __init__(self, id, name, city) -> None:
        self.id = id
        self.name = name
        self.city = city
        self.restaurants = []


class Match: 
    def __init__(self, id, number, date, group, stadium_id, home_id, away_id) -> None:
        self.id = id
        self.number = number
        self.date = date
        self.group = group
        self.stadium_id = stadium_id
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

def getStadiums():
    res = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json")
    if(res.status_code != 200):
        print("No se pudo obtener los datos de los equipos")
        return
    
    data = res.json()

    stadiums = []

    for s in data:
        stadium = Stadium(s['id'], s['name'], s['city'])
        for r in s['restaurants']:
            restaurant = Restaurant(r['name'])
            for i in r['products']:
                product = RestaurantItem(i['name'], i['price'], i['stock'], i['adicional'])
                restaurant.products.append(product)

            stadium.restaurants.append(restaurant)

        stadiums.append(stadium)

    print(stadiums[0].restaurants[0].products[0].name)
    return stadiums

def getMatches():
    res = requests.get('https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/matches.json')
    if(res.status_code != 200):
        print("No se pudo obtener los datos de los partidos")
        return
    
    data = res.json()

    matches: list[Match] = []

    for m in data: 
        match = Match(m['id'], m['number'], m['date'], m['group'], m['stadium_id'], m['home']['id'], m['away']['id'])

        matches.append(match)

    print(matches[0].away_id)
 
    return matches

getMatches()

