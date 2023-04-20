import sys, arcade
import Views.HostOrJoinView as HostOrJoinView

# setting path
sys.path.append('../')

class StartView(arcade.View):
    """ Start View
    """

    """ Constructor parameterized
    """
    def __init__(self, params):
        """Initialize the window
        """

        # Call the parent class constructor
        super().__init__()

        # assets
        self.bg = None
        self.title = None
        self.playButton = None

        # BG width and height
        self.bg_w = params.SCREEN_WIDTH
        self.bg_h = params.SCREEN_HEIGHT

        self.alpha = 0
        self.alphaMultiplier = 1

    def setup(self):
        self.bg = arcade.load_texture("assests/bg.jpg")
        self.title = arcade.load_texture("assests/game_title.png")
        self.playButton = arcade.load_texture("assests/btn_play.png")

        # Set the background window
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        """Called whenever you need to draw your window
        """

        # Clear the screen and start drawing
        self.clear()

        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            self.bg_w, self.bg_h,
                                            self.bg)


        arcade.draw_texture_rectangle(self.bg_w // 2, self.bg_h // 2 + 50, self.title.width / 1.5, self.title.height / 1.5, self.title)
        arcade.draw_texture_rectangle(self.bg_w // 2, self.bg_h // 2 - 150, self.playButton.width // 1.75, self.playButton.height // 1.75, self.playButton, alpha = self.alpha)


    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        newview = HostOrJoinView.HostOrJoinView(self.bg_w, self.bg_h)
        newview.setup()
        self.window.show_view(newview)

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        pass

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        pass

    def on_update(self, delta_time: float):
        self.alpha = (self.alpha + (3 * self.alphaMultiplier))
        if self.alpha > 255:
            self.alphaMultiplier = -1
            self.alpha = self.alpha = 255
        elif self.alpha < 0:
            self.alphaMultiplier = 1
            self.alpha = 10
