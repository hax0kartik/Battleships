class Ship:

    def __init__(self, size, orientation=0):
        self.start = [-1, -1]
        # no of blocks
        self.size = size
        # 0 -> vertically
        # 1 -> horizonatly
        self.orientation = orientation

    def changeOrientation(self, orientation):
        if orientation == 0 or orientation == 1:
            self.orientation = orientation

    def setHead(self, headIndex):
        self.start = headIndex

    def getSize(self):
        return self.size

    def getHead(self):
        return self.start

    def getOrientation(self):
        return self.orientation
