class Grid:
    def __init__(self, row, column):
        self.n_row = row
        self.n_column = column
        self.grid = []

    def initGrid(self):
        for i in range(0, self.n_row):
            self.grid.append([])
            for j in range(0, self.n_column):
                self.grid[i].append(0)

    def GetGrid(self):
        return self.grid

    def GetSize(self):
        return [self.n_row, self.n_column]

    def SetGrid(self, grid):
        for i in range(0, self.n_row):
            for j in range(0, self.n_column):
                self.grid[i][j] = grid[i][j]

    def printGrid(self):
        print(' |', end = '')
        for x in range(0, 10):
            print(chr(ord('A') + x) + '|', end = '')
        print("")
        for i in range(0, self.n_row):
            print(i, end='|')
            for j in range(0, self.n_column):
                print(self.grid[i][j], end = '|')
            print("")

    # col, row here are 0-indexed i,j
    def placeShip(self, Ship, indexes, ignoreHead = False):
        row = indexes[0]
        col = indexes[1]

        if row < 0 or row > self.n_row or col < 0 or col > self.n_column:
            return False

        if Ship.orientation == 0 and row + Ship.size > self.n_row:
            return False

        elif Ship.orientation == 1 and col + Ship.size > self.n_column:
            return False

        for x in range(0 + int(ignoreHead), Ship.size):
            if Ship.orientation == 0 and self.grid[row + x][col] != 0:
                return False
            elif Ship.orientation == 1 and self.grid[row][col + x] != 0:
                return False

        for x in range(0, Ship.size):
            if Ship.orientation == 1: # Horizantally
                self.grid[row][col + x] = 1
            else: # Vertically
                self.grid[row + x][col] = 1
        Ship.setHead([row, col])
        return True

    def changeOrientationOfShip(self, Ship):
        Ship.orientation = Ship.orientation ^ 1
        indexes = Ship.getHead()
        if self.placeShip(Ship, indexes, True) == False:
            Ship.orientation = Ship.orientation ^ 1
            print("Can't change orienation")
        else:
            oriOrientation = Ship.orientation ^ 1
            row = indexes[0]
            col = indexes[1]
            print(f"Row {row} Col: {col}")
            self.cleanOrignalPos(Ship, row, col, oriOrientation, True)
        self.printGrid()

    def cleanOrignalPos(self, ship, row, col, orientation = 0, ignoreHead = False):
        for x in range(0 + int(ignoreHead), ship.size):
            if orientation == 1: # Horizantally
                self.grid[row][col + x] = 0
            else: # Vertically
                self.grid[row + x][col] = 0

    def TryHit(self, i, j, force = False):
        if self.grid[i][j] == 1 or force:
            print(f"Setting grid {i} {j} to 2")
            self.grid[i][j] = 2
            return True
        else:
            self.grid[i][j] = 3
        return False

