from pyreeEngine.textures import TextureFromImage

class imgAnim():
    def __init__(self, paths):
        self.paths = paths
        self.playMode = "pingpong"

        self.textures = []

        for path in self.paths:
            self.textures.append(TextureFromImage(path))

        self.framecount = len(self.textures)

        self.indx = 0
        self.forwards = True

    def setPingPong(self):
        self.playMode = "pingpong"

    def setRepeat(self):
        self.playMode = "repeat"

    def nextFrame(self):
        if self.forwards:
            self.indx += 1
            if self.indx == self.framecount:
                if self.playMode == "repeat":
                    self.indx = 0
                elif self.playMode == "pingpong":
                    self.indx -= 2
                    self.forwards = False
        else:
            self.indx -= 1
            if self.indx < 0:
                self.indx = 1
                self.forwards = True

        return self.textures[self.indx]
