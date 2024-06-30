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

    def main_menu(self):
        menu = Menu("Menu principal", {
            "Buscar Partidos": self.match_stadium_manager.menu,
            "Comprar Entrada": self.ticket_manager.sellTicket,
            "Chequear Entrada": self.ticket_manager.checkTicketMenu,
            # "Asistir al partido": 0,
            # "Estadisticas": 0,
        })

        menu.show()

program = Program()
program.main_menu()
