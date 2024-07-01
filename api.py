import requests
import json
from data_objects import Team, Stadium, Match, Restaurant, RestaurantItem

def get_API_data():
    res_teams = requests.get('https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/teams.json')

    teams_data = res_teams.json()

    res_stadiums = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json")

    stadiums_data = res_stadiums.json()

    res_matches = requests.get('https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/matches.json')

    matches_data = res_matches.json()

    data = {
        "teams": teams_data,
        "stadiums": stadiums_data,
        "matches": matches_data,
    }

    with open("datos.txt", "w") as archivo: 
        json.dump(data, archivo, indent=4)

    print("Se guardaron los datos proveninentes de la api")

def getTeams():
    with open("datos.txt", "r") as archivo:
        raw_data = json.load(archivo)
    
    data = raw_data['teams']

    teams = []

    for i in data:
        teams.append(Team(i['id'], i['code'], i['name'], i['group']))

    return teams

def findTeam(teams, team_id):
    for t in teams:
        if(t.id == team_id):
            return t

def getStadiums():
    with open("datos.txt", "r") as archivo:
        raw_data = json.load(archivo)
    
    data = raw_data['stadiums']

    stadiums = []

    for s in data:
        stadium = Stadium(s['id'], s['name'], s['city'], s['capacity'])
        for r in s['restaurants']:
            restaurant = Restaurant(r['name'])
            for i in r['products']:
                product = RestaurantItem(i['name'], float(i['price']), i['stock'], i['adicional'])
                restaurant.products.append(product)

            stadium.restaurants.append(restaurant)

        stadiums.append(stadium)

    return stadiums

def findStadium(stadiums, stadium_id):
    for s in stadiums:
        if(s.id == stadium_id):
            return s

def getMatches(teams, stadiums):
    with open("datos.txt", "r") as archivo:
        raw_data = json.load(archivo)
    
    data = raw_data['matches']
    
    matches = []

    for m in data: 
        stadium = findStadium(stadiums, m['stadium_id'])
        home = findTeam(teams, m['home']['id'])
        away = findTeam(teams, m['away']['id'])
        match = Match(m['id'], m['number'], m['date'], m['group'], stadium, home, away)

        matches.append(match)

    return matches
