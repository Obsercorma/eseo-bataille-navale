class Ship:
    def __init__(self, coords: list[str]):
        self.coords = [{coord: nameCoord, hit: False} for nameCoord in coords]
        self.isDestroyed = False
