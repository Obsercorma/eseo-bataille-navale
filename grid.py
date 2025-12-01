from tabulate import tabulate


class Grid:
    NUMBER_OF_COLS = 9
    NUMBER_OF_ROWS = 5
    CHR_START_INDEX = 65  # 'A'

    def __init__(self):
        self.cells = []
        self.headers = [
            hName if hName != 0 else " " for hName in range(self.NUMBER_OF_COLS)
        ]

    def generate_grid(self):
        self.cells = [
            [
                "*" if col != 0 else chr(self.CHR_START_INDEX + row)
                for col in range(self.NUMBER_OF_COLS)
            ]
            for row in range(self.NUMBER_OF_ROWS)
        ]
        print(
            tabulate(
                headers=self.headers, tabular_data=self.cells, tablefmt="rounded_grid"
            )
        )


if __name__ == "__main__":
    gridTest = Grid()
    gridTest.generate_grid()
