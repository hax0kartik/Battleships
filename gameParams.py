import base.Ship as Ship

class GameParams:

#--------------------------Constants-------------------
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    SCREEN_TITLE = "BATTLESHIPS"
#------------------------------------------------------
#-------------------------- Ships ---------------------
    DESTROYER = Ship.Ship(2)
    SUBMARINE = Ship.Ship(3)
    CRUISER = Ship.Ship(3)
    BATTLESHIP = Ship.Ship(4)
    CARRIER = Ship.Ship(5)
    shipList = [CARRIER, DESTROYER, CRUISER, SUBMARINE, BATTLESHIP]
#-------------------------------------------------------
#-------------------------------------------------------

    def __init__(self):
        pass