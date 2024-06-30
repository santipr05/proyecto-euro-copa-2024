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

