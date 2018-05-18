class Clkdiv:
    def __init__(self):
        self.c = 0

    def tick(self, n) -> bool:
        self.c += 1
        if self.c == n:
            self.c = 0
            return True
        return False

class FPS:
    def __init__(self):
        self.timeElapsed = 0

    def tick(self, fps, dt) -> bool:
        self.timeElapsed += dt
        if self.timeElapsed > (1/fps):
            self.timeElapsed -= (1/fps)
            return True
        return False