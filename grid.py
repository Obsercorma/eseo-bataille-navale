from tabulate import tabulate
from enum import Enum
from re import match

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

    def __init__(self, depth: DepthRule):
        self.cells = []
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
        print(
            tabulate(
                headers=self.headers, tabular_data=self.cells, tablefmt="rounded_grid"
            ),
        )

    def fireOnTarget(self, coords: str, cellCase: CellCase):
        regex = "^[A-endChr1]{1}[1-endRow]{1}".replace(
            "endChr", self._chrEndCol
        ).replace("endRow", f"{self.NUMBER_OF_ROWS}")
        if not match(regex, coords):
            return print(f"L'emplacement {coords} sur la grille n'existe pas !")

        row = ord(coords[0]) - 65
        col = int(coords[1])
        self.cells[row][col] = cellCase


if __name__ == "__main__":
    gridTest = Grid(DepthRule.DEPTH_200)
    gridTest.generate_grid()
    gridTest.fireOnTarget("B2", CellCase.TARGET_HIT)
    gridTest.generate_grid()
