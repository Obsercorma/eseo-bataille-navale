from tabulate import tabulate
from enum import Enum
from re import match

CLEAR_CHR = "\x1b[2J"

class Ship:
    def __init__(self, coords: list[str], profondeur: str, taille: int, joueur: str):
        self.joueur = joueur
        self.coords = coords
        self.taille = taille
        self.profondeur = profondeur
        self.touches = []

    def est_coule(self):
        return len(self.touches) == self.taille

class Joueur:
    def __init__(self, name: str):
        self.name = name
        self.ships = []
        self.grill100 = Grid()
        self.grill200 = Grid()
        self.grill300 = Grid()

    def ajouter_ship(self, ship: Ship):
        self.ships.append(ship)

# Définition des cas possibles dans une case sur la grille
class CellCase(Enum):
    TARGET_UNKNOWN = "*"
    # Aucun batiment dans cette case
    TARGET_NOTHING = "R"
    # Batiment repéré
    TARGET_FOUND = "V"
    # Batiment touché
    TARGET_HIT = "T"
    # Batiment détruit
    TARGET_DESTROYED = "C"

    def __str__(self):
        return self.value

class Grid:
    NUMBER_OF_COLS = 10
    NUMBER_OF_ROWS = 5
    CHR_START_INDEX = 65  # 'A'

    def __init__(self):
        self.cells = []
        self._chrEndCol = chr(self.CHR_START_INDEX + self.NUMBER_OF_ROWS - 1)
        self.headers = [
            hName if hName != 0 else " " for hName in range(self.NUMBER_OF_COLS)
        ]
        self.cells = [
            [
                "*" if col != 0 else chr(self.CHR_START_INDEX + row)
                for col in range(self.NUMBER_OF_COLS)
            ]
            for row in range(self.NUMBER_OF_ROWS)
        ]

    def __str__(self) -> str:
        print(CLEAR_CHR)
        print("|\tGrille{}\t|")
        print(
            tabulate(
                headers=self.headers,
                tabular_data=self.cells,
                tablefmt="rounded_grid",
                stralign="center",
            ),
        )
        return ''

    def affect_other_depths(self, profondeur: str, coord: str, joueur: Joueur, cell: CellCase) -> None:
        other_depths = ['100', '200', '300']
        other_depths.remove(profondeur)
        if profondeur == '100':
            other_depths.remove('300')
        if profondeur  == '300':
            other_depths.remove('100')

        for depth in other_depths:
            dico_Grilles = {
                '100': joueur.grill100, '200': joueur.grill200, '300': joueur.grill300}
            dico_Grilles[depth].fireOnTarget(coord, cell)

    def cases_affected(self, profondeur:str, coord: str, joueur: Joueur) -> None:
        dico_Grilles = {
            '100': joueur.grill100, '200': joueur.grill200, '300': joueur.grill300}
        for ships in joueur.ships:
            if ships.profondeur == profondeur:
                for ship_coord in ships.coords:
                    if ship_coord == coord:
                        ships.touches.append(coord)
                        dico_Grilles[profondeur].fireOnTarget(coord, CellCase.TARGET_HIT)
                        if ships.est_coule():
                            for sunk_coord in ships.coords:
                                dico_Grilles[profondeur].fireOnTarget(sunk_coord, CellCase.TARGET_DESTROYED)
                            print(f"Le navire de taille {ships.taille} du joueur {joueur.name} a été coulé !")
                        return

                row, col = coord[0], coord[1]
                #construction des coordonnées entourant la cible
                adjacent_coords = [coord,
                    f"{chr(ord(row)-1)}{col}",  # au-dessus
                    f"{chr(ord(row)+1)}{col}",  # en-dessous
                    f"{row}{int(col)-1}",       # à gauche
                    f"{row}{int(col)+1}"        # à droite
                ]
                for adjacent in adjacent_coords:
                    for ships.coord in ships.coords:
                        if adjacent == ships.coord:
                            for adjacent2 in adjacent_coords:
                                if '@' not in adjacent2:
                                    dico_Grilles[profondeur].fireOnTarget(adjacent2, CellCase.TARGET_FOUND)
                                dico_Grilles[profondeur].affect_other_depths(profondeur, coord, joueur, CellCase.TARGET_FOUND)
                            return
                for adjacent in adjacent_coords:
                    if '@' not in adjacent:
                        dico_Grilles[profondeur].fireOnTarget(adjacent, CellCase.TARGET_NOTHING)
                    dico_Grilles[profondeur].affect_other_depths(profondeur, coord, joueur, CellCase.TARGET_NOTHING)
                return






    def fireOnTarget(self, coords: str, cellCase: CellCase) -> list[Ship]:
        regex = "^[A-endChr1]{1}[1-endRow]{1}".replace(
            "endChr", self._chrEndCol
        ).replace("endRow", f"{self.NUMBER_OF_ROWS}")
        if not match(regex, coords):
            return print(f"L'emplacement {coords} sur la grille n'existe pas !")

        #Les colonnes 6, 7, 8, 9 ne fonctionnent pas

        row = ord(coords[0]) - 65
        col = int(coords[1])
        self.cells[row][col] = cellCase


if __name__ == "__main__":
    Pirate = Joueur("Pirate")
    print(Pirate.grill100)
    Pirate.ajouter_ship(Ship(['A1', 'A2', 'A3'], '100', 3, 'Pirate'))
    Pirate.grill100.cases_affected('100', 'E5', Pirate)
    print(Pirate.grill100)
    print(Pirate.grill200)
