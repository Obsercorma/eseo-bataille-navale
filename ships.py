class Ship:
    def __init__(self, coords: list[str], nbcases: int):
        self.coords = [{coord: nameCoord, hit: False} for nameCoord in coords]
        self.nbcases = nbcases
        self.isDestroyed = False

class Sea:
    MER_A = "Mer A"
    MER_B = "Mer B"
    def __str__(self):
        return f"{self.value}m"