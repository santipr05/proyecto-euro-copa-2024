class Team :
    def __init__(self, id, code, name, group) -> None:
        self.id = id
        self.code = code
        self.name = name
        self.group = group


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
