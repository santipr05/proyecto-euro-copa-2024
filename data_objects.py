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
    def __init__(self, id, number, date, group, stadium, home, away) -> None:
        self.id = id
        self.number = number
        self.date = date
        self.group = group
        self.stadium = stadium
        self.home = home
        self.away = away
