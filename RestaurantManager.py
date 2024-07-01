from Menu import Menu
from utils import isPerfectNumber

class RestaurantManager:
    def __init__(self, stadiums) -> None:
        self.stadiums = stadiums
        pass

    def sellProduct(self, ticket):
        stadium = ticket.match.stadium

        restaurant_menu = Menu("Restaurante", {x.name: None for x in stadium.restaurants })
        
        # Seleccionar restaurante
        selected_restaurant = None
        selection = -1

        while selection == -1:
            selection = restaurant_menu.promt()
            if selection == len(restaurant_menu.actions) + 1: 
                break
            selected_restaurant = stadium.restaurants[selection - 1]

        # Seleccionar producto 
        products = []
        menuBusquda = Menu("Buscar productos", {
            "Buscar por nombre": None,
            "Buscar por tipo": None,
            "Buscar por rango de precio": None,
        })

        selected_product = None

        selection = -1

        while True:
            while selection == -1:
                selection = menuBusquda.promt(exitOption=False)

            if selection == 1:
                product_name = input("Ingrese el nombre del producto: ")
                products = self.search_product_by_name(selected_restaurant, product_name)
                if(len(products) == 0):
                    print("La busqueda no tubo resultados.")
                    continue

            if selection == 2:
                plate_type_menu = Menu("", {
                    "Plato": None,
                    "Bebida no alcoholica": None,
                    "Bebida alcolica": None,
                })

                print("Ingrese el nombre del tipo de producto: ")
                selected_type = plate_type_menu.promt(exitOption=False)
                if selected_type == -1 or selected_type == 4:
                    continue

                products = self.search_product_by_type(selected_restaurant, selected_type)
                if(len(products) == 0):
                    print("La busqueda no tubo resultados.")
                    continue

            if selection == 3:
                top_price = input("Ingrese el precio maximo: ")
                bottom_price = input("Ingrese el precio minimo: ")
                products = self.search_product_by_price_range(selected_restaurant, top_price, bottom_price)
                if(len(products) == 0):
                    print("La busqueda no tubo resultados.")
                    continue

            productsMenu = Menu("", {x.__str__(): None for x in products})

            selection = productsMenu.promt()

            if selection != len(productsMenu.actions)+1 and selection != -1:
                selected_product = products[selection - 1]
                break

            selection = -1

        cost = selected_product.price
        descuento = 0
        if isPerfectNumber(ticket.ci):
            descuento = cost * 0.15
            print("Obtuvo un 15% de descuento")

        print(f"Producto: {selected_product.name}")
        print(f"Subtotal: {cost}")
        print(f"Descuento: {descuento}")
        cost = cost - descuento
        print(f"TOTAL: {cost}")

        comprar = input("Desea comprar el producto (si, no): ")
        if(comprar.lower() == "si"):
            print("Gracias por su compra")
            selected_product.stock -= 1

    def search_product_by_name(self, restaurant, product_name):
        results = []
        for p in restaurant.products:
            if product_name in p.name:
                results.append(p)

        return results

    def search_product_by_type(self, restaurant, product_type):
        results = []
        for p in restaurant.products:
            if product_type == 1 and p.isFood: # plate
                results.append(p)

            if product_type == 2 and p.isAlcoholic: # alcoholic
                results.append(p)

            if product_type == 3 and not p.isFood and not p.isAlcoholic: # non-alcoholic
                results.append(p)

        return results

    def search_product_by_price_range(self, restaurant, top_price, bottom_price):
        results = []
        for p in restaurant.products:
            if p.price <= top_price and p.price >= bottom_price:
                results.append(p)
        return results

