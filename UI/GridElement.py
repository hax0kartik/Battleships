import sys
import arcade

# setting path
sys.path.append('../base')

from base.Grid import Grid

WIDTH = 30
HEIGHT = 30

class GridElement:
    def __init__(self, nrow, ncolumn, x = 0, y = 0, w = 0, h = 0):
        self.grid = Grid(nrow, ncolumn)
        self.grid.initGrid()
        self.tile = arcade.load_texture("assests/tile.png")
        self.tile_red = arcade.load_texture("assests/UIPack/PNG/red_cross.png")
        self.tile_green = arcade.load_texture("assests/UIPack/PNG/green_circle.png")
        self.tiles = [self.tile, self.tile, self.tile_green, self.tile_red]
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def SetPosition(self, x, y):
        self.x = x
        self.y = y

    def GetPosition(self):
        return [self.x, self.y]

    def GetSize(self):
        grid = self.grid.GetGrid()
        height = HEIGHT + (HEIGHT * len(grid))
        width = WIDTH + (WIDTH * len(grid[0]))
        return [width, height]

    def Draw(self):
        grid = self.grid.GetGrid()
        for row in range(0, len(grid[0])):
            arcade.draw_text(len(grid) - row, self.x, (HEIGHT) * row + HEIGHT // 2 + self.y, color = arcade.color.BLACK, align="center", width = WIDTH)
            for column in range(0, len(grid)):
                 # Do the math to figure out where the box is
                x = (WIDTH) * column + WIDTH // 2 + WIDTH + self.x
                y = (HEIGHT) * row + HEIGHT // 2 + self.y

                # Draw the box
                #arcade.draw_rectangle_outline(x, y, WIDTH, HEIGHT, arcade.color.BLUE, 1)
                arcade.draw_texture_rectangle(x, y, WIDTH, HEIGHT, self.tile)

        x = WIDTH + self.x
        y = (HEIGHT) * len(grid) + self.y + HEIGHT // 3
        for column in range(0, len(grid)):
            arcade.draw_text(chr(ord('A') + column), x, y, color = arcade.color.BLACK, align="center", width = WIDTH)
            x = x + WIDTH

    def DrawHits(self):
        grid = self.grid.GetGrid()
        for row in range(0, len(grid[0])):
            arcade.draw_text(len(grid) - row, self.x, (HEIGHT) * row + HEIGHT // 2 + self.y, color = arcade.color.BLACK, align="center", width = WIDTH)
            for column in range(0, len(grid)):
                 # Do the math to figure out where the box is
                x = (WIDTH) * column + WIDTH // 2 + WIDTH + self.x
                y = (HEIGHT) * row + HEIGHT // 2 + self.y

                # Draw the box
                #arcade.draw_rectangle_outline(x, y, WIDTH, HEIGHT, arcade.color.BLUE, 1)
                if grid[self.grid.n_row - row - 1][column] == 2:
                    arcade.draw_texture_rectangle(x, y, self.tile_green.width / 1.5, self.tile_green.height / 1.5, self.tile_green)
                elif grid[self.grid.n_row - row - 1][column] == 3:
                    arcade.draw_texture_rectangle(x, y, self.tile_red.width / 1.5, self.tile_red.height / 1.5, self.tile_red)

    def GetRectFromPos(self, row, column):
        x = (WIDTH) * (column) + WIDTH + self.x
        y = (HEIGHT) * (self.grid.n_row - row - 1) + self.y
        return [x, y, WIDTH, HEIGHT]

    def GetPosFromCoord(self, x, y):
        column = (x - self.x - WIDTH) // WIDTH
        row = self.grid.n_row - ((y - self.y) // HEIGHT) - 1
        return [row, column]

    def GetGrid(self):
        return self.grid

    def ProcessEvents():
        pass
