import arcade

class Button:
    def __init__(self, texture_loc):
        self.texture = arcade.load_texture(texture_loc)
        self.x = 0
        self.y = 0
        self.width = self.texture.width
        self.height = self.texture.height
        self.scaleFactorW = 1
        self.scaleFactorH = 1

    def SetPosition(self, x, y):
        self.x = x
        self.y = y

    def Scale(self, scaleFactorW, scaleFactorH):
        self.width *= scaleFactorW
        self.height *= scaleFactorH

    def Draw(self):
        arcade.draw_lrwh_rectangle_textured(self.x, self.y, self.width, self.height, self.texture)

    def IsMouseWithin(self, mx, my):
        if mx >= self.x and mx <= self.x + self.width and my >= self.y and my <= self.y + self.height:
            return True
        return False

    def IsClicked(self, mx, my):
        return self.IsMouseWithin(mx, my)
