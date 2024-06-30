import requests
import math
from data_objects import Team, Stadium, Match, Restaurant, RestaurantItem

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



# teams = getTeams()
# stadiums = getStadiums()
# matches = getMatches(teams, stadiums)
#
# matchStadiumManager = MatchStadiumManager(stadiums, matches)


def isVapireNumber(n):
    n_digits = math.ceil(math.log10(n))
    digits = []
    permutation = []

    for i in range(n_digits):
        permutation.append(-1)

    if not n_digits % 2 == 0:
        return False

    def buildNumber(digits):
        result = 0;
        for d in digits:
            result = result * 10 + d

        return result

    def isVampire(digits):
        half = math.floor(len(digits)/2)
        a = buildNumber(digits[:half])
        b = buildNumber(digits[half:])
        if(a * b == n):
            return True

    def permutate(digit = 0):
        if not digit < n_digits:
            return isVampire(permutation)

        for i in range(n_digits):
            if i in permutation:
                continue
            permutation[digit] = digits[i]
            if permutate(digit + 1):
                return True
            permutation[digit] = -1

        return False

    for i in range(n_digits):
        digits.append(math.floor(n / math.pow(10, i)) % 10)

    return permutate()
