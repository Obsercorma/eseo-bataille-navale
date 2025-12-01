from tabulate import tabulate
from enum import Enum
from re import match
from ships import Ship

CLEAR_CHR = "\x1b[2J"


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


# Cas de profondeurs en mètres
class DepthRule(Enum):
    # 100m
    DEPTH_100 = 100
    # 200m
    DEPTH_200 = 200
    # 300m
    DEPTH_300 = 300

    def __str__(self):
        return f"{self.value}m"


class Grid:
    NUMBER_OF_COLS = 10
    NUMBER_OF_ROWS = 5
    CHR_START_INDEX = 65  # 'A'

    def __init__(self, depth: DepthRule, sea: str, ships: list[Ship]):
        self.cells = []
        self.ships = ships
        self.sea = sea
        self.depth = depth
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

    # Vérifie si la profondeur renseigné correspond à celle qui a été initialisé au départ
    def checkDepth(self, depth: int):
        return depth == self.depth.value

    def generate_grid(self):
        print(CLEAR_CHR)
        print(f"Grille {self.sea}".center(65))
        print(
            tabulate(
                headers=self.headers,
                tabular_data=self.cells,
                tablefmt="rounded_grid",
                stralign="center",
            ),
        )

    def fireOnTarget(self, coords: str):
        regex = "^[A-endChr1]{1}[1-endRow]{1}".replace(
            "endChr", self._chrEndCol
        ).replace("endRow", f"{self.NUMBER_OF_ROWS}")
        if not match(regex, coords):
            return print(f"L'emplacement {coords} sur la grille n'existe pas !")

        row = ord(coords[0]) - 65
        col = int(coords[1])

        for ship in self.ships:
            if ship.coords == coords:
                self.cells[row][col] = CellCase.TARGET_HIT
            topCell = chr(64 + col)
            bottomCell = chr(66 + col)
            leftCell = col - 1
            rightCell = col + 1
            if f"{row}{leftCell}":
                self.cells[row][leftCell] = CellCase.TARGET_FOUND
            if f"{row}{rightCell}":
                self.cells[row][rightCell] = CellCase.TARGET_FOUND
            if f"{topCell}{col}":
                self.cells[topCell][col] = CellCase.TARGET_FOUND
            if f"{bottomCell}{col}":
                self.cells[bottomCell][col] = CellCase.TARGET_FOUND


if __name__ == "__main__":
    gridTest = Grid(DepthRule.DEPTH_200, "Mer A", [])
    gridTest.generate_grid()
    gridTest.fireOnTarget("B2")
    gridTest.generate_grid()
