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

    # Vérifie si le navire est coulé
    def est_coule(self):
        return len(self.touches) == self.taille

class Joueur:
    def __init__(self, name: str):
        self.name = name
        self.ships = [] # Liste des navires du joueur
        self.grill100 = Grid()
        self.grill200 = Grid()
        self.grill300 = Grid()

    def ajouter_ship(self, ship: Ship):
        self.ships.append(ship)

    # Vérifie si le joueur a perdu (tous ses navires sont coulés)
    def a_perdu(self) -> bool:
        for ship in self.ships:
            if not ship.est_coule():
                return False
        return True

    def cases_affected(self, profondeur:str, coord: str) -> None:
        dico_Grilles = {
            '100': self.grill100, '200': self.grill200, '300': self.grill300} # dictionnaire pour accéder à la grille en fonction de la profondeur
        for ships in self.ships:
            if ships.profondeur == profondeur:
                for ship_coord in ships.coords: # vérifie si la cible touche un navire
                    if ship_coord == coord:
                        if coord not in ships.touches:
                            ships.touches.append(coord)
                        dico_Grilles[profondeur].fireOnTarget(coord, CellCase.TARGET_HIT)
                        if ships.est_coule():
                            for sunk_coord in ships.coords: # Cas où le navire est coulé
                                dico_Grilles[profondeur].fireOnTarget(sunk_coord, CellCase.TARGET_DESTROYED)
                            print(f"Le navire de taille {ships.taille} du joueur {self.name} a été coulé !")
                        return

                row, col = coord[0], coord[1]
                #construction des coordonnées entourant la cible
                adjacent_coords = [coord,       # cible
                    f"{chr(ord(row)-1)}{col}",  # au-dessus
                    f"{chr(ord(row)+1)}{col}",  # en-dessous
                    f"{row}{int(col)-1}",       # à gauche
                    f"{row}{int(col)+1}"        # à droite
                ]
                for adjacent in adjacent_coords: # vérifie si un sous-marin est adjacent à la cible
                    for ships.coord in ships.coords:
                        if adjacent == ships.coord:
                            for adjacent2 in adjacent_coords:
                                if '@' not in adjacent2 and '0' not in adjacent2: #filtre les effets de bord
                                    dico_Grilles[profondeur].fireOnTarget(adjacent2, CellCase.TARGET_FOUND)
                                dico_Grilles[profondeur].affect_other_depths(profondeur, coord, self, CellCase.TARGET_FOUND)
                            return
                for adjacent in adjacent_coords: # marque les cases adjacentes comme n'ayant pas de sous-marin
                    if '@' not in adjacent and '0' not in adjacent: #filtre les effets de bord
                        dico_Grilles[profondeur].fireOnTarget(adjacent, CellCase.TARGET_NOTHING)
                    dico_Grilles[profondeur].affect_other_depths(profondeur, coord, self, CellCase.TARGET_NOTHING)
                return

# Définition des cas possibles dans une case sur la grille
class CellCase(Enum):
    TARGET_UNKNOWN = "*"
    # Aucun sous-marin dans cette case
    TARGET_NOTHING = "R"
    # sous-marin repéré
    TARGET_FOUND = "V"
    # sous-marin touché
    TARGET_HIT = "T"
    # sous-marin détruit
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
        print(
            tabulate(
                headers=self.headers,
                tabular_data=self.cells,
                tablefmt="rounded_grid",
                stralign="center",
            ), end=''
        )
        return ''

    # Met à jour les autres grilles de profondeur en fonction de l'attaque
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


    # Met à jour la grille en fonction des coordonnées et du cas de la cellule déterminées par cases_affected
    def fireOnTarget(self, coords: str, cellCase: CellCase):
        regex = "^[A-endChr1]{1}[1-endRow]{1}".replace(
            "endChr", self._chrEndCol
        ).replace("endRow", f"{self.NUMBER_OF_COLS -1}")
        if not match(regex, coords):
            pass

        try: # gère les coordonnées invalides générées par cases_affected
            row = ord(coords[0]) - 65
            col = int(coords[1])
            if self.cells[row][col] != 'T' and self.cells[row][col] != 'C': # ne pas écraser les cases déjà touchées ou coulées
                self.cells[row][col] = cellCase
        except:
            pass


if __name__ == "__main__":  #tests
    Pirate = Joueur("Pirate")
    print(Pirate.grill100)
    Pirate.ajouter_ship(Ship(['A1', 'A2', 'A3'], '100', 3, 'Pirate'))
    Pirate.cases_affected('100', 'A2')
    print(Pirate.grill100)
    Pirate.cases_affected('100', 'A3')
    Pirate.cases_affected('100', 'A1')
    Pirate.cases_affected('100', 'D7')
    print(Pirate.grill100)
