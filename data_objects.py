import math

from utils import isVapireNumber

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
    def __init__(self, id, number, date, group, stadium, home, away) -> None:
        self.id = id
        self.number = number
        self.date = date
        self.group = group
        self.stadium = stadium
        self.home = home
        self.away = away

class Ticket:
    def __init__(self, name, ci, age, match, vip, row, col, code) -> None:
        self.name = name
        self.ci = ci
        self.age = age
        self.match = match
        self.vip = vip
        self.row = row
        self.col = col
        self.code = code
        self.cost = self.getCost()

    def getCost(self) -> float:
        cost = 35
        if self.vip:
            cost = 75

        if isVapireNumber(self.ci):
            cost = cost * 0.5
        
        # Sumar el iva
        cost = cost * 0.16

        return cost
