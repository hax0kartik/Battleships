import sys, arcade

# setting path
sys.path.append('../')
import gameParams, NetworkClientManager
import UI.GridElement as GridElement
import UI.ShipSprite as ShipSprite

class GameView(arcade.View):
    def __init__(self):
         # Call the parent class constructor
        super().__init__()

        self.OpponentGrid = GridElement.GridElement(10, 10)
        # TODO: Should be none here
        self.MyGrid = GridElement.GridElement(10, 10)
        self.ShipList = None
        self.nw = None

        self.bg_w = gameParams.GameParams.SCREEN_WIDTH
        self.bg_h = gameParams.GameParams.SCREEN_HEIGHT

        self.chance = 0

        # assets
        self.bg = None

    def setup(self, grid, shipList, nw : NetworkClientManager.NetworkClientManager):
        self.MyGrid = grid
        self.ShipList = shipList
        self.nw = nw

        self.chance = int(self.nw.GetMode()) - 1
        self.pos = None

        self.nw.SetSocketToNonBlocking()

        self.ShipSpriteList = [ShipSprite.ShipSprite(self.ShipList[i], f"assests/ship{i+1}.png") for i in range(len(self.ShipList))]

        w_grid, h_grid = self.MyGrid.GetSize()
        grid_x = (self.bg_w - (w_grid + 50 + w_grid)) / 2
        self.MyGrid.SetPosition(grid_x, (h_grid) // 2)
        self.OpponentGrid.SetPosition(w_grid + 50 + grid_x, (h_grid) // 2)

        self.bg = arcade.load_texture("assests/bg.jpg")

        turn_asset1 = arcade.load_texture("assests/turn1.png")
        turn_asset2 = arcade.load_texture("assests/turn2.png")
        self.turn_textures = [turn_asset2, turn_asset1]

        # Game Logic
        self.hits = 0
        for ship in self.ShipList:
            self.hits += ship.getSize()

        # Set the background window
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        """Called whenever you need to draw your window
        """

        # Clear the screen and start drawing
        arcade.start_render()

        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            self.bg_w, self.bg_h,
                                            self.bg)

        self.MyGrid.Draw()
        self.OpponentGrid.Draw()

        x, y = self.MyGrid.GetPosition()
        w, h = self.MyGrid.GetSize()
        arcade.draw_text("Your Grid", x + w/2, y - 24, color= arcade.color.BLACK, anchor_x='center', bold = True)

        x, y = self.OpponentGrid.GetPosition()
        w, h = self.OpponentGrid.GetSize()
        arcade.draw_text("Opponent's Grid", x + w/2, y - 24, color= arcade.color.BLACK, anchor_x='center', bold = True)

        for ShipSprite in self.ShipSpriteList:
            ShipSprite.drawShip(self.MyGrid)

        self.MyGrid.DrawHits()
        self.OpponentGrid.DrawHits()

        arcade.draw_xywh_rectangle_filled((self.chance ^ 1) * (self.bg_w/2), 0, self.bg_w/2, self.bg_h, arcade.color_from_hex_string('33000000'))

        arcade.draw_texture_rectangle(self.bg_w/2, self.bg_h - (self.turn_textures[self.chance].height/2), self.turn_textures[self.chance].width, self.turn_textures[self.chance].height, self.turn_textures[self.chance])

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        # Check if the click is within the right part of the screen
        if(self.chance and x >= self.bg_w/2):
            i, j = self.OpponentGrid.GetPosFromCoord(x, y)
            if i < 0 or j < 0:
                return
            print(f"{i} {j} clicked")
            self.pos = [int(i), int(j)]
            self.nw.SendGuess(int(i), int(j))

    def on_update(self, delta_time: float):
        flag = self.nw.HandleGuess(self.CheckHit, ())
        if flag is not None and (flag == 0 or flag == 1):
            self.OpponentGrid.GetGrid().TryHit(self.pos[0], self.pos[1], flag)
            self.chance = self.chance ^ 1
            self.pos = None
        elif flag is not None and flag == 3:
            self.OpponentGrid.GetGrid().TryHit(self.pos[0], self.pos[1], 1)
            print('You have won')
        if self.hits == 0:
            print('You have lost')


    def CheckHit(self, i, j):
        self.chance = self.chance ^ 1
        hit = self.MyGrid.GetGrid().TryHit(i, j)
        if hit:
            self.hits -= 1
        win = True if self.hits == 0 else False
        return [win, hit]

