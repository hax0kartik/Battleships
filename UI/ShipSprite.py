import sys
import arcade

sys.path.append('../base')

from base.Ship import Ship

class ShipSprite:
    def __init__(self, ship, spriteLoc):
        self.ship = ship
        self.img = arcade.load_texture(spriteLoc)
        self.imgr = self.img.image.rotate(90)
        self.mouse_override = False
        self.mox = 0
        self.moy = 0
        self.anchorx = 0
        self.anchory = 0
        self.orow = 0
        self.ocol = 0

    def setMouseOverride(self, flag):
        self.orow, self.ocol = self.ship.getHead()
        self.mouse_override = flag

    def setMousePos(self, grid, mx, my):
        x, y, w, h = self.calcBoundRect(grid)
        self.mox = mx - self.anchorx
        self.moy = my - self.anchory

    def calcBoundRect(self, grid):
        i, j = self.ship.getHead()
        x, y, w, h = grid.GetRectFromPos(i, j)
        draw_h = h
        if self.ship.getOrientation() == 0: # vertically
            draw_h = draw_h * self.ship.getSize()
            y -= draw_h - h
        else:
            w = w * self.ship.getSize()

        return [x, y, w, draw_h]

    def drawShip(self, grid):
        x, y, w, h = self.calcBoundRect(grid)
        if self.mouse_override:
            x = self.mox
            y = self.moy

        # Draw the box
        arcade.draw_lrtb_rectangle_outline(x - 1, x + w, y + h, y, arcade.color.DARK_BLUE, 2)
        arcade.draw_lrtb_rectangle_filled(x + 1, x + w - 1, y + h - 2, y + 1, arcade.color.BABY_BLUE)

    def isMouseWithin(self, mx, my, grid):
        x, y, w, h = self.calcBoundRect(grid)
        if mx >= x and mx <= x + w and my >= y and my <= y + h:
            self.anchory = my - y
            self.anchorx = mx - x
            print(f"Anchor X :{self.anchorx} Anchor Y:{self.anchory}")
            return True

        return False

    def LatchToMousePos(self, mx, my, grid):
        x, y, w, h = self.calcBoundRect(grid)
        row, column = grid.GetPosFromCoord(mx - self.anchorx, my + (h - self.anchory))
        grid.GetGrid().cleanOrignalPos(self.ship, self.orow, self.ocol, self.ship.getOrientation(), False)
        n_rows, n_cols = grid.GetGrid().GetSize()
        if grid.GetGrid().placeShip(self.ship, [round(row), int(column)]) == False:
            grid.GetGrid().placeShip(self.ship, [self.orow, self.ocol])
            self.orow = 0
            self.ocol = 0
        self.mouse_override = False

