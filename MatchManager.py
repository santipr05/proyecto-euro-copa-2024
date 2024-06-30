from utils import printDebugInfo
from Menu import Menu

class MatchStadiumManager:
    """Maneja la informacion de los partidos"""

    def __init__(self, stadiums, matches) -> None:
        self.stadiums = stadiums
        self.matches = matches

    def searchByCountry(self, country_name):
        """Busca los partidos de un pais específico"""

        results = []
        for match in self.matches:
            if country_name in match.home.name :
                results.append(match)
            elif country_name in match.away.name:
                results.append(match)
        return results

    def searchByStadium(self, stadium_name):
        """Busca los partidos por un estadio especifico"""

        results = []
        for match in self.matches:
            if stadium_name in match.stadium.name:
                results.append(match)
        return results

    def searchByDate(self, date):
        """Busca los partidos por una fecha especifica"""

        results = []
        for match in self.matches:
            if date in match.date:
                results.append(match)
        return results

    def searchByCountryMenu(self):
        """Muestra la entrada para buscar los partidos por pais"""

        country = input("Escriba el pais: ")
        matches = self.searchByCountry(country)
        print(f"Resultados para el pais {country}")
        for match in matches:
            print("\t", match)

    def searchByStadiumMenu(self):
        """Muestra la entrada para buscar los partidos por estadio"""

        stadium = input("Escriba el estadio: ")
        matches = self.searchByStadium(stadium)
        print(f"Resultados para el estadio {stadium}")
        for match in matches:
            print("\t", match)

    def searchByDateMenu(self):
        """Muestra la entrada para buscar los partidos por fecha"""

        date = input("Introduzca la fecha (año-mes-dia): ")
        matches = self.searchByDate(date)
        print(f"Resultados para la fecha: {date}")
        for match in matches:
            print("\t", match)

    def menu(self):
        """Muesta el menu para buscar partidos"""

        printDebugInfo("Match Stadium Manager")

        menu = Menu("Buscar Partidos", {
            "Buscar por pais": self.searchByCountryMenu,
            "Buscar por estadio": self.searchByStadiumMenu,
            "Buscar por fecha": self.searchByDateMenu,
        })
        menu.show()
