import arcade
import gameParams
import Views.StartView as StartView
import Views.ArrangeShipView as ArrangeShipView

params = gameParams.GameParams()

# Main code entry point
if __name__ == "__main__":
    window = arcade.Window(params.SCREEN_WIDTH, params.SCREEN_HEIGHT, params.SCREEN_TITLE)
    view = StartView.StartView(params)
    #view = ArrangeShipView.ArrangeShipsView()
    window.show_view(view)
    view.setup()
    arcade.run()