import sys
import arcade, arcade.gui, arcade.window_commands
import NetworkClientManager

# setting path
sys.path.append('../')

import Views.ArrangeShipView as ArrangeShipView

class HostOrJoinView(arcade.View):
    """Arrange your ships View
    """
    def __init__(self, WIDTH, HEIGHT):
        """Initialize the window
        """

        # Call the parent class constructor
        super().__init__()

        self.manager = None
        self.button_normal = None
        self.bg = None

        self.bg_w = WIDTH
        self.bg_h = HEIGHT

        self.nw = NetworkClientManager.NetworkClientManager()

    def setup(self):
        self.bg = arcade.load_texture("assests/bg.jpg")
        self.button_normal = arcade.load_texture(':resources:gui_basic_assets/red_button_normal.png')
        self.button_pressed = arcade.load_texture(':resources:gui_basic_assets/red_button_press.png')
        self.button_hovered = arcade.load_texture(':resources:gui_basic_assets/red_button_hover.png')
        self.label_text = arcade.load_texture(":resources:onscreen_controls/flat_dark/unchecked.png")
        self.inputbox = arcade.load_texture("assests/UIPack/PNG/red_button10.png")
        self.tick = arcade.load_texture("assests/UIPack/PNG/red_boxCheckmark.png")

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.box = arcade.gui.UIBoxLayout()
        self.button = arcade.gui.UITextureButton(texture= self.button_normal, texture_hovered = self.button_hovered, \
                                            texture_pressed=self.button_pressed,
                                            text = "Join A Room", width = 200)
        self.box.add(self.button.with_space_around(bottom=20))

        self.button2 = arcade.gui.UITextureButton(texture= self.button_normal, texture_hovered = self.button_hovered, \
                                            texture_pressed=self.button_pressed,
                                            text = "Host A Room", width = 200)
        self.box.add(self.button2.with_space_around(bottom=20))

        self.label = arcade.gui.UILabel(text="")

        #self.box.add(self.label.with_space_around(bottom=20))

        self.button.on_click = self.join_on_click_button
        self.button2.on_click = self.host_on_click_button

        self.input_field = arcade.gui.UIInputText(color=arcade.color.DARK_BLUE_GRAY, width=200, text="")
        #self.box.add(self.input_field.with_space_around(bottom=20))

        self.UIAnchorWidget = arcade.gui.UIAnchorWidget(anchor_x='center_x', anchor_y='center_y', child=self.box)
        self.manager.add(self.UIAnchorWidget)

        # Set the background window
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        """Called whenever you need to draw your window
        """
        self.clear()

        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            self.bg_w, self.bg_h,
                                            self.bg)

        self.manager.draw()

    def host_on_click_button(self, event):
        print('Host Button clicked!')

        self.nw.SetMode(NetworkClientManager.ClientEnums.HOST)
        roomcode = self.nw.StartHost()
        self.label.text = f"Room Code: {roomcode}. Waiting for second player to connect..."
        self.label.fit_content()

        self.label.trigger_full_render()
        self.box.add(self.label.with_background(self.label_text, top=10, bottom=10, right=100, left=100))
        self.box.trigger_full_render()

    def join_on_click_button(self, event):
        print('Join Button clicked!')
        self.box2 = arcade.gui.UIBoxLayout(vertical=False)

        self.label.text = "Please enter your room code: "
        self.label.fit_content()

        self.box2.add(self.input_field.with_background(self.inputbox, top = 12.5, bottom= -12.5, left = 70, right = -70))
        tickbutton = arcade.gui.UITextureButton(texture=self.tick)
        tickbutton.on_click = self.connect_on_click_button
        self.box2.add(tickbutton)

        self.box.add(self.label.with_space_around(bottom=10))
        self.box.add(self.box2)
        self.box.trigger_full_render()

    def connect_on_click_button(self, event):
        print(f"Clicked on connect button {self.input_field.text}")
        self.nw.SetMode(NetworkClientManager.ClientEnums.CLIENT)
        self.nw.StartJoin(int(self.input_field.text))

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        pass

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        pass

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        pass

    def on_update(self, delta_time: float):
        if self.nw.IsConnected():
            newview = ArrangeShipView.ArrangeShipsView()
            newview.setup(self.nw)
            self.window.show_view(newview)
