import sys, arcade

# setting path
sys.path.append('../')

import UI.GridElement as GridElement
import UI.ShipSprite as ShipSprite
import UI.Button as Button

import Views.GameView as GameView

import gameParams, NetworkClientManager

# Classes
class ArrangeShipsView(arcade.View):
    """Arrange your ships View
    """
    def __init__(self):
        """Initialize the window
        """

        # Call the parent class constructor
        super().__init__()

        self.MyGrid = GridElement.GridElement(10, 10)
        self.OpponentGrid = GridElement.GridElement(10, 10)

        self.shipList = gameParams.GameParams.shipList
        self.shipSpriteList = [ShipSprite.ShipSprite(self.shipList[i], f"assests/ship{i+1}.png") for i in range(len(self.shipList))]

        self.bg_w = gameParams.GameParams.SCREEN_WIDTH
        self.bg_h = gameParams.GameParams.SCREEN_HEIGHT

        # assets
        self.bg = None

        self.mx = 0
        self.my = 0
        self.isDrag = False

        self.button = None

        self.nw = None

    def setup(self, nw):
        for x in range(0, len(self.shipList)):
            self.MyGrid.GetGrid().placeShip(self.shipList[x], [0, 0 + x])

        w_grid, h_grid = self.MyGrid.GetSize()
        grid_x = (self.bg_w - (w_grid)) / 2
        self.MyGrid.SetPosition(grid_x, (h_grid) // 2)
        #self.OpponentGrid.SetPosition(w_grid + 50 + grid_x, (h_grid) // 2)

        self.nw = nw

        self.arrangeDone = False

        self.bg = arcade.load_texture("assests/bg.jpg")

        self.button = Button.Button("assests/btn_startwar.png")
        self.button.Scale(0.75, 0.75)
        self.button.SetPosition((self.bg_w - self.button.width) / 2, 10)

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
        #self.OpponentGrid.Draw()

        for shipSprite in self.shipSpriteList:
            shipSprite.drawShip(self.MyGrid)

        x, y = self.MyGrid.GetPosition()
        w, h = self.MyGrid.GetSize()
        arcade.draw_text("Your Grid", x + w/2, y - 24, color= arcade.color.BLACK, anchor_x='center', bold = True)

        #x, y = self.OpponentGrid.GetPosition()
        #w, h = self.OpponentGrid.GetSize()
        #arcade.draw_text("Opponent's Grid", x + w/2, y - 24, color= arcade.color.BLACK, anchor_x='center', bold = True)

        self.button.Draw()

    #def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        #print("MOUSE PRESS")

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        for shipSprite in self.shipSpriteList:
            if self.isDrag == False and shipSprite.isMouseWithin(x, y, self.MyGrid):
                shipSprite.setMouseOverride(True)
                shipSprite.setMousePos(self.MyGrid, x, y)
            elif shipSprite.mouse_override == True:
                shipSprite.setMousePos(self.MyGrid, x, y)

        self.isDrag = True

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        if(self.isDrag == False):
            for shipSprite in self.shipSpriteList:
                if shipSprite.isMouseWithin(x, y, self.MyGrid):
                    self.MyGrid.GetGrid().changeOrientationOfShip(shipSprite.ship)

            if self.button.IsClicked(x, y):
                print('Button pressed')
                self.arrangeDone = True
        else:
            print("MOUSE DRAG - RELEASE")
            self.isDrag = False
            for shipSprite in self.shipSpriteList:
                if shipSprite.mouse_override == True:
                    shipSprite.setMouseOverride(False)
                    shipSprite.LatchToMousePos(x, y, self.MyGrid)

    def check_if_client_arranged(self):
        done = self.nw.IsArrangeDoneByClient()
        if done and self.arrangeDone:
            self.nw.ChangeScreen()
            view = GameView.GameView()
            view.setup(self.MyGrid, self.shipList, self.nw)
            self.window.show_view(view)

    def on_update(self, delta_time: float):
        if self.nw.GetMode() == NetworkClientManager.ClientEnums.CLIENT:
            ret = self.nw.HandleArrangeStatus(self.arrangeDone)
            if ret == 1: #changeScreen
                view = GameView.GameView()
                view.setup(self.MyGrid, self.shipList, self.nw)
                self.window.show_view(view)
        else:
            self.check_if_client_arranged()
