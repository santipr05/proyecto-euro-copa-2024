import requests
from utils import printDebugInfo
from Menu import Menu
from MatchManager import MatchStadiumManager
from TicketManager import TicketManager
from RestaurantManager import RestaurantManager
import api


class Program:
    debug = True

    def __init__(self) -> None:
        printDebugInfo("Obteniendo datos de la api")
        try:
            self.teams = api.getTeams()
            self.stadiums = api.getStadiums()
            self.matches = api.getMatches(self.teams, self.stadiums)
        except requests.exceptions.ConnectionError:
            print("Error de coneccion: No se pudo obtener los datos de la api")

        # TODO: Guardar datos en archivos de texto

        self.match_stadium_manager = MatchStadiumManager(self.stadiums, self.matches)
        self.ticket_manager = TicketManager(self.match_stadium_manager)
        self.restaurant_manager = RestaurantManager(self.stadiums)

    def attend_to_match(self):
        ticket_id = input("Ingrese el codigo de su ticket: ")
        if not self.ticket_manager.checkTicket(ticket_id):
            print("El ticket es invalido")
            return
        
        ticket = self.ticket_manager.register_assist(ticket_id)

        print(ticket)

        if ticket == None:
            return
        
        if not ticket.vip:
            print("No es un usuario VIP, no puede comprar en el restarurante")
            return

        menu = Menu("Restaurante", {
            "Comprar en restaurante": None
        })

        selection = -1
        while selection == -1:
            selection = menu.promt()
            self.restaurant_manager.sellProduct(ticket)
            if selection == 2:
                break

        menu.show()

    def main_menu(self):
        menu = Menu("Menu principal", {
            "Buscar Partidos": self.match_stadium_manager.menu,
            "Comprar Entrada": self.ticket_manager.sellTicket,
            "Chequear Entrada": self.ticket_manager.checkTicketMenu,
            "Asistir al partido": self.attend_to_match,
            # "Estadisticas": 0,
        })

        menu.show()

program = Program()
program.main_menu()
